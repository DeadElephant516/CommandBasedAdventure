import os
import random
import utils
from combat import battle
import items
import use
from game import  game
from classes import character_classes

rooms = game["rooms"]
inventory = game["inventory"]
player = game["player"]
enemies = game["enemies"]
current_room = game["current_room"]
previous_room = game["previous_room"]
message = game["message"]



utils.clear()
utils.prompt()

#CLASS SELECTION
utils.clear()
print("CHOOSE YOUR ORIGIN\n")
print("In this wretched place, your past defines your survival:\n")
for class_name, class_data in character_classes.items():
    print(f"- {class_name.upper()}: {class_data['description']}")
while True:
    chosen_class = input("\nWhat is your origin? ").strip().lower()
    if chosen_class in character_classes:
        class_data = character_classes[chosen_class]

        # Apply stats using our clean function
        player = utils.apply_class_stats(player, class_data)

        # Add starting gear to inventory
        for item in class_data["starting_gear"]:
            inventory[item] = inventory.get(item, 0) + 1

        print(f"\nYou are {chosen_class.upper()}.")
        print(f"HP:{player['hp']} ATK:{player['atk']} DEF:{player['def']} SPD:{player['spd']}")
        print(f"Combat skills: {', '.join(player['combat_actions'])}")
        input("\nPress any key to face what awaits...")
        break
    else:
        print("Unknown origin. Choose:", list(character_classes.keys()))

# --- MAIN GAME LOOP ---
while True:
    utils.clear()
    available_exits = ", ".join(rooms[current_room]["exits"].keys())
    print(f"You are in {current_room.title()}\nExits: {available_exits}")
    print(f"Inventory: {inventory}")
    print("-" * 27)

    # Display last move result/message
    if message:
        print(message)
        message = ""

    # Show nearby item
    if "items" in rooms[current_room] and rooms[current_room]["items"]:
        nearby_items = rooms[current_room]["items"]
        for nearby_item in nearby_items:
            article = "an" if nearby_item[0].lower() in "aeiou" else "a"
            print(f"You see {article} {nearby_item}.")


    # Player input
    #command = input("\nEnter command:\n> ").strip().lower()
    command = ' '.join(input().strip().lower().split())

    # Movement
    if command.startswith("go "):
        direction = command.split(" ")[1]
        if direction == "back":
            if previous_room != "":
                current_room = previous_room

        elif direction in rooms[current_room]["exits"]:
            previous_room = current_room
            current_room = rooms[current_room]["exits"][direction]


        else:
            message = "You can't go that way."

    # Item pickup
    elif command.startswith("get ") or command.startswith("take "):
        item_name = command.split(" ", 1)[1]
        message = use.pick_up_item(rooms,current_room,item_name,inventory)


    #ITEM USAGE
    elif command.startswith("use "):
        item_name = command.split(" ", 1)[1]
        message = use.use_item(player,inventory,item_name)
        print(message)

    #EQUIP-UNEQUIP
    elif command.startswith("equip "):
        item_name = command.split(" ",1)[1]
        message = use.equip_item(player,inventory,item_name)
        #print(message)
        print(player)
    elif command.startswith("unequip "):
        item_name = command.split(" ",1)[1]
        message = use.unequip_item(player,inventory,item_name)
        #print(message)
        print(player)

    # Help
    elif command in ("help", "?"):
        message = "Commands: go north/south/east/west, use {item}, get {item},map,inventory, equip {item}, unequip {item}, quit, Combat: attack, bluff, guard, flee, use {item}"

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



    # COMBAT CHECK
    if "enemy" in rooms[current_room]:
        enemy_name = rooms[current_room]["enemy"]

        # SHADOW MAN CHECK
        if enemy_name == "shadow man" and "crystal" not in inventory:
            print(
                f"The {enemy_name} blocks your path your are not ready to fight this battle yet\nYou should explore more")
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

    game["current_room"] = current_room
    game["previous_room"] = previous_room
    game["message"] = message
    game["inventory"] = inventory
    game["player"] = player
    game["rooms"] = rooms
