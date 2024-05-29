"""
Defines the function that waits for a player to choose a valid action.
"""


from pokerpy.structures import Player


from ._action_is_valid import action_is_valid


def wait_for_player(player: Player, is_under_bet: bool):

    """
    Waits for a player to choose a valid action. Once the generator ends, returns the chosen action.
    """

    # Player keeps its turn until selects a valid action
    while True:

        # Wait for player's action
        yield player

        # Determine whether action is valid or not
        action = player.requested_action
        if action is not None and action_is_valid(action, is_under_bet):
            print(f'{player.name} {action.upper()}S')
            break
        print(f'--- invalid action: {action}')
    
    # Reset player and return requested action
    player.reset_action()
    return action