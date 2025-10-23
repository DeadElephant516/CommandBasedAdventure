import random
from items import items


def pick_up_item(rooms,current_room,item_name,inv):
    if "items" in rooms[current_room] and item_name in rooms[current_room]["items"]:
        inv[item_name] = inv.get(item_name,0) + 1
        rooms[current_room]["items"].remove(item_name)
        return f"You picked up the {item_name}."
    else:
        return "There's nothing like that here."


def use_item(player,inv,item_name):
    if item_name not in inv or inv[item_name] <= 0:
        return f"You don't have {item_name}."

    if item_name not in items:
        return f"{item_name} seems unfamiliar, you don't hold any knowledge about that"

    item = items[item_name]

    if item["type"] == "healing":
        heal_amount = random.randint(*item["heal"])
        player["hp"] += heal_amount
        if player["hp"] > player["max_hp"]:
            player["hp"] = player["max_hp"]
        inv[item_name] -= 1
        if inv[item_name] == 0:
            del inv[item_name]
        return f"You used {item_name} and healed for {heal_amount} | Current HP: {player['hp']}"

def equip_item(player,inv,item_name):
    if item_name not in inv or inv[item_name] <= 0:
        return f"You don't have {item_name} in your belongings"
    if item_name not in items:
        return f"{item_name} does not exist"

    item = items[item_name]
    slot = item["type"]

    old_item = player["equipped"].get(slot)
    if old_item:
        unequip_item(player,inv,old_item)

    player["equipped"][slot] = item_name

    for stat in ["max_hp", "atk", "def", "spd"]:
        player[stat] += item[f"{stat}_bonus"]

    inv[item_name] -= 1
    if inv[item_name] == 0:
        del inv[item_name]

    return f"You equipped {item_name}"



def unequip_item(player,inv,item_name):
    if item_name not in items:
        return f"{item_name} does not exist"

    item = items[item_name]
    slot = item["type"]

    if player["equipped"].get(slot) != item_name:
        return f"{item_name} is not equipped"

    for stat in ["max_hp", "atk", "def", "spd"]:
        player[stat] -= item[f"{stat}_bonus"]

    player["equipped"][slot] = None

    inv[item_name] = inv.get(item_name, 0) + 1

    return f"You unequipped {item_name}"


