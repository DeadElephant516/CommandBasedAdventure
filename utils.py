

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
                    [Mirror Maze]
                          |
[Bazaar] -- [Liminal Space] -- [Bat Cavern] -- [Volcano]
      |                         |
 [Meat Locker]           [Quicksand Pit]
      |
    [Dojo]


  - Collect all 6 items before facing the Shadow Man
    """)
