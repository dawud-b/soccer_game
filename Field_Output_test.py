### Soccer Game Field Output ###

def print_space(count):
  for i in range(count):
      print(" ", end='')

def print_field(row, col, p1_owner):
  print("    +–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
  

  # 61 total spaces between each | !!!!

  if row != 1:
    print ("    |                                                               |"
          +"    |                                                               |"
          +"+---|                                                               |---+")
  else:
    spaces = (col + 3) * 8
    
    # first line
    print("    |   ", end='')
    print_space(spaces)
    print(" O      O ", end='')
    print_space(50 - spaces)
    print("|")
    
    # second line
    print("    |   ", end='')
    print_space(spaces)
    print("/|\\    /|\\", end='')
    print_space(50 - spaces)
    print("|") 

    # third line
    print("+---|   ", end='')
    print_space(spaces)
    print("/ \\", end='')
    if p1_owner:
      print("*   / \\", end='')
    else:
      print("   */ \\", end='')
    print_space(50 - spaces)
    print("|---+")


for i in range(-3, 3):
  print_field(1, i, True)
  print()

for i in range(-3, 3):
  print_field(1, i, False)
  print()