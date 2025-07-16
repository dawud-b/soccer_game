#### Soccer Game ####

# valid inputs
shooting_inputs = ("4", "5", "6")
passing_inputs = ("1", "2", "3")

# valid values
shooting_values = (4, 5, 6)
passing_values = (1, 2, 3)

def select_position(player):
  while(1):
    value = input(f"{player} enter value: ")
    if (value in shooting_inputs) or (value in passing_inputs):
      return int(value)
    print("Invalid Selection")

# if its not the shooting phase, the player who has ownership of the ball cannot use 4,5,6 else a penalty occured
# penalty changes ownership and shooting round begins
def check_penalty(p1_ownership, shoot_phase, p1_input, p2_input, position):
  if not shoot_phase:
    if (p1_input not in passing_values) and p1_ownership:
      position = 3
      p1_ownership = not p1_ownership
      print("PENALTY! P1 tried to shoot!")
    elif (p2_input not in passing_values) and (not p1_ownership):
      position = -3
      p1_ownership = not p1_ownership
      print("PENALTY! P2 tried to shoot!")
  # if shooting phase, shooting player cannot use passing values
  else:
    if (p1_input not in shooting_values) and p1_ownership:
      position = 3
      p1_ownership = not p1_ownership
      print("PENALTY! P1 tried to pass!")
    elif (p2_input not in shooting_values) and (not p1_ownership):
      position = -3
      p1_ownership = not p1_ownership
      print("PENALTY! P2 tried to pass!")
  return p1_ownership, position

def compare_selections(p1_ownership, shoot_phase, p1_input, p2_input, position):
  # Print inputs
  print(f"P1: {p1_input}, P2: {p2_input}")
  
  # compare inputs. If matching ownership changes
  if p1_input == p2_input:
    p1_ownership = not p1_ownership
  elif p1_ownership:
    position -= 1
  else:
    position += 1

  # check for penalty
  p1_ownership, position = check_penalty(p1_ownership, shoot_phase, p1_input, p2_input, position)

  # update shoot_phase
  if (position == 3 and not p1_ownership) or (position == -3 and p1_ownership):
    shoot_phase = True
  else:
     shoot_phase = False

  return p1_ownership, shoot_phase, position


# Initalize values.
def reset():
  # false if p2 has ownership
  p1_ownership = True

  # set if it is a shooting phase
  shoot_phase = False

  p1_score = 0
  p2_score = 0

  # 0 means middle of field. +3 is p1 goal, -3 is p2 goal
  position = 0

  return p1_ownership, shoot_phase, p1_score, p2_score, position

def main():
  # reset / init values
  p1_ownership, shoot_phase, p1_score, p2_score, position = reset()

  print(f"------------------------------------------------------------------\n" +
        f"Position: {position}, Player 1's Ball, Score: {p1_score}:{p2_score}")

  # Begin game
  while(1):
    # First players select value
    p1_input = select_position("Player 1")
    p2_input = select_position("Player 2")

    # check values, update position
    p1_ownership, shoot_phase, position = compare_selections(p1_ownership, shoot_phase, p1_input, p2_input, position)

    # if postion >3 or <-3 then a player scored. Reset position and P2 gains control
    if position > 3:
      print("Player 2 scored!")
      p2_score += 1
      position, shoot_phase, p1_ownership = 0, False, True
    elif position < -3:
      print("Player 1 scored!")
      p1_score += 1
      position, shoot_phase, p1_ownership = 0, False, False

    # First player to 5 scores wins
    if p1_score >= 5:
      print("--- Player 1 Wins! --- ")
      break
    if p2_score >= 5:
      print("--- Player 1 Wins! --- ")
      break
      
    # print results
    if p1_ownership:
      owner = "Player 1"
    else:
      owner = "Player 2"
    print(f"---------------------------------------------------------------------\n" +
          f"Position: {position}, {owner}'s Ball, Score: {p1_score}:{p2_score}, Shooting: {shoot_phase}")


main()
  

