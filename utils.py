import os

def prompt():
    print("Welcome to my game\n\n"
          "You must collect all six items before fighting the boss.\n\n"
          "Moves:\t 'go {direction}' (travel north, south, east, or west)\n"
          "         'get {item}' (add nearby item to inventory)\n\n")
    input("Press any key to continue...")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_map():
    print("""
        |Mirror Maze*|
            ||             |Meat Locker* --  |Quicksand Pit*!|
            ||                ||
        |Liminal Space| -- |Bazaar*!|  -- |Dojo!|
            ||
            ||
        |Bat Cavern*!| -- |Volcano*!|

  - * = item, ! = enemy
  - Collect all 6 items before facing the Shadow Man
    """)