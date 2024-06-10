"""
Defines the function that alternates players within the betting round.
"""


from pokerpy.constants import ACTION_FOLD, aggressive_action_names
from pokerpy.logger import get_logger
from pokerpy.structures import Table


logger = get_logger()


from ._wait_for_player import wait_for_player


def alternate_players(table: Table):

    """
    Alternates players within the betting round. Once the generator ends, returns whether round must stop or not.
    """

    round_must_stop = False

    # All players are itered but only active ones are allowed to act
    for player in table.players:

        # Determine whether betting round should be stopped or not
        if len(table.active_players) == 1:
            round_must_stop = True
            break
        if player == table.last_aggressive_player:
            round_must_stop = True
            break

        # Determine whether player should be allowed to play or not
        if player not in table.active_players:
            continue

        # Player keeps its turn until selects a valid action
        action = yield from wait_for_player(player=player, table=table)

        # Set consequences of aggressive actions
        if action.name in aggressive_action_names:
            table.add_to_current_amount(player.current_amount - table.current_amount)
            table.set_last_aggressive_player(player)

        # Determine whether the player becomes inactive or not
        if action.name == ACTION_FOLD:
            table.fold_player(player)

        logger.info(f'TABLE CURRENT AMOUNT: {table.current_amount}\n')

    return round_must_stop