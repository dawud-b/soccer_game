# soccer_game.py
# This file contains the core game logic for the soccer game.
from Field_Output_test import print_field

# valid inputs
SHOOTING_INPUTS = ("4", "5", "6")
PASSING_INPUTS = ("1", "2", "3")

# valid values
SHOOTING_VALUES = (4, 5, 6)
PASSING_VALUES = (1, 2, 3)

def select_position_logic(value_str):
  """
  Validates a player's input string and returns its integer value.
  This version is for server-side logic, not for direct user input.
  Returns None if input is invalid.
  """
  if (value_str in SHOOTING_INPUTS) or (value_str in PASSING_INPUTS):
    return int(value_str)
  return None

def check_penalty(p1_ownership, shoot_phase, p1_input, p2_input, position):
  """
  Checks for penalties based on player inputs and game phase.
  Returns updated ownership, position, and a penalty message if applicable.
  """
  penalty_message = ""
  # if its not the shooting phase, the player who has ownership of the ball cannot use 4,5,6 else a penalty occured
  # penalty changes ownership and shooting round begins
  if not shoot_phase:
    if (p1_input not in PASSING_VALUES) and p1_ownership:
      position = 3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P1 tried to shoot!"
    elif (p2_input not in PASSING_VALUES) and (not p1_ownership):
      position = -3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P2 tried to shoot!"
  # if shooting phase, shooting player cannot use passing values
  else:
    if (p1_input not in SHOOTING_VALUES) and p1_ownership:
      position = 3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P1 tried to pass!"
    elif (p2_input not in SHOOTING_VALUES) and (not p1_ownership):
      position = -3
      p1_ownership = not p1_ownership
      penalty_message = "PENALTY! P2 tried to pass!"
  return p1_ownership, position, penalty_message

from Field_Output_test import print_field

def compare_selections(p1_ownership, shoot_phase, p1_input, p2_input, position):
  print(f"Game Logic: P1: {p1_input}, P2: {p2_input}")

  if p1_input == p2_input:
    p1_ownership = not p1_ownership
  elif p1_ownership:
    position -= 1
  else:
    position += 1

  p1_ownership, position, penalty_message = check_penalty(p1_ownership, shoot_phase, p1_input, p2_input, position)

  if (position == 3 and not p1_ownership) or (position == -3 and p1_ownership):
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
  print_field(p1_row, p2_row, col=position, p1_owner=p1_ownership)

  return p1_ownership, shoot_phase, position, penalty_message

def reset_game_logic():
  """
  Resets the core game state variables to their initial values.
  Returns a tuple of initial game state: (p1_ownership, shoot_phase, p1_score, p2_score, position)
  """
  p1_ownership = True
  shoot_phase = False
  p1_score = 0
  p2_score = 0
  position = 0
  
  return p1_ownership, shoot_phase, p1_score, p2_score, position

