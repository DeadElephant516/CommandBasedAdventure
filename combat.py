import random


def battle(player, enemy_name, enemy_data):
    """Handles fighting returns True if player wins returns False if player dies or flees"""
    enemy = enemy_data.copy()
    print(f"\nA {enemy_name} appears")

    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\nYour HP {player["hp"]} | {enemy_name.title()} HP: {enemy["hp"]}")
        action = input("Choose an action (attack/flee)")

        if action == "attack":
            #PLAYER ATTACK
            player_dice = random.randint(1,6)
            attack_roll = random.randint(1,20) + player["spd"]
            dodge_roll = random.randint(1,20) + enemy["spd"]
            if attack_roll >= dodge_roll:
                player_damage = max(1,  player["atk"] - enemy["def"]) + player_dice
                enemy["hp"] -= player_damage
                print(f"You hit the {enemy_name} for {player_damage} damage!")
            else:
                print(f"The {enemy_name} dodged your attack")
            #ENEMY ATTACK
            enemy_dice = random.randint(1,enemy["max_dice"])
            attack_roll = random.randint(1,20) + enemy["spd"]
            dodge_roll = random.randint(1,20) + player["spd"]
            if attack_roll >= dodge_roll:
                enemy_damage = max(1, enemy["atk"] - player["def"]) + enemy_dice
                player["hp"] -= enemy_damage
                print(f"The {enemy_name} hits you for {enemy_damage} damage!")
            else:
                print(f"You dodged {enemy_name} attack")
                #EXCHANGE RESULT
            print(f"\nAfter the exchange:\nYour HP: {player['hp']} | {enemy_name.title()} HP: {enemy['hp']}")

            #CHECK RESULT
            if player["hp"] <= 0 and enemy["hp"] <= 0:
                print("You both fall to the ground for a final rest")
                return False
            elif enemy["hp"] <= 0:
                print(f"You've slain the {enemy_name}")
                return True
            elif player["hp"] <= 0:
                print("You Died")
                return False

        elif action == "flee":
            print("You escape the danger with a cost")
            return "fled"
        else:
            print("invalid command")

    return False

