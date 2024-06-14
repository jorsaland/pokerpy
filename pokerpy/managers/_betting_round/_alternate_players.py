"""
Defines the function that alternates players within the betting round.
"""


from pokerpy.constants import ACTION_FOLD, aggressive_actions
from pokerpy.structures import Table


from ._wait_for_player import wait_for_player


def alternate_players(table: Table):

    """
    Alternates players within the betting round.
    """

    # All players are itered but only active ones are allowed to act
    for player in table.players:

        # Determine whether betting round should be stopped or not
        if len(table.active_players) == 1:
            print(f'--- only one active player ({table.active_players[0].name})... ending round\n')
            break

        # Determine whether player should be allowed to play or not
        if player not in table.active_players:
            print(f'--- {player.name} already folded\n')
            continue

        # Let player keep choosing an action until it is valid
        action = yield from wait_for_player(
            player = player,
            is_under_bet = table.is_under_bet,
            fold_to_nothing = table.fold_to_nothing,
        )

        # Determine whether round becomes under bet or not
        if action in aggressive_actions:
            table.become_under_bet()
        
        # Determine whether the player becomes inactive or not
        if action == ACTION_FOLD:
            table.fold_player(player)