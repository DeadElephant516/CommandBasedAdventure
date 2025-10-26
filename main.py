import os
import random
import utils
from combat_v2 import battle
import items
import use
from game import  game
from classes import character_classes


rooms = game["rooms"]
inventory = game["inventory"]
enemies = game["enemies"]
current_room = game["current_room"]
previous_room = game["previous_room"]
message = game["message"]



utils.clear()
utils.prompt()

#CLASS SELECTION
utils.clear()
utils.class_selection(game,game["inventory"],character_classes)
player = game["player"]
utils.clear()

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
    msg = utils.show_nearby_item(rooms,current_room)
    print(msg)


    # Player input
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
        message = utils.show_map()

    elif command == "inv" or command == "inventory":
        print(inventory)

    # Quit
    elif command in ("quit", "exit"):
        print("Thanks for playing!")
        break

    # Invalid input
    else:
        message = "Invalid command."


    # COMBAT CHECK (only if player moved or took action)
    if "enemy" in rooms[current_room]:
        enemy_name = rooms[current_room]["enemy"]

        # SHADOW MAN CHECK
        if enemy_name == "shadow man" and "crystal" not in inventory:
            message = f"The {enemy_name} blocks your path. You need a crystal to face him."
            current_room = previous_room
        else:
            result = battle(player, enemy_name, enemies[enemy_name], inventory)
            if result is False:
                print("Game Over")
                break
            elif result == "fled":
                message = "You retreat to safety."
                current_room = previous_room
            else:
                del rooms[current_room]["enemy"]
                message = f"You defeated the {enemy_name}!"


    game["current_room"] = current_room
    game["previous_room"] = previous_room
    game["message"] = message
    game["inventory"] = inventory
    game["player"] = player
    game["rooms"] = rooms

