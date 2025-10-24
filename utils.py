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


def apply_class_stats(player, class_data):
    stats_to_copy = ["max_hp", "hp", "atk", "def", "spd", "combat_actions"]
    for stat in stats_to_copy:
        player[stat] = class_data[stat]
    return player

def show_nearby_item(rooms,cur_room):
    if "items" in rooms[cur_room] and rooms[cur_room]["items"]:
        nearby_items = rooms[cur_room]["items"]
        a = []
        for nearby_item in nearby_items:
            article = "an" if nearby_item[0].lower() in "aeiou" else "a"
            a.append(f"You see {article} {nearby_item}.")
        return  "\n".join(a)
    return ""


def class_selection(game,inv,char_classes):
    print("CHOOSE YOUR ORIGIN")
    print("In this wretched place your past defines survival \n")

    for c,c_data in char_classes.items():
        print(f"-{c.upper()}: {c_data["description"]}")

    while True:
        chosen_class = input("What is your origin\n").strip().lower()
        if chosen_class in char_classes:
            c_data = char_classes[chosen_class]

            game["player"] = apply_class_stats(game["player"],c_data)
            player = game["player"]

            for item in c_data["starting_gear"]:
                inv[item] =inv.get(item,0) + 1
            print(f"\nYou are {chosen_class.upper()}.")
            print(f"HP:{player['hp']} ATK:{player['atk']} DEF:{player['def']} SPD:{player['spd']}")
            print(f"Combat skills: {', '.join(player['combat_actions'])}")
            input("\nPress any key to face what awaits...")
            break
        else:
            print("Unknown origin. Choose:", list(char_classes.keys()))