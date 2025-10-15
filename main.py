import os

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
    "bat cavern": {"north": "liminal space", "east": "volcano", "item": "staff"},
    "bazaar": {"west": "liminal space", "north": "meat locker", "east": "dojo", "item": "altoids"},
    "meat locker": {"south": "bazaar", "east": "quicksand pit", "item": "fig"},
    "quicksand pit": {"west": "meat locker", "item": "robe"},
    "volcano": {"west": "bat cavern", "item": "elderberry"},
    "dojo": {"west": "bazaar", "boss": "shadow man"}
}

# --- PLAYER STATE ---
inventory = []
current_room = "liminal space"
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

    # Boss encounter
    if "boss" in rooms[current_room]:
        boss = rooms[current_room]["boss"]
        if len(inventory) < 6:
            print(f"You lost a fight with {boss}.")
            break
        else:
            print(f"You defeated {boss} and won the game!")
            break

    # Player input
    command = input("\nEnter command:\n> ").strip().lower()

    # Movement
    if command.startswith("go "):
        direction = command.split(" ")[1]
        if direction in rooms[current_room]:
            current_room = rooms[current_room][direction]
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
