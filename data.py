
# --- MAP SETUP (all lowercase for consistency) ---
rooms = {
    "liminal space": {"north": "mirror maze", "south": "bat cavern", "east": "bazaar"},
    "mirror maze": {"south": "liminal space", "item": "wearable skin"},
    "bat cavern": {"north": "liminal space", "east": "volcano", "item": "dagger", "enemy" : "bat"},
    "bazaar": {"west": "liminal space", "north": "meat locker", "east": "dojo", "item": "altoids", "enemy" : "rat"},
    "meat locker": {"south": "bazaar", "east": "quicksand pit", "item": "fig", "enemy": "rat"},
    "quicksand pit": {"west": "meat locker", "item": "crystal", "enemy" : "goblin"},
    "volcano": {"west": "bat cavern", "item": "elderberry", "enemy" : "goblin"},
    "dojo": {"west": "bazaar", "enemy": "shadow man"}
}

healing_items = ["fig", "elderberry", "essence of life"]

#PLAYER STATS AND ENEMIES
player = {"max_hp" : 10,
          "hp" : 10,
          "atk" : 5,
          "def" : 5,
          "spd" : 2,
          "equipped" : {
              "weapon" : None,
              "armor" : None,
              "helmet" : None,
              "gloves" : None,
              "boots" : None
            }
          }


player["hp"] = player["max_hp"]

enemies = {
    "bat" : {"hp" : 5, "atk" : 1, "def" : 1, "spd" : 5, "max_dice" : 2},
    "rat" : {"hp": 5, "atk": 1, "def": 1, "spd" : 1, "max_dice" : 2},
    "goblin" : {"hp": 7, "atk": 2, "def": 3, "spd" : 2, "max_dice" : 3},
    "shadow man" : {"hp": 15, "atk" : 6, "def" : 5, "spd" : 5, "max_dice" : 4}
}

# --- PLAYER STATE ---
inventory = []
current_room = "liminal space"
previous_room = ""
message = ""