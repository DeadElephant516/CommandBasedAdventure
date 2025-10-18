import os
import random
import utils
from combat import battle
import items
import use
from data import rooms,player,enemies,inventory,message,healing_items,current_room,previous_room


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
                if enemy_name == "shadow man" and "crystal" not in inventory:
                    print(f"The {enemy_name} blocks your path your are not ready to fight this battle yet\nYou should explore more")
                    current_room = previous_room
                else:
                    result = battle(player, enemy_name, enemies[enemy_name], inventory)
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
        message = use.use_item(player,inventory,item_name)
        print(message)

    #EQUIP-UNEQUIP
    elif command.startswith("equip "):
        item_name = command.split(" ",1)[1]
        message = use.equip_item(player,inventory,item_name)
        print(message)
        print(player)
    elif command.startswith("unequip "):
        item_name = command.split(" ",1)[1]
        message = use.unequip_item(player,inventory,item_name)
        print(message)
        print(player)

    # Help
    elif command in ("help", "?"):
        message = "Commands: go north/south/east/west, get {item},attack,map,inventory, equip {item}, unequip {item}, quit"

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
