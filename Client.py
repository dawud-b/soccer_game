import socket
import json
import sys
import os
from Field_Output_test import print_field
import time
from Soccer_Game import solo_mode

valid_inputs = ("1", "2", "3", "4", "5", "6")

def print_menu():
  print("#### Soccer Game Menu ####\n")
  print("1. Solo Mode")
  print("2. Multiplayer Mode")
  print("3. Exit\n")
  print("##########################\n")

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

    print(f"Player 1: {state['p1_score']} {'(You)' if p1_is_you else ''} | Player 2: {state['p2_score']} {'(You)' if p2_is_you else ''}")
    print(f"Position: {state['position']}")
    print(f"Ball Ownership: {'Player 1' if state['p1_ownership'] else 'Player 2'}")
    # print(f"Game Phase: {'Shooting' if state['shoot_phase'] else 'Passing'}")
    print(f"\n--- {state['message']} ---\n")

    # Finds the row of the player (1-3, if 4-6 just subtract 3)
    # Player 1:
    if state['p1_input'] is None:
        p1_row = 2 # middle row
    else:
        p1_row = state['p1_input']
    if p1_row > 3:
        p1_row = p1_row - 3
    # Player 2:
    if state['p2_input'] is None:
        p2_row = 2 # middle row
    else:
        p2_row = state['p2_input']
    if p2_row > 3:
        p2_row = p2_row - 3

    # Update Players: Player 1's screen
    if p1_is_you and state['p1_ownership'] and state['turn']=="player2":  # p1 owns, p2 move
        p2_row = state['p2_row']
    elif p1_is_you:
        p1_row = state['p1_row']
        p2_row = state['p2_row']

    # # Update Players: Player 2's screen
    if p2_is_you and not state['p1_ownership'] and state['turn']=="player1":  # p2 owns, p1 move
        p1_row = state['p1_row']
    elif p2_is_you:
        p1_row = state['p1_row']
        p2_row = state['p2_row']

    ### Print Players and visual field ###
    has_ball = (state['p1_ownership'] and p1_is_you) or (not state['p1_ownership'] and p2_is_you)
    print_field(col=state['position'], p1_owner=state['p1_ownership'], p1_row=p1_row, p2_row=p2_row)

    if state["status"] == "finished":
        print("\n--- GAME OVER ---")
        print("Type 'reset_game' to play again, or 'exit' to quit.")
    elif state["turn"] == client_player_id:
        print("It's YOUR turn!\nType 1, 2, 3 to pass or 4, 5, 6 to shoot.")
    else:
        print(f"It's {state['turn'].upper()}'s turn. Please wait...")


def multiplayer_mode():
    clear_screen()
    print("#### Multiplayer ####\n")
    #################### HOST AND PORT ########################
    host_input = input("Enter the Host IP (or press Enter for localhost): ")
    if host_input == "":
        HOST = '127.0.0.1' # localhost
    else:
        HOST = host_input.strip()
    PORT = 12345
    ###########################################################

    
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))

        print("Waiting for other player to join...")

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
        clear_screen()
    except:
        clear_screen()
        print(f"Connection to IP {HOST} failed.")
        print("Returning to Menu...")
        time.sleep(2)
        return
    finally:
        client_socket.close()

def main():
    # Enter menu:
    clear_screen()
    print_menu()
    while True:
        mode_selection = input("Select a mode (1-3): ")
        if mode_selection == "1":
            solo_mode()
            print_menu()
        elif mode_selection == "2":
            multiplayer_mode()
            print_menu()
        elif mode_selection == "3":
            break
        else:
            print("Invalid Selection. Try again.")
    
    
if __name__ == "__main__":
    main()