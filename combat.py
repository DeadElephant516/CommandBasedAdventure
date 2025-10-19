import random
from use import use_item

temp_mods = {
    "player": {
        "atk": 0,
        "def": 0,
        "spd": 0,
        "guard_rounds": 0,
        "bluff_rounds": 0,
    },
    "enemy": {
        "atk": 0,
        "def": 0,
        "spd": 0,
        "effect_rounds": 0,
    },
}

def handle_guard(tm):
    if tm["player"]["guard_rounds"] > 0:
        tm["player"]["guard_rounds"] -= 1
        if tm["player"]["guard_rounds"] == 0:
            tm["player"]["def"] = 0
            print("Your guard fades away, you lose your stance")

def reset_guard(tm):
    tm["player"]["def"] = 0
    tm["player"]["guard_rounds"] = 0

def battle(player, enemy_name, enemy_data, inv):
    """Handles fighting, returns True if player wins, False if player dies or flees"""
    enemy = enemy_data.copy()
    print(f"\nA {enemy_name} appears")

    reset_guard(temp_mods)

    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\nYour HP {player['hp']} | {enemy_name.title()} HP: {enemy['hp']}")
        action = input("Choose an action (attack/flee)")


        if action == "attack":
            # PLAYER ATTACK
            player_dice = random.randint(1,6)
            player_attack_roll = random.randint(1,6) + player["spd"]
            enemy_dodge_roll = random.randint(1,6) + enemy["spd"]
            if player_attack_roll >= enemy_dodge_roll:
                player_damage = max(1, player["atk"] - enemy["def"]  + player_dice)
                enemy["hp"] -= player_damage
                print(f"You hit the {enemy_name} for {player_damage} damage!")
            else:
                print(f"The {enemy_name} dodged your attack")

            # ENEMY ATTACK
            enemy_dice = random.randint(1, enemy["max_dice"])
            enemy_attack_roll = random.randint(1,6) + enemy["spd"]
            player_dodge_roll = random.randint(1,6) + player["spd"]
            if enemy_attack_roll >= player_dodge_roll:
                enemy_damage = max(1, enemy["atk"] - player["def"]  + enemy_dice)
                player["hp"] -= enemy_damage
                print(f"The {enemy_name} hits you for {enemy_damage} damage!")
            else:
                print(f"You dodged {enemy_name} attack")

            # AFTER EXCHANGE
            print(f"\nAfter the exchange:\nYour HP: {player['hp']} | {enemy_name.title()} HP: {enemy['hp']}")

        elif action == "guard":
            player_dice = random.randint(1,6)
            guard_dice = random.randint(1,6)
            temp_mods["player"]["def"] = random.randint(3,5)
            temp_mods["player"]["guard_rounds"] = 3 if guard_dice != 6 else 4
            effective_rounds = temp_mods["player"]["guard_rounds"] - 1
            effective_def = player["def"] + temp_mods["player"]["def"]
            enemy_dice = random.randint(1, enemy["max_dice"])
            print(f"you guard for {temp_mods['player']['def']} extra points of def for {effective_rounds}")

            if guard_dice == 6:
                counter_damage = max(1, player["atk"] - enemy["def"] + player_dice)
                enemy["hp"] -= counter_damage
                print(f"Your guard triggered a counter attack! You deal {counter_damage} to {enemy_name}")
            else:
                enemy_damage = max(0, (enemy["atk"] + enemy_dice) - effective_def)
                if enemy_damage > 0:
                    player["hp"] -= enemy_damage
                    print(f"The {enemy_name} hits you for {enemy_damage} damage!")
                else:
                    print(f"You blocked the attack with your guard!")

        elif action == "flee":
            print("You escape the danger with a cost")
            return "fled"

        elif action.startswith("use "):
            item_name = action.split(" ", 1)[1]
            message = use_item(player, inv, item_name)
            print(message)

        else:
            print("invalid command")

        handle_guard(temp_mods)
        print(
            f"HP:{player['hp']} | DEF:{player['def']}+{temp_mods['player']['def']}({temp_mods['player']['guard_rounds']}r) = {player['def'] + temp_mods['player']['def']} |"
            f" ATK+:{temp_mods['player']['atk']} | SPD+:{temp_mods['player']['spd']}")

        # --- check battle result each turn ---
        if player["hp"] <= 0 and enemy["hp"] <= 0:
            print("You both fall to the ground for a final rest")
            return False
        elif enemy["hp"] <= 0:
            print(f"You've slain the {enemy_name}")
            return True
        elif player["hp"] <= 0:
            print("You Died")
            return False

    return False
