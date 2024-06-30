"""
Defines the function that waits for a player to choose a valid action.
"""


from pokerpy.logger import get_logger
from pokerpy.structures import Player, Table


from ._action_is_valid import action_is_valid


logger = get_logger()


def wait_for_player(*, player: Player, table: Table):

    """
    Waits for a player to choose a valid action. Once the generator ends, returns the chosen action.
    """

    # Player keeps its turn until selects a valid action
    while True:

        # Wait for player's action
        yield player

        # Determine whether action is valid or not
        action = player.requested_action
        if action is not None and action_is_valid(action=action, table=table, player=player):
            player.add_to_current_amount(action.amount)
            logger.info(f"{''.join(str(card) for card in player.cards)} {player.name} {action.name.upper()}S {action.amount} ({player.name}'s current amount: {player.current_amount})")
            break
        logger.debug(f'--- invalid action: {action.name}s {action.amount}')

    # Reset player and return requested action
    player.reset_action()
    return action