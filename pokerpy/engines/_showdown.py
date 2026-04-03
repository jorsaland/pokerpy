# Copyright 2026 Andrés Saldarriaga Jordan (jorsaland)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Defines the functions to distribute the pot at the end of a cycle.
"""


from collections import defaultdict
from collections.abc import Sequence


from pokerpy.messages import msg_not_table_instance
from pokerpy.logger import get_logger
from pokerpy.structures import Player, Table


logger = get_logger()


def break_tie(winners: Sequence[Player], pot: int, pot_index: int):

    """
    Distributes the central pot between the tied winners.
    """

    pot_name = 'main pot' if pot_index == 0 else f'side pot {pot_index}'
    logger.info(f'it is a tie for {pot_name}! winners: {", ".join([w.name for w in winners])}.')
    profit_per_winner = pot // len(winners)
    remainder = pot % len(winners)
    profit_by_winner = {winner: profit_per_winner for winner in winners}

    for player in winners:
        if remainder == 0:
            break
        profit_by_winner[player] += 1
        remainder -= 1

    for winner in winners:
        profit = profit_by_winner[winner]
        if pot_index == 0:
            logger.info(f'{winner.name} wins {profit}.')
        else:
            logger.info(f'{winner.name} wins {profit}.')
        winner.add_to_stack(profit)


def showdown(table: Table):

    """
    Determines who are the winners among the remaining players and distributes the pot between them.
    """

    if not isinstance(table, Table):
        raise TypeError(msg_not_table_instance.format(type(table).__name__))

    logger.info(f'Remaining players: {", ".join(player.name for player in table.players_in_hand)}')

    players_by_participation: dict[int, list[Player]] = {player.pot_participation: [] for player in table.players_in_hand}
    for participation, participating_players in players_by_participation.items():
        for player in table.players_in_hand:
            if player.pot_participation >= participation:
                participating_players.append(player)

    for i, side_pot in enumerate(table.split_pot):

        winners: list[Player] = []

        min_pot_participation = min(players_by_participation.keys())
        participating_players = players_by_participation.pop(min_pot_participation)

        for player in participating_players:
            player_is_unbeaten = True
            for oponent in participating_players:
                if oponent.name == player.name:
                    continue
                if oponent.hand > player.hand:
                    player_is_unbeaten = False
                    break
            if player_is_unbeaten:
                winners.append(player)

        if len(winners) == 1:
            winner = winners[0]
            if i == 0:
                logger.info(f'{winner.name} wins main pot: {side_pot}!')
            else:
                logger.info(f'{winner.name} wins side pot {i}: {side_pot}!')
            winner.add_to_stack(side_pot)
        else:
            break_tie(winners, side_pot, i)