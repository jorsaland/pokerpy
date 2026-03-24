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


from pokerpy.logger import get_logger
from pokerpy.structures import Player


logger = get_logger()


def no_showdown(active_players: list[Player], central_pot: int):

    """
    Displays a message on distributing the central pot to the only remaining player.
    """

    winner = active_players[0]
    logger.info(f'{winner.name} wins {central_pot}!')


def break_tie(winners: list[Player], central_pot: int):

    """
    Displays a message on how to distribute the central pot between the tied winners.
    """

    logger.info(f'It is a tie! Winners: {", ".join([w.name for w in winners])}.')
    profit_per_player = central_pot // len(winners)
    remainder = central_pot % len(winners)
    profit_by_player = {player: profit_per_player for player in winners}

    for player in winners:
        if remainder == 0:
            break
        profit_by_player[player] += 1
        remainder -= 1

    for player in winners:
        logger.info(f'{player.name} wins {profit_by_player[player]}.')

    return


def showdown(active_players: list[Player], central_pot: int):

    """
    Determines who are the winners among remaining players and displays a message on how to distribute the pot.
    """

    logger.info(f'Remaining players: {", ".join(p.name for p in active_players)}')

    winners: list[Player] = []
    for player in active_players:

        player_is_unbeaten = True
        for oponent in active_players:
            if oponent.name == player.name:
                continue
            if oponent.hand > player.hand:
                player_is_unbeaten = False
                break

        if player_is_unbeaten:
            winners.append(player)

    if len(winners) == 1:
        logger.info(f'{winners[0].name} wins {central_pot}!')
        return

    return break_tie(winners, central_pot)