### Soccer Game Field Output ###

def print_space(count):
  for i in range(count):
      print(" ", end='')

def print_field(row, col):
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
    print(" O ", end='')
    print_space(58 - spaces)
    print("|")
    
    # second line
    print("    |   ", end='')
    print_space(spaces)
    print("/|\\", end='')
    print_space(58 - spaces)
    print("|") 

    # third line
    print("+---|   ", end='')
    print_space(spaces)
    print("/ \\", end='')
    print_space(58 - spaces)
    print("|---+")


for i in range(-3, 3):
  print_field(1, i)
  print()