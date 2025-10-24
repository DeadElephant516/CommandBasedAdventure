import random

def roll_dice(sides):
    return random.randint(1,sides)

def check_counter_attack(player,enemy,c_state):
    has_guard = "guard" in c_state["temp_effects"]["player"]["active_actions"]
    if has_guard:
        counter_chance = c_state["temp_effects"]["player"]["def_bonus"] * 8
        return random.randint(1,100) <= counter_chance
    return False

def apply_counter_attack(player,enemy):
    damage = max(1, player["atk"] - enemy["def"] + roll_dice(3))
    enemy["hp"] -= damage
    return f"You counterattacked for {damage} damage"

def check_bluff(player,enemy,c_state):
    has_bluff = "bluff" in c_state["temp_effects"]["player"]["active_actions"]
    if has_bluff:
        player_speed = player["spd"] + c_state["temp_effects"]["player"]["spd_bonus"]
        enemy_speed = enemy["spd"] + c_state["temp_effects"]["enemy"]["spd_bonus"]
        is_faster = player_speed > enemy_speed
        return is_faster, random.randint(1,100) <= 40

def apply_dodge(player, enemy):
    """Execute dodge"""
    return "You dodge the attack"


EFFECT_MAP = {
    "counter_attack" : {
        "check" : check_counter_attack,
        "apply" : apply_counter_attack,
        "interrupt" : True,
    },
    "bluff" : {
        "check" : check_bluff,
        "apply" : apply_dodge,
        "interrupt" : True,
    }
}
