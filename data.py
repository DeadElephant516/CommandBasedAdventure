import random

# --- MAP SETUP (all lowercase for consistency) ---
rooms = {
    "liminal space": {
        "exits": {"north": "mirror maze", "south": "bat cavern", "east": "bazaar"},
        "description": "A space between spaces. The air hums with static possibility.\n"
                       "Flickering lights reveal endless corridors that shift when not observed.\n"
                       "You feel both nowhere and everywhere at once.",
        "items": [],
        "enemy": None
    },
    "mirror maze": {
        "exits": {"south": "liminal space"},
        "description": "Countless mirrors reflect endless versions of yourself.\n"
                       "Some reflections move independently, mocking your gestures.\n"
                       "The air is cold and the sound of breaking glass echoes from unseen distances.",
        "items": ["wearable skin"],
        "enemy": None
    },
    "bat cavern": {
        "exits": {"north": "liminal space", "east": "volcano"},
        "description": "The ceiling drips with sleeping bat-things that are not quite bats.\n"
                       "Their leathery wings twitch in unison. The floor is carpeted in bones picked clean.\n"
                       "A faint chittering fills the oppressive dark.",
        "items": ["dagger"],
        "enemy": "bat"
    },
    "bazaar": {
        "exits": {"west": "liminal space", "north": "meat locker", "east": "dojo"},
        "description": "Stalls made of bone and stretched skin display wares no living being should sell.\n"
                       "Shadowy figures haggle over prices paid in memories. The air smells of incense and decay.\n",
        "items": ["altoids"],
        "enemy": None
    },
    "meat locker": {
        "exits": {"south": "bazaar", "east": "quicksand pit"},
        "description": "Hooks dangling from chains hold carcasses that still twitch.\n"
                       "The walls weep crimson, and the floor is slick with things better left unexamined.\n"
                       "A low moaning vibrates through the meat.",
        "items": ["fig", "hermes feet"],
        "enemy": "rat"
    },
    "quicksand pit": {
        "exits": {"west": "meat locker"},
        "description": "The ground shifts uneasily, pulling at your feet.\n"
                       "Pale hands occasionally breach the surface before sinking back into the hungry earth.\n"
                       "The air is thick with the scent of wet grave.",
        "items": ["crystal", "elderberry"],
        "enemy": "goblin"
    },
    "volcano": {
        "exits": {"west": "bat cavern"},
        "description": "Molten rock flows in veins of orange and black.\n"
                       "The heat is unnatural, carrying whispers of ancient fury.\n"
                       "Ash falls like snow, coating everything in gray funeral shroud.",
        "items": ["elderberry"],
        "enemy": "goblin"
    },
    "dojo": {
        "exits": {"west": "bazaar"},
        "description": "Tatami mats float in perfect formation above an endless void.\n"
                       "Training dummies made of shadow practice forms without masters.\n"
                       "This is where final tests are administered.",
        "items": [],
        "enemy": "shadow man"
    }
}


#PLAYER STATS AND ENEMIES
player_base = {"max_hp" : 10,
          "hp" : 10,
          "atk" : 5,
          "def" : 5,
          "spd" : 2,
          "equipped" : {
              "weapon" : None,
              "armor" : None,
              "helmet" : None,
              "gloves" : None,
              "boots" : None,
            }
          }


enemies = {
    "bat" : {"hp" : 5, "atk" : 1, "def" : 1, "spd" : 3, "max_dice" : 2, "drop": {"bat wing" : (0,2)} },
    "rat" : {"hp": 5, "atk": 1, "def": 1, "spd" : 1, "max_dice" : 2, "drop" : {"rat tail": (0,1)} },
    "goblin" : {"hp": 7, "atk": 2, "def": 3, "spd" : 2, "max_dice" : 3, "drop": {"gold": (5,10)} },
    "shadow man" : {"hp": 15, "atk" : 7, "def" : 5, "spd" : 5, "max_dice" : 4}
}

# --- PLAYER STATE ---
inventory = {}
current_room = "liminal space"
previous_room = ""
message = ""