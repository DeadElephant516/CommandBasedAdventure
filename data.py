import random

# --- MAP SETUP (all lowercase for consistency) ---
rooms = {
    "liminal space":
        {"exits" : {"north": "mirror maze", "south": "bat cavern", "east": "bazaar"}},
    "mirror maze":
        {"exits": {"south": "liminal space"},
         "items": ["wearable skin"]},
    "bat cavern":
        {"exits": {"north": "liminal space", "east": "volcano"},
         "items": ["dagger"],
         "enemy" : "bat"},
    "bazaar":
        {"exits" : {"west": "liminal space", "north": "meat locker", "east": "dojo"},
         "items": ["altoids"], },
    "meat locker":
        {"exits" : {"south": "bazaar", "east": "quicksand pit"},
         "items": ["fig", "hermes feet"],
         "enemy": "rat"},
    "quicksand pit":
        {"exits" : {"west": "meat locker"},
         "items": ["crystal", "elderberry"],
         "enemy" : "goblin"},
    "volcano":
        {"exits" : {"west": "bat cavern"},
         "items": ["elderberry"],
         "enemy" : "goblin"},
    "dojo":
        {"exits" : {"west": "bazaar"},
         "enemy": "shadow man"}
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
    "bat" : {"hp" : 5, "atk" : 1, "def" : 1, "spd" : 3, "max_dice" : 2},
    "rat" : {"hp": 5, "atk": 1, "def": 1, "spd" : 1, "max_dice" : 2},
    "goblin" : {"hp": 7, "atk": 2, "def": 3, "spd" : 2, "max_dice" : 3, "gold": random.randint(5,10)},
    "shadow man" : {"hp": 15, "atk" : 7, "def" : 5, "spd" : 5, "max_dice" : 4}
}

# --- PLAYER STATE ---
inventory = []
current_room = "liminal space"
previous_room = ""
message = ""