import data

game = {
    "rooms" : data.rooms,
    "player" : data.player_base.copy(),
    "enemies" : data.enemies,
    "inventory" : data.inventory,
    "current_room" : data.current_room,
    "previous_room" : data.previous_room,
    "message" : data.message,
    "healing_items" : data.healing_items,
}

