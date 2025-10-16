import random


def battle(player, enemy_name, enemy_data):
    """Handles fighting returns True if player wins returns False if player dies or flees"""
    enemy = enemy_data.copy()
    print(f"\nA {enemy_name} appears")

    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\nYour HP {player["hp"]} | {enemy_name.title()} HP: {enemy["hp"]}")
        action = input("Chose an action (attack/flee)")

        if action == "attack":
            #PLAYER ATTACK
            player_damage = max(1,  player["atk"] - enemy["def"])
            enemy["hp"] -= player_damage
            #ENEMY ATTACK
            enemy_damage = max(1, enemy["atk"] - player["def"])
            player["hp"] -= enemy_damage
            #FEEDBACK
            print(f"You hit the {enemy_name} for {player_damage} damage!")
            print(f"The {enemy_name} hits you for {enemy_damage} damage!")
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

