import os
import random
import utils
from combat import battle



# --- MAP SETUP (all lowercase for consistency) ---
rooms = {
    "liminal space": {"north": "mirror maze", "south": "bat cavern", "east": "bazaar"},
    "mirror maze": {"south": "liminal space", "item": "robe"},
    "bat cavern": {"north": "liminal space", "east": "volcano", "item": "staff", "enemy" : "bat"},
    "bazaar": {"west": "liminal space", "north": "meat locker", "east": "dojo", "item": "altoids", "enemy" : "rat"},
    "meat locker": {"south": "bazaar", "east": "quicksand pit", "item": "fig", "enemy": "rat"},
    "quicksand pit": {"west": "meat locker", "item": "crystal", "enemy" : "goblin"},
    "volcano": {"west": "bat cavern", "item": "elderberry", "enemy" : "goblin"},
    "dojo": {"west": "bazaar", "enemy": "shadow man"}
}

healing_items = ["fig", "elderberry", "essence of life"]

#PLAYER STATS AND ENEMIES
player = {"hp" : 10, "atk" : 5, "def" : 5, "spd" : 2}
enemies = {
    "bat" : {"hp" : 5, "atk" : 2, "def" : 1, "spd" : 5, "max_dice" : 2},
    "rat" : {"hp": 5, "atk": 2, "def": 3, "spd" : 1, "max_dice" : 2},
    "goblin" : {"hp": 7, "atk": 3, "def": 3, "spd" : 2, "max_dice" : 3},
    "shadow man" : {"hp": 15, "atk" : 10, "def" : 10, "spd" : 5, "max_dice" : 4}
}

# --- PLAYER STATE ---
inventory = []
current_room = "liminal space"
previous_room = ""
message = ""

utils.clear()
utils.prompt()

# --- MAIN GAME LOOP ---
while True:
    utils.clear()
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
        if direction == "back":
            current_room = previous_room

        elif direction in rooms[current_room]:
            previous_room = current_room
            current_room = rooms[current_room][direction]


            #COMBAT CHECK
            if "enemy" in rooms[current_room]:
                enemy_name = rooms[current_room]["enemy"]

                #SHADOW MAN CHECK
                if enemy_name == "shadow man" and "crystal" in inventory:
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

    #ITEM USAGE
    elif command.startswith("use "):
        item_name = command.split(" ", 1)[1]
        if item_name in inventory:
            if item_name in healing_items:
                heal_amount = random.randint(1,4)
                player["hp"] += heal_amount
                if player["hp"] >= 10:
                    player["hp"] = 10
                print(f"You used the {item_name} and heal {heal_amount} current HP: {player["hp"]}")
                inventory.remove(item_name)
            else:
                print(f"You can't use {item_name} now")
        else:
            print(f"You don't have {item_name} in your inventory")

    # Help
    elif command in ("help", "?"):
        message = "Commands: go north/south/east/west, get {item},attack,map,inventory"

    elif command == "map":
        utils.show_map()

    elif command == "inv" or command == "inventory":
        print(inventory)

    # Quit
    elif command in ("quit", "exit"):
        print("Thanks for playing!")
        break


    # Invalid input
    else:
        message = "Invalid command."
