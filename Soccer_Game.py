# soccer_game.py
# This file contains the core game logic for the soccer game.
# Author: Dawud Benedict

from Field_Output_test import print_field
import os
import random
import time

# valid inputs
SHOOTING_INPUTS = ("4", "5", "6")
PASSING_INPUTS = ("1", "2", "3")

# valid values
SHOOTING_VALUES = (4, 5, 6)
PASSING_VALUES = (1, 2, 3)

#### Player 1 Goal at -3, P1 shoots at +3 ####
#### Player 2 Goal at +3, P2 shoots at -3 ####


# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Validates a player's input string and returns its integer value.
# This version is for server-side logic, not for direct user input.
# Returns None if input is invalid.
def select_position_logic(value_str):
  if (value_str in SHOOTING_INPUTS) or (value_str in PASSING_INPUTS):
    return int(value_str)
  return None


# Checks for penalties based on player inputs and game phase.
# Returns updated ownership, position, and a penalty message if applicable.
def check_penalty(p1_ownership, shoot_phase, p1_input, p2_input, position):
  penalty_message = ""
  # if not the shooting phase, ball owner cannot use 4,5,6 else a penalty occurs
  # penalty changes ownership and shooting round begins
  if not shoot_phase:
    if (p1_input not in PASSING_VALUES) and p1_ownership:
      position = -3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P1 tried to shoot!"
    elif (p2_input not in PASSING_VALUES) and (not p1_ownership):
      position = 3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P2 tried to shoot!"
  # if shooting phase, shooting player cannot use passing values
  else:
    if (p1_input not in SHOOTING_VALUES) and p1_ownership:
      position = -3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P1 tried to pass!"
    elif (p2_input not in SHOOTING_VALUES) and (not p1_ownership):
      position = 3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P2 tried to pass!"
  return p1_ownership, position, penalty_message

from Field_Output_test import print_field

def compare_selections(p1_ownership, shoot_phase, p1_input, p2_input, position):
  # print(f"Game Logic: P1: {p1_input}, P2: {p2_input}")

  if p1_input == p2_input:
    p1_ownership = not p1_ownership
  elif p1_ownership:
    position += 1
  else:
    position -= 1

  p1_ownership, position, penalty_message = check_penalty(p1_ownership, shoot_phase, p1_input, p2_input, position)

  if (position == -3 and not p1_ownership) or (position == 3 and p1_ownership):
    shoot_phase = True
  else:
    shoot_phase = False

  # VISUAL OUTPUT
  p1_row = p1_input
  if p1_row > 3:
    p1_row = p1_row - 3
  p2_row = p2_input
  if p2_row > 3:
    p2_row = p2_row - 3
  # print_field(p1_row, p2_row, col=position, p1_owner=p1_ownership)

  return p1_ownership, shoot_phase, position, penalty_message


# Resets the core game state variables to their initial values.
# Returns a tuple of initial game state: (p1_ownership, shoot_phase, p1_score, p2_score, position)
def reset_game_logic():
 
  p1_ownership = True
  shoot_phase = False
  p1_score = 0
  p2_score = 0
  position = 0
  
  return p1_ownership, shoot_phase, p1_score, p2_score, position

#### Solo Mode ####
def solo_mode():
  clear_screen()
  print("#### SOLO MODE ####")
  print("You're Player 1.")
  print("First to 5 goals wins!\n")
  input("Press Enter to start. ")

  p1_ownership, shoot_phase, p1_score, p2_score, position = reset_game_logic()

  p1_row = 2
  p2_row = 2

  while p1_score < 5 and p2_score < 5:
    clear_screen()
    print(f"Score: P1 {p1_score} - {p2_score} P2")
    print(f"Position: {position} | Ball Owner: {'You' if p1_ownership else 'P2'}\n")
    # print(f"Game Phase: {'Shooting' if state['shoot_phase'] else 'Passing'}")
    print_field(p1_row, p2_row, col=position, p1_owner=p1_ownership)
    print()
    
    # Player 1 selection
    while True:
      user_input = input("It's YOUR turn!\nEnter your move (Type 'exit' to quit): ")
      if user_input == "exit":
        clear_screen()
        return
      if user_input in PASSING_INPUTS or user_input in SHOOTING_INPUTS:
        p1_input = int(user_input)
        break
      else:
        print("Invalid Input. Try again.")

    # Bot selection
    if shoot_phase:
      p2_input = random.choice(SHOOTING_VALUES)
    else:
      p2_input = random.choice(PASSING_VALUES)

    # Compare Values
    p1_ownership, shoot_phase, position, penalty_message = compare_selections(p1_ownership, shoot_phase, p1_input, p2_input, position)

    if penalty_message != "":
      print("\n------------------------------------")
      print(penalty_message)
      time.sleep(1)

    # Update player position
    p1_row = p1_input if p1_input <= 3 else p1_input - 3
    p2_row = p2_input if p2_input <= 3 else p2_input - 3

    # Check Score
    if position < -3:
      p2_score += 1
      print("\n------------------------------------")
      print("      Player 2 scored a goal!")
      p1_ownership, shoot_phase, _, _, position = reset_game_logic()
      p1_row = 2
      p2_row = 2
      time.sleep(2)
    elif position > 3:
      p1_score += 1
      print("\n------------------------------------")
      print("        You scored a goal!")
      p1_ownership, shoot_phase, _, _, position = reset_game_logic()
      p1_row = 2
      p2_row = 2
      time.sleep(2)

  if p1_score > p2_score:
    print("\n---------------------")
    print("     You Win!\n")
  else:
    print("\n---------------------")
    print("     You Lose :(\n")
  input("Press Enter to return to menu. ")
  clear_screen()
