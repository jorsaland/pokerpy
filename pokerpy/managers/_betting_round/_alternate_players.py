"""
Defines the function that alternates players within the betting round.
"""


from pokerpy.constants import ACTION_FOLD, aggressive_action_names
from pokerpy.logger import get_logger
from pokerpy.structures import Table


logger = get_logger()


from ._wait_for_player import wait_for_player


def alternate_players(*, table: Table, ignore_invalid_actions: bool):

    """
    Alternates players within the betting round. Once the generator ends, returns whether round must stop or not.
    """

    round_must_stop = False

    # All players are itered but only active ones are allowed to act
    for player in table.players:

        # Stop if there is one player remaining
        if len(table.active_players) == 1:
            round_must_stop = True
            break

        # Determine whether player should be allowed to play or not
        if player not in table.active_players:
            continue

        # Player keeps its turn until selects a valid action
        action = yield from wait_for_player(
            player = player,
            table = table,
            ignore_invalid_actions = ignore_invalid_actions,
        )

        # Set consequences of aggressive actions
        if action.name in aggressive_action_names:
            table.add_to_current_amount(player.current_amount - table.current_amount)
            table.set_stopping_player(player)

        # Determine whether the player becomes inactive or not
        if action.name == ACTION_FOLD:
            table.fold_player(player)

        # Stop if the current player still is the stopping player
        if player == table.stopping_player:
            round_must_stop = True
            break

        logger.info(f'TABLE CURRENT AMOUNT: {table.current_amount}\n')

    return round_must_stop