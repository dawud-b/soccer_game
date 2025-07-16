import socket
import json
import threading
import Soccer_Game # Import your game logic file

# Global game state (managed by the server)
game_state = {
    "p1_ownership": True,  # True if P1 has ownership, False if P2
    "shoot_phase": False,  # True if it's a shooting phase
    "p1_score": 0,
    "p2_score": 0,
    "position": 0,  # 0 means middle of field. +3 is P1 goal, -3 is P2 goal
    "p1_input": None,
    "p2_input": None,
    "turn": "player1",  # 'player1' or 'player2'
    "status": "waiting_for_players", # 'waiting_for_players', 'playing', 'finished'
    "message": "Waiting for players to join...",
    "player_map": {} # Maps client address (string) to player1/player2 string
}

# Global lock for synchronizing access to game_state
game_state_lock = threading.Lock()

# Sockets for connected clients
clients = [] # Stores (conn, addr) tuples

def reset_game_state_server():
    """Resets the game state to initial values using Soccer_Game logic. Assumes game_state_lock is held by caller."""
    global game_state
    p1_ownership, shoot_phase, p1_score, p2_score, position = Soccer_Game.reset_game_logic()
    game_state["p1_ownership"] = p1_ownership
    game_state["shoot_phase"] = shoot_phase
    game_state["p1_score"] = p1_score
    game_state["p2_score"] = p2_score
    game_state["position"] = position
    game_state["p1_input"] = None
    game_state["p2_input"] = None
    game_state["turn"] = "player1" # Always start with player1's turn after reset
    game_state["status"] = "playing"
    game_state["message"] = "Game reset! Player 1's turn."
    # player_map is preserved


def send_game_state(conn, state):
    """Sends the current game state to a specific client."""
    try:
        # Serialize the dictionary to a JSON string
        json_state = json.dumps(state)
        # Encode the string to bytes and send its length first
        conn.sendall(len(json_state).to_bytes(4, 'big')) # Send 4-byte length
        conn.sendall(json_state.encode('utf-8'))
    except Exception as e:
        print(f"Error sending state to client {conn.getpeername()}: {e}")
        # Handle disconnection if needed

def broadcast_game_state():
    """Sends the current game state to all connected clients. Assumes game_state_lock is held by caller."""
    for conn, addr in clients:
        send_game_state(conn, game_state)

def handle_client(conn, addr, player_id):
    """Handles communication with a single client."""
    global game_state

    # Convert tuple address to string for use as dictionary key
    addr_str = f"{addr[0]}:{addr[1]}"
    print(f"Connected by {addr} as {player_id}")

    with game_state_lock: # Acquire lock for initial game_state modification and send
        game_state["player_map"][addr_str] = player_id # Store string representation
        # Create a copy of the game state and add the specific player ID for this client
        state_for_client = game_state.copy()
        state_for_client["your_player_id"] = player_id # Add the specific player ID for this client
        send_game_state(conn, state_for_client) # Send the modified state to this client

    while True:
        try:
            # Receive 4-byte length of the incoming message
            length_bytes = conn.recv(4)
            if not length_bytes:
                break # Client disconnected

            message_length = int.from_bytes(length_bytes, 'big')
            received_data = b''
            while len(received_data) < message_length:
                chunk = conn.recv(message_length - len(received_data))
                if not chunk:
                    break
                received_data += chunk

            if not received_data:
                break # Client disconnected

            player_input_str = received_data.decode('utf-8')
            print(f"Received from {player_id} ({addr}): {player_input_str}")

            with game_state_lock: # Use the global lock to protect game_state modifications
                if player_id == game_state["turn"] and game_state["status"] == "playing":
                    # Use Soccer_Game's logic to validate input
                    parsed_input = Soccer_Game.select_position_logic(player_input_str)
                    if parsed_input is None:
                        game_state["message"] = f"Invalid input from {player_id}. Please enter 1-6."
                        broadcast_game_state()
                        continue

                    if player_id == "player1":
                        game_state["p1_input"] = parsed_input
                        game_state["turn"] = "player2"
                    else: # player_id == "player2"
                        game_state["p2_input"] = parsed_input
                        game_state["turn"] = "player1"

                    game_state["message"] = f"{player_id} made a move. Waiting for other player..."

                    # If both inputs are received, process the turn using Soccer_Game logic
                    if game_state["p1_input"] is not None and game_state["p2_input"] is not None:
                        p1_ownership, shoot_phase, position, penalty_message = Soccer_Game.compare_selections(
                            game_state["p1_ownership"],
                            game_state["shoot_phase"],
                            game_state["p1_input"],
                            game_state["p2_input"],
                            game_state["position"]
                        )

                        game_state["p1_ownership"] = p1_ownership
                        game_state["shoot_phase"] = shoot_phase
                        game_state["position"] = position

                        if penalty_message:
                            game_state["message"] = penalty_message

                        # Check for score
                        if game_state["position"] > 3:
                            game_state["p2_score"] += 1
                            game_state["position"] = 0
                            game_state["shoot_phase"] = False
                            game_state["p1_ownership"] = False # P2 gains control
                            game_state["message"] = "Player 2 scored!"
                        elif game_state["position"] < -3:
                            game_state["p1_score"] += 1
                            game_state["position"] = 0
                            game_state["shoot_phase"] = False
                            game_state["p1_ownership"] = True # P1 gains control
                            game_state["message"] = "Player 1 scored!"

                        # Check for win condition
                        if game_state["p1_score"] >= 5:
                            game_state["message"] = "--- Player 1 Wins! ---"
                            game_state["status"] = "finished"
                        elif game_state["p2_score"] >= 5:
                            game_state["message"] = "--- Player 2 Wins! ---"
                            game_state["status"] = "finished"

                        # Reset inputs for next round
                        game_state["p1_input"] = None
                        game_state["p2_input"] = None

                        # Set turn based on new ownership if game not finished
                        if game_state["status"] == "playing":
                            game_state["turn"] = "player1" if game_state["p1_ownership"] else "player2"

                    broadcast_game_state()
                elif player_input_str == "reset_game":
                    reset_game_state_server() # Use the server's reset wrapper
                    broadcast_game_state()
                else:
                    # It's not the player's turn, or game not playing
                    game_state["message"] = f"It's not {player_id}'s turn or game not in playing state."
                    send_game_state(conn, game_state) # Send specific message back to only this client
        except ConnectionResetError:
            print(f"Client {addr} disconnected unexpectedly.")
            break
        except json.JSONDecodeError:
            print(f"Invalid JSON received from {addr}")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    # Client disconnected
    print(f"Client {addr} disconnected.")
    with game_state_lock: # Use the global lock for client removal and game state update
        clients.remove((conn, addr))
        addr_str_to_remove = f"{addr[0]}:{addr[1]}"
        if addr_str_to_remove in game_state["player_map"]:
            del game_state["player_map"][addr_str_to_remove]

        if len(clients) < 2:
            game_state["status"] = "waiting_for_players"
            game_state["message"] = "A player disconnected. Waiting for players to join..."
            game_state["p1_input"] = None
            game_state["p2_input"] = None
            game_state["p1_score"] = 0
            game_state["p2_score"] = 0
            game_state["position"] = 0
            game_state["p1_ownership"] = True
            game_state["shoot_phase"] = False
            game_state["turn"] = "player1" # Reset turn as well
        broadcast_game_state()
    conn.close()

def start_server(host, port):
    """Starts the soccer game server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
    try:
        server_socket.bind((host, port))
        server_socket.listen(2) # Allow up to 2 pending connections
        print(f"Server listening on {host}:{port}")

        player_count = 0
        while player_count < 2:
            conn, addr = server_socket.accept()
            clients.append((conn, addr))
            player_count += 1
            player_id = f"player{player_count}"
            thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
            thread.daemon = True # Allow main program to exit even if threads are running
            thread.start()
            with game_state_lock: # Acquire lock for game_state modification
                game_state["message"] = f"Player {player_count} joined. Waiting for {2 - player_count} more..."
                # No broadcast here, as handle_client sends the initial state to the new client
            print(f"Player {player_count} connected from {addr}")

        with game_state_lock: # Acquire lock for final game_state modification and broadcast
            game_state["status"] = "playing"
            game_state["message"] = "Both players connected! Game starting. Player 1's turn."
            broadcast_game_state() # Broadcast the final starting state to both clients
        print("Both players connected. Game started.")

        # Keep the main thread alive while client threads run
        while True:
            # You can add server-side commands here if needed, e.g., to stop the server
            pass

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Server shutting down.")
        for conn, addr in clients:
            conn.close()
        server_socket.close()

if __name__ == "__main__":
    HOST = '127.0.0.1' # Standard loopback interface address (localhost)
    PORT = 12345       # Arbitrary non-privileged port
    start_server(HOST, PORT)
