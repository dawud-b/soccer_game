### Soccer Game Field Output ###

def print_space(count):
  for i in range(count):
      print(" ", end='')

def row_preprint(row, part):
  match row:
    case 1:
      if (part == 1 or part == 2): print("    | ", end='')
      else: print("+---| ", end='')
    case 2:
      print("|   | ", end='')
    case 3:
      if (part == 2 or part == 3): print("    | ", end='')
      else: print("+---| ", end='')

def row_postprint(row, part):
  match row:
    case 1:
      if (part == 1 or part == 2): print(" |")
      else: print(" |---+")
    case 2:
      print(" |   |")
    case 3:
      if (part == 2 or part == 3): print(" |")
      else: print(" |---+")

# prints one player in its locations.
def print_player(p1_owner, col, row, player):
  spaces = (col + 3) * 8 + 3

  # first line
  row_preprint(row, 1)
  print_space(spaces)
  if player == 1:
    print(" O        ", end='')
  else:
    print("        O ", end='')
  print_space(52 - spaces)
  row_postprint(row, 1)
    
  # second line
  row_preprint(row, 2)
  print_space(spaces)
  if player == 1:
    print("/|\\       ", end='')
  else:
    print("       /|\\", end='')
  print_space(52 - spaces)
  row_postprint(row, 2)

  # third line
  row_preprint(row, 3)
  print_space(spaces)
  if p1_owner and player == 1:
    print("/ \\*      ", end='')
  elif player == 1:
    print("/ \\       ", end='')
  elif not p1_owner:
    print("      */ \\", end='')
  else:
    print("       / \\", end='')
  print_space(52 - spaces)
  row_postprint(row, 3)

# prints both players at same location.
def print_both_players(p1_owner, col, row):
  spaces = (col + 3) * 8 + 3

  # first line
  row_preprint(row, 1)
  print_space(spaces)
  print(" O      O ", end='')
  print_space(52 - spaces)
  row_postprint(row, 1)
    
  # second line
  row_preprint(row, 2)
  print_space(spaces)
  print("/|\\    /|\\", end='')
  print_space(52 - spaces)
  row_postprint(row, 2)

  # third line
  row_preprint(row, 3)
  print_space(spaces)
  print("/ \\", end='')
  if p1_owner:
    print("*   / \\", end='')
  else:
    print("   */ \\", end='')
  print_space(52 - spaces)
  row_postprint(row, 3)


def print_field(p1_row, p2_row, col, p1_owner):
  print("    +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
  
  # 61 total spaces between each | !!!!

  if p1_row == 1 and p2_row == 1:
    print_both_players(p1_owner, col, p1_row)
  elif p1_row == 1:
    print_player(p1_owner, col, p1_row, player=1)
  elif p2_row == 1:
    print_player(p1_owner, col, p2_row, player=2)
  else:
    print ("    |                                                                |\n"
          +"    |                                                                |\n"
          +"+---|                                                                |---+")

  if p1_row == 2 and p2_row == 2:
    print_both_players(p1_owner, col, p1_row)
  elif p1_row == 2:
    print_player(p1_owner, col, p1_row, player=1)
  elif p2_row == 2:
    print_player(p1_owner, col, p2_row, player=2)
  else:
    print ("|   |                                                                |   |\n"
          +"|   |                                                                |   |\n"
          +"|   |                                                                |   |")

  if p1_row == 3 and p2_row == 3:
    print_both_players(p1_owner, col, p1_row)
  elif p1_row == 3:
    print_player(p1_owner, col, p1_row, player=1)
  elif p2_row == 3:
    print_player(p1_owner, col, p2_row, player=2)
  else:
    print ("+---|                                                                |---+\n"
          +"    |                                                                |\n"
          +"    |                                                                |")

  print("    +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
    
    
# for j in range (1, 4):
#   for i in range(-3, 4):
#     print_field(j, i, True)
#     print()
#     print_field(j, i, False)
#     print()

for i in range(-3, 4):
  print_field(p1_row=1, p2_row=2, col=i, p1_owner=True)
  print_field(p1_row=1, p2_row=3, col=i, p1_owner=True)
  print_field(p1_row=2, p2_row=2, col=i, p1_owner=True)
  print_field(p1_row=2, p2_row=1, col=i, p1_owner=True)