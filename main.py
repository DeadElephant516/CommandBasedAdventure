import os
import random

from combat import battle


def prompt():
    print("Welcome to my game\n\n"
          "You must collect all six items before fighting the boss.\n\n"
          "Moves:\t 'go {direction}' (travel north, south, east, or west)\n"
          "         'get {item}' (add nearby item to inventory)\n\n")
    input("Press any key to continue...")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- MAP SETUP (all lowercase for consistency) ---
rooms = {
    "liminal space": {"north": "mirror maze", "south": "bat cavern", "east": "bazaar"},
    "mirror maze": {"south": "liminal space", "item": "crystal"},
    "bat cavern": {"north": "liminal space", "east": "volcano", "item": "staff", "enemy" : "bat"},
    "bazaar": {"west": "liminal space", "north": "meat locker", "east": "dojo", "item": "altoids", "enemy" : "rat"},
    "meat locker": {"south": "bazaar", "east": "quicksand pit", "item": "fig", "enemy": "rat"},
    "quicksand pit": {"west": "meat locker", "item": "robe", "enemy" : "goblin"},
    "volcano": {"west": "bat cavern", "item": "elderberry", "enemy" : "goblin"},
    "dojo": {"west": "bazaar", "enemy": "shadow man"}
}

#PLAYER STATS AND ENEMIES
player = {"hp" : 10, "atk" : 5, "def" : 5, "spd" : 2}
enemies = {
    "bat" : {"hp" : 5, "atk" : 3, "def" : 1, "spd" : 3},
    "rat" : {"hp": 5, "atk": 3, "def": 3, "spd" : 1},
    "goblin" : {"hp": 7, "atk": 5, "def": 3, "spd" : 2},
    "shadow man" : {"hp": 15, "atk" : 10, "def" : 10, "spd" : 5}
}

# --- PLAYER STATE ---
inventory = []
current_room = "liminal space"
previous_room = ""
message = ""

clear()
prompt()

# --- MAIN GAME LOOP ---
while True:
    clear()
    print(f"You are in {current_room.title()}")
    print(f"Inventory: {inventory}")
    print("-" * 27)

    # Display last move result/message
    if message:
        print(message)
        message = ""

    # Show nearby item
    if "item" in rooms[current_room]:
        nearby_item = rooms[current_room]["item"]
        article = "an" if nearby_item[0].lower() in "aeiou" else "a"
        print(f"You see {article} {nearby_item}.")


    # Player input
    command = input("\nEnter command:\n> ").strip().lower()

    # Movement
    if command.startswith("go "):
        direction = command.split(" ")[1]
        if direction in rooms[current_room]:
            previous_room = current_room
            current_room = rooms[current_room][direction]

            #COMBAT CHECK
            if "enemy" in rooms[current_room]:
                enemy_name = rooms[current_room]["enemy"]

                #SHADOW MAN CHECK
                if enemy_name == "shadow man" and len(inventory) < 6:
                    print(f"The {enemy_name} blocks your path your are not ready to fight this battle yet\nYou should explore more")
                    current_room = previous_room
                else:
                    result = battle(player, enemy_name, enemies[enemy_name])
                    if result == False:
                        print("Game Over")
                        break
                    elif result == "fled":
                        print("You return to the previous room to regroup.")
                        current_room = previous_room
                    else:
                        del rooms[current_room]["enemy"]

        else:
            message = "You can't go that way."

    # Item pickup
    elif command.startswith("get "):
        item_name = command.split(" ", 1)[1]
        if "item" in rooms[current_room] and item_name == rooms[current_room]["item"]:
            inventory.append(item_name)
            del rooms[current_room]["item"]
            message = f"You picked up the {item_name}."
        else:
            message = "There's nothing like that here."

    # Help
    elif command in ("help", "?"):
        message = "Commands: go north/south/east/west, get {item}"

    # Quit
    elif command in ("quit", "exit"):
        print("Thanks for playing!")
        break

    # Invalid input
    else:
        message = "Invalid command."
