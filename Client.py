import socket
import json
import sys
import os

# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def receive_game_state(sock):
    """Receives and decodes the game state from the server."""
    try:
        # Receive 4-byte length of the incoming message
        length_bytes = sock.recv(4)
        if not length_bytes:
            print("Client: Server disconnected (no length bytes).")
            return None # Server disconnected

        message_length = int.from_bytes(length_bytes, 'big')
        received_data = b''
        while len(received_data) < message_length:
            chunk = sock.recv(message_length - len(received_data))
            if not chunk:
                print("Client: Server disconnected (incomplete data).")
                return None # Server disconnected
            received_data += chunk

        if not received_data:
            print("Client: Received empty data.")
            return None # Server disconnected

        return json.loads(received_data.decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode game state from server. JSON Error: {e}")
        print(f"Problematic data (raw): {received_data}")
        print(f"Problematic data (decoded): {received_data.decode('utf-8', errors='ignore')}") # Use errors='ignore' to prevent decode errors here
        return None
    except Exception as e:
        print(f"Error receiving game state: {e}")
        return None

def display_game_state(state, client_player_id):
    """Clears screen and displays the current game state to the client."""
    clear_screen()
    print("#### Soccer Game ####\n")
    print(f"Your Player ID: {client_player_id.upper()}\n")

    if state["status"] == "waiting_for_players":
        print(f"STATUS: {state['message']}\n")
        print("Waiting for another player to join...")
        return

    p1_is_you = (client_player_id == "player1")
    p2_is_you = (client_player_id == "player2")

    p1_score_display = f"Player 1 Score: {state['p1_score']}"
    p2_score_display = f"Player 2 Score: {state['p2_score']}"

    if p1_is_you:
        p1_score_display += " (You)"
    elif p2_is_you:
        p2_score_display += " (You)"

    print(f"Score: {p1_score_display} | {p2_score_display}")
    print(f"Position: {state['position']}")

    owner_display = "Player 1" if state['p1_ownership'] else "Player 2"
    print(f"Ball Ownership: {owner_display}")

    phase_display = "Shooting Phase" if state['shoot_phase'] else "Passing Phase"
    print(f"Game Phase: {phase_display}")

    print(f"\n--- {state['message']} ---\n")

    if state["status"] == "finished":
        print("\n--- GAME OVER ---")
        print(state["message"])
        print("Type 'reset_game' to play again, or 'exit' to quit.")
    elif state["turn"] == client_player_id:
        print("It's YOUR turn!")
        print("Valid inputs: Pass (1, 2, 3) | Shoot (4, 5, 6)")
    else:
        print(f"It's {state['turn'].upper()}'s turn. Please wait...")

def main():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345        # The port used by the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Receive initial game state which now includes 'your_player_id'
        initial_state = receive_game_state(client_socket)
        if not initial_state:
            print("Failed to receive initial game state. Exiting.")
            return

        client_player_id = initial_state.get("your_player_id")
        if not client_player_id:
            print("Error: Server did not provide a player ID. Exiting.")
            return

        while True:
            current_game_state = receive_game_state(client_socket)
            if current_game_state is None:
                print("Server disconnected. Exiting game.")
                break

            display_game_state(current_game_state, client_player_id)

            if current_game_state["status"] == "finished":
                user_action = input("Game over. Type 'reset_game' to play again or 'exit' to quit: ").strip().lower()
                if user_action == "reset_game":
                    client_socket.sendall(len("reset_game").to_bytes(4, 'big'))
                    client_socket.sendall("reset_game".encode('utf-8'))
                    continue
                elif user_action == "exit":
                    break
                else:
                    print("Invalid input. Please type 'reset_game' or 'exit'.")
                    continue

            if current_game_state["turn"] == client_player_id and current_game_state["status"] == "playing":
                while True:
                    player_input = input("Enter your move (1-6): ").strip()
                    if player_input in ["1", "2", "3", "4", "5", "6"]:
                        try:
                            # Send 4-byte length of the input string
                            client_socket.sendall(len(player_input).to_bytes(4, 'big'))
                            client_socket.sendall(player_input.encode('utf-8'))
                            break # Input sent, break from inner loop
                        except Exception as e:
                            print(f"Error sending data: {e}")
                            break # Break from inner loop, will lead to outer loop break
                    else:
                        print("Invalid input. Please enter a number between 1 and 6.")
            else:
                # Not current player's turn, just wait for next state update
                pass

    except ConnectionRefusedError:
        print(f"Connection refused. Make sure the server is running at {HOST}:{PORT}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Client shutting down.")
        client_socket.close()

if __name__ == "__main__":
    main()
