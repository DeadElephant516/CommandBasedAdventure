import random
from use import use_item

#COMBAT STATE
combat_state = {
    "round" : 1,
    "player_turn" : True,
    "message" : "",
    "temp_effects" : {
        "player" : {"def_bonus":0,
                    "spd_bonus":0,
                    "rounds_left":0,
                    },
        "enemy": {"def_bonus": 0,
                  "spd_bonus": 0,
                  "rounds_left":0,
                    }
    }
}

def roll_dice(sides):
    return random.randint(1,sides)


def calculate_initiative(player,enemy):
    player_initiative = player["spd"] + combat_state["temp_effects"]["player"]["spd_bonus"] + roll_dice(6)
    enemy_initiative = enemy["spd"] + combat_state["temp_effects"]["enemy"]["spd_bonus"] + roll_dice(6)
    return player_initiative >= enemy_initiative

def player_attack(player,enemy):
    damage_roll = roll_dice(6)
    damage = max(1, player["atk"] - enemy["def"] + damage_roll//2)
    enemy["hp"] -= damage
    return f"You strike for {damage} damage"

def enemy_attack(player,enemy):
    damage_roll = roll_dice(6)
    damage = max(1, enemy["atk"] - player["def"] + damage_roll//2)
    player["hp"] -= damage
    return f"The {enemy['name']} hits you for {damage} damage!"

def guard(player,enemy):
    guard_bonus = random.randint(2,4)
    combat_state["temp_effects"]["player"]["def_bonus"] = guard_bonus
    combat_state["temp_effects"]["player"]["rounds_left"] = 2
    return f"You take a defensive stance! + {guard_bonus} DEF for 2 rounds"

def bluff(player,enemy):
    if roll_dice(6) > 2:
        combat_state["temp_effects"]["player"]["spd_bonus"] = 1
        combat_state["temp_effects"]["player"]["rounds_left"] = 2
        combat_state["temp_effects"]["enemy"]["spd_bonus"] = -2
        combat_state["temp_effects"]["enemy"]["rounds_left"] = 2
        return "Your bluff confuses the enemy, Their speed drops by 2! You gain +1 spd"
    return "Failure, the enemy sees through your bluff"


def handle_combat_actions(player, enemy, action, inventory):
    """Process player's chosen action"""
    if action == "attack":
        return player_attack(player, enemy)

    elif action == "guard" and "guard" in player["combat_actions"]:
        return guard(player, enemy)

    elif action == "bluff" and "bluff" in player["combat_actions"]:
        return bluff(player, enemy)

    elif action.startswith("use "):
        item_name = action.split(" ", 1)[1]
        return use_item(player, inventory, item_name)

    elif action == "flee":
        return "flee"

    return "Invalid action!"


def update_combat_effects():
    """Handle effect expiration"""
    # Reduce effect durations
    for entity in ["player", "enemy"]:
        if combat_state["temp_effects"][entity]["rounds_left"] > 0:
            combat_state["temp_effects"][entity]["rounds_left"] -= 1
            if combat_state["temp_effects"][entity]["rounds_left"] == 0:
                combat_state["temp_effects"][entity]["def_bonus"] = 0
                combat_state["temp_effects"][entity]["spd_bonus"] = 0


def display_combat_status(player, enemy_name, enemy):
    """Show clear combat UI"""
    print(f"\n=== ROUND {combat_state['round']} ===")
    print(f"Your HP: {player['hp']}/{player['max_hp']} | {enemy_name}: {enemy['hp']} HP")

    # Show active effects
    player_effects = []
    if combat_state["temp_effects"]["player"]["def_bonus"]:
        player_effects.append(f"+{combat_state['temp_effects']['player']['def_bonus']} DEF")
    if combat_state["temp_effects"]["player"]["spd_bonus"]:
        player_effects.append(f"+{combat_state['temp_effects']['player']['spd_bonus']} SPD")

    if player_effects:
        print(f"Active effects: {', '.join(player_effects)}")


def battle(player, enemy_name, enemy_data, inventory):
    """Main combat loop - clean turn-based system"""
    enemy = enemy_data.copy()
    enemy["name"] = enemy_name

    # Reset combat state for new battle
    combat_state.update({"round": 1, "player_turn": True, "message": ""})
    combat_state["temp_effects"] = {"player": {"def_bonus": 0, "spd_bonus": 0, "rounds_left": 0},
                                    "enemy": {"def_bonus": 0, "spd_bonus": 0, "rounds_left": 0}}

    print(f"\n⚔️ A {enemy_name} confronts you! ⚔️")

    while enemy["hp"] > 0 and player["hp"] > 0:
        display_combat_status(player, enemy_name, enemy)

        # Determine turn order each round
        player_goes_first = calculate_initiative(player, enemy)

        if player_goes_first:
            # Player turn
            print(f"\n--- YOUR TURN ---")
            available_actions = player.get("combat_actions", ["attack", "flee"])
            print(f"Actions: {', '.join(available_actions)}")

            action = input("Choose action: ").strip().lower()
            result = handle_combat_actions(player, enemy, action, inventory)

            if result == "flee":
                print("You escape from combat!")
                return "fled"

            print(result)

            # Enemy turn if still alive
            if enemy["hp"] > 0:
                print(f"\n--- {enemy_name.upper()}'S TURN ---")
                print(enemy_attack(player, enemy))

        else:
            # Enemy goes first
            print(f"\n--- {enemy_name.upper()}'S TURN ---")
            print(enemy_attack(player, enemy))

            # Player turn if still alive
            if player["hp"] > 0:
                print(f"\n--- YOUR TURN ---")
                available_actions = player.get("combat_actions", ["attack", "flee"])
                print(f"Actions: {', '.join(available_actions)}")

                action = input("Choose action: ").strip().lower()
                result = handle_combat_actions(player, enemy, action, inventory)

                if result == "flee":
                    print("You escape from combat!")
                    return "fled"

                print(result)

        # End of round cleanup
        update_combat_effects()
        combat_state["round"] += 1

        # Check battle end conditions
        if player["hp"] <= 0:
            print("\n💀 You have been defeated...")
            return False
        elif enemy["hp"] <= 0:
            print(f"\n🎉 You defeated the {enemy_name}!")
            # Handle drops here
            return True

    return False