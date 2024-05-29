"""
Defines the function that alternates players within the betting round.
"""


from pokerpy.constants import ACTION_FOLD, aggressive_actions
from pokerpy.structures import Table


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
        action = yield from wait_for_player(player=player, is_under_bet=table.is_under_bet)

        # Set consequences of aggressive actions
        if action in aggressive_actions:
            table.become_under_bet()
            table.set_last_aggressive_player(player)

        # Determine whether the player becomes inactive or not
        if action == ACTION_FOLD:
            table.fold_player(player)
    
    return round_must_stop