### Soccer Game Field Output ###

def print_space(count):
  for i in range(count):
      print(" ", end='')

def row_preprint(row, part):
  match row:
    case 1:
      if (part == 1 or part == 2): print("    |   ", end='')
      else: print("+---|   ", end='')
    case 2:
      print("|   |   ")
    case 3:
      if (part == 2 or part == 3): print("    |   ", end='')
      else: print("+---|   ", end='')

def row_postprint(row, part):
  match row:
    case 1:
      if (part == 1 or part == 2): print("|")
      else: print("|---+")
    case 2:
      print("|   |")
    case 3:
      if (part == 2 or part == 3): print("|")
      else: print("|---+")



def print_players(p1_owner, col, row):
  spaces = (col + 3) * 8 + 3

  # first line
  row_preprint(row, 1)
  print_space(spaces)
  print(" O      O ", end='')
  print_space(50 - spaces)
  row_postprint(row, 1)
    
  # second line
  row_preprint(row, 2)
  print_space(spaces)
  print("/|\\    /|\\", end='')
  print_space(50 - spaces)
  row_postprint(row, 2)

  # third line
  row_preprint(row, 3)
  print_space(spaces)
  print("/ \\", end='')
  if p1_owner:
    print("*   / \\", end='')
  else:
    print("   */ \\", end='')
  print_space(50 - spaces)
  row_postprint(row, 3)


def print_field(row, col, p1_owner):
  print("    +–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
  
  # 61 total spaces between each | !!!!

  if row != 1:
    print ("    |                                                               |\n"
          +"    |                                                               |\n"
          +"+---|                                                               |---+")
  else:
    print_players(p1_owner, col, row)

  if row != 2:
    print ("|   |                                                               |   |\n"
          +"|   |                                                               |   |\n"
          +"|   |                                                               |   |")
  else:
    print_players(p1_owner, col, row)

  if row != 3:
    print ("+---|                                                               |---+\n"
          +"    |                                                               |\n"
          +"    |                                                               |")
  else:
    print_players(p1_owner, col, row)

  print("    +–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
    
    
  

for i in range(-3, 3):
  print_field(3, i, True)
  print()