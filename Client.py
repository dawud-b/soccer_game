import socket
import json
import sys
import os
from Field_Output_test import print_field

valid_inputs = ("1", "2", "3", "4", "5", "6")

# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def receive_game_state(sock):
    try:
        length_bytes = sock.recv(4)
        if not length_bytes:
            return None
        message_length = int.from_bytes(length_bytes, 'big')
        received_data = b''
        while len(received_data) < message_length:
            chunk = sock.recv(message_length - len(received_data))
            if not chunk:
                return None
            received_data += chunk
        return json.loads(received_data.decode('utf-8'))
    except:
        return None

def display_game_state(state, client_player_id):
    clear_screen()
    print("#### Soccer Game ####\n")
    print(f"Your Player ID: {client_player_id.upper()}\n")

    if state["status"] == "waiting_for_players":
        print(f"STATUS: {state['message']}\n")
        print("Waiting for another player to join...")
        return

    p1_is_you = (client_player_id == "player1")
    p2_is_you = (client_player_id == "player2")

    print(f"Score: Player 1: {state['p1_score']} {'(You)' if p1_is_you else ''} | Player 2: {state['p2_score']} {'(You)' if p2_is_you else ''}")
    print(f"Position: {state['position']}")
    print(f"Ball Ownership: {'Player 1' if state['p1_ownership'] else 'Player 2'}")
    print(f"Game Phase: {'Shooting' if state['shoot_phase'] else 'Passing'}")
    print(f"\n--- {state['message']} ---\n")

# Finds the row of the player (1-3, if 4-6 just subtract 3)
    if state['p1_input'] is None:
        p1_row = 2 # middle row
    else:
        p1_row = state['p1_input']
    if p1_row > 3:
        p1_row = p1_row - 3

    if state['p2_input'] is None:
        p2_row = 2 # middle row
    else:
        p2_row = state['p2_input']
    if p2_row > 3:
        p2_row = p2_row - 3

    if p1_is_you and state['p1_ownership'] and state['turn']=="player1":        # p1 owns. First move. Let p1 see new p1 and prev p2
        p2_row = state['p2_row']
    elif p1_is_you and state['p1_ownership']:                                   # p1 owns. Second move. Let p1 see p1 prev and new p2.
        p1_row = state['p1_row']
    elif p1_is_you and not state['p1_ownership'] and state['turn']=="player2":  # p2 owns. First move. Let p1 see prev p2 and prev p1
        p2_row = state['p2_row']
        p1_row = state['p1_row']
    #                                                                           # p2 owns. Second move. Let p1 see p1 and p2 (No change)

    # same for p2
    if p2_is_you and state['p1_ownership'] and state['turn']=="player1":        # p1 owns. First move. Let p2 see prev p1 and prev p2
        p2_row = state['p2_row']
        p1_row = state['p1_row']
    elif p2_is_you and not state['p1_ownership'] and state['turn']=="player1":  # p2 owns. Second move. Let p2 see new p1 and prev p2.
        p2_row = state['p2_row']
    elif p2_is_you and not state['p1_ownership'] and state['turn']=="player2":  # p2 owns. First move. Let p2 see prev p1 and new p2
        p1_row = state['p1_row']
    #                                                                           # p1 owns. Second move. Let p2 see p1 and p2 (No change)

    # Print visual field
    has_ball = (state['p1_ownership'] and p1_is_you) or (not state['p1_ownership'] and p2_is_you)
    print_field(col=state['position'], p1_owner=state['p1_ownership'], p1_row=p1_row, p2_row=p2_row)

    if state["status"] == "finished":
        print("\n--- GAME OVER ---")
        print("Type 'reset_game' to play again, or 'exit' to quit.")
    elif state["turn"] == client_player_id:
        print("It's YOUR turn!\nValid inputs: Pass (1, 2, 3) | Shoot (4, 5, 6)")
    else:
        print(f"It's {state['turn'].upper()}'s turn. Please wait...")

def main():
    # HOST = '127.0.0.1'
    HOST = '10.48.190.208'
    #################### HOST AND PORT ########################
    PORT = 12345
    ###########################################################
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        initial_state = receive_game_state(client_socket)
        if not initial_state:
            return

        client_player_id = initial_state.get("your_player_id")
        if not client_player_id:
            return

        # Main Loop
        while True:
            state = receive_game_state(client_socket)
            if state is None:
                break

            # display GUI
            display_game_state(state, client_player_id)

            if state["status"] == "finished":
                user_action = input("Game over. Type 'reset_game' to play again or 'exit': ").strip().lower()
                if user_action == "reset_game":
                    client_socket.sendall(len("reset_game").to_bytes(4, 'big'))
                    client_socket.sendall("reset_game".encode('utf-8'))
                    continue
                elif user_action == "exit":
                    break
                else:
                    continue

            if state["turn"] == client_player_id and state["status"] == "playing":
                while True:
                    move = input("Enter your move (1-6): ").strip()
                    if move in ["1", "2", "3", "4", "5", "6"]:
                        try:
                            client_socket.sendall(len(move).to_bytes(4, 'big'))
                            client_socket.sendall(move.encode('utf-8'))
                            break
                        except:
                            break
                    else:
                        print("Invalid input.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()