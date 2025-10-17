import random
from items import items

def use_item(player,inv,item_name):
    if item_name not in inv:
        return f"You don't have {item_name}."

    if item_name not in items:
        return f"{item_name} seems unfamiliar, you don't hold any knowledge about that"

    item = items[item_name]

    if item["type"] == "healing":
        heal_amount = random.randint(*item["heal"])
        player["hp"] += heal_amount
        if player["hp"] > player["max_hp"]:
            player["hp"] = player["max_hp"]
        inv.remove(item_name)
        return f"You used {item_name} and healed for {heal_amount} | Current HP: {player['hp']}"
