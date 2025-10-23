import random

items = {
        "fig" : {
            "type": "healing",
            "heal": (2,6),   #Healing range
            "description" : "a sweet fig in a bitter place, lesser wound healing"
        },
        "elderberry" : {
            "type" : "healing",
            "heal" : (3,7),
            "description" : "an almost magical berry, mild wound healing"
        },
        "essence of life" : {
            "type" : "healing",
            "heal" : (5,10),
            "description" : "for a body to restored a certain soul must be taken"
        },
        "crystal" : {
            "type" : "quest",
            "description" : "a dim crystal, pretty dark for an otherwise shiny object"
        },
        "dagger": {
            "type" : "weapon",
            "max_hp_bonus" : 0,
            "atk_bonus" : 2,
            "def_bonus": 0,
            "spd_bonus" : 0,
            "description" : "sharp like a twisted mind, a great fit to such world"
        },
        "wearable skin" : {
            "type" : "armor",
            "max_hp_bonus" : 0,
            "atk_bonus" : 0,
            "def_bonus" : 2,
            "spd_bonus" : 0,
            "description" : "an insult to the fallen, a praise for those who continue"
        },
        "altoids" : {
            "type" : "consumable",
            "description" : "savor a taste while you can, it won't be always the same"
        },
        "hermes feet" : {
            "type" : "boots",
            "max_hp_bonus": 0,
            "atk_bonus": 0,
            "def_bonus": 0,
            "spd_bonus": 2,
            "description": "seems like they were attacked to someone's body"
        }
}