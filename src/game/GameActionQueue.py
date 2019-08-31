action_from_player = []
message_to_player = []

def add_action_from_player(msg, player):
    action_from_player.append([player, msg])

def get_action_from_player():
    return action_from_player.pop(0)

def add_message_to_player(msg, player):
    message_to_player.append([player, msg])

def get_message_to_player():
    return message_to_player.pop(0)