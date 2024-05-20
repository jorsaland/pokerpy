"""
Defines the function that waits for a player to choose a valid action.
"""


from pokerpy.structures import Player
from pokerpy.utils import action_is_valid


def wait_for_player(player: Player, is_under_bet: bool):

    """
    Waits for a player to choose a valid action. Once the generator ends, returns the chosen action.
    """

    # Player keeps its turn until selects a valid action
    while True:

        # Wait for player's action
        print(f'Waiting for {player.name}...')
        yield player

        # Determine wheter action is valid or not
        action = player.requested_action
        if action is not None and action_is_valid(action=action, is_under_bet=is_under_bet):
            action_print_message = f'--- {player.name} {action}s ---'.upper()
            print('-' * len(action_print_message))
            print(action_print_message)
            print('-' * len(action_print_message) + '\n')
            break
        print(f'<< INVALID ACTION: {action.upper()} >>')
    
    # Return when iteration stops
    return action