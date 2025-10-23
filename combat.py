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

def roll_dice(a,b):
    dice = random.randint(a,b)
    return dice

def handle_guard(tm):
    if tm["player"]["guard_rounds"] > 0:
        tm["player"]["guard_rounds"] -= 1
        if tm["player"]["guard_rounds"] == 0:
            tm["player"]["def"] = 0
            print("Your guard fades away, you lose your stance")

def handle_bluff(tm):
    if tm["player"]["bluff_rounds"] > 0:
        tm["player"]["bluff_rounds"] -= 1
        if tm["player"]["bluff_rounds"] == 0:
            tm["player"]["spd"] = 0
            tm["enemy"]["spd"] = 0
            print("Your bluff fades, enemy recovers")

def reset_guard(tm):
    tm["player"]["def"] = 0
    tm["player"]["guard_rounds"] = 0

def reset_bluff(tm):
    tm["player"]["spd"] = 0
    tm["player"]["bluff_rounds"] = 0
    tm["enemy"]["spd"] = 0


def enemy_attack(enemy_name, enemy, player, tm):
    """Handles enemy attacking the player. Returns damage dealt."""
    player_dice = roll_dice(1, 6)
    enemy_dice = roll_dice(1, enemy["max_dice"])

    enemy_attack_roll = enemy_dice + enemy["spd"] + tm["enemy"]["spd"]
    player_dodge_roll = player_dice + player["spd"] + tm["player"]["spd"]
    effective_def = player["def"] + tm["player"]["def"]
    if enemy_attack_roll >= player_dodge_roll:
        damage = max(1, enemy["atk"] - effective_def + enemy_dice // 2)
        player["hp"] -= damage
        print(f"The {enemy_name} hits you for {damage} damage!")
    else:
        damage = 0
        print(f"You dodged {enemy_name} attack")

    return damage


def battle(player, enemy_name, enemy_data, inv):
    """Handles fighting, returns True if player wins, False if player dies or flees"""
    enemy = enemy_data.copy()
    print(f"\nA {enemy_name} appears")

    reset_guard(temp_mods)
    reset_bluff(temp_mods)

    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\nYour HP {player['hp']} | {enemy_name.title()} HP: {enemy['hp']}")
        action = input("Choose an action (attack/flee)")
        action = action.lower()


        if action == "attack":
            # PLAYER ATTACK
            player_dice = roll_dice(1,6)
            enemy_dice = roll_dice(1,enemy["max_dice"])
            player_attack_roll = player_dice//2 + player["spd"] + temp_mods["player"]["spd"]
            enemy_dodge_roll = enemy_dice//2 + enemy["spd"] + temp_mods["enemy"]["spd"]
            if player_attack_roll >= enemy_dodge_roll:
                player_damage = max(1, player["atk"] - enemy["def"]  + player_dice//2)
                enemy["hp"] -= player_damage
                print(f"You hit the {enemy_name} for {player_damage} damage!")
            else:
                print(f"The {enemy_name} dodged your attack")

            #ENEMY ATTACK
            enemy_attack(enemy_name,enemy,player,temp_mods)

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
            print(f"you guard for {temp_mods['player']['def']} extra points of def for {effective_rounds} rounds")

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

        elif action == "bluff":
            player_dice = roll_dice(1,6)
            if player_dice > 2:
                temp_mods["player"]["spd"] = 1
                temp_mods["player"]["bluff_rounds"] = 3 if player_dice != 6 else 4
                effective_rounds = temp_mods["player"]["bluff_rounds"] - 1
                temp_mods["enemy"]["spd"] = -2 if player_dice != 6 else 3
                print(f"You bluff! Your speed rises by 1, enemy speed drops by {temp_mods["enemy"]["spd"]} for {effective_rounds} rounds")
            else:
                print("Your bluff failed! Enemy sees through your move.")
                temp_mods["player"]["spd"] = 0
                temp_mods["enemy"]["spd"] = 0

            # ENEMY ATTACK
            enemy_attack(enemy_name,enemy,player,temp_mods)

            # AFTER EXCHANGE
            print(f"\nAfter the exchange:\nYour HP: {player['hp']} | {enemy_name.title()} HP: {enemy['hp']}")



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
        handle_bluff(temp_mods)

        print(
            f"HP:{player['hp']} | DEF:{player['def']}+{temp_mods['player']['def']}({temp_mods['player']['guard_rounds']}r) = {player['def'] + temp_mods['player']['def']} |"
            f" ATK+:{temp_mods['player']['atk']} | SPD+:{temp_mods['player']['spd']}({temp_mods['player']['bluff_rounds']}r)")

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
