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
Iteratively refunds the deepest side pots if the participating players are all folded. This
situation happens when players place optional blinds and then they fold.
"""


from pokerpy.structures import Player, Table


def refund_excess(table: Table):

    """
    Iteratively refunds the deepest side pots if the participating players are all folded. This
    situation happens when players place optional blinds and then they fold. If the big blind
    went all-in with less than the big blind amount, then the optional blinds will be unmatched.
    If the deepest pot matches these characteristics, the excess is returned to the players who
    posted it. Some games may be setup with multiple sizes of optional blinds, so once the deepest
    pot is exhausted, the next deepest one is evaluated.
    """

    while table.bettor_players:

        max_bet_level = 0
        next_max_bet_level = 0

        max_level_players: list[Player] = []

        for player in table.bettor_players:
            if player.bet_level > max_bet_level:
                next_max_bet_level = max_bet_level
                max_bet_level = player.bet_level
                max_level_players = [player]
            elif player.bet_level == max_bet_level:
                max_level_players.append(player)
            elif player.bet_level > next_max_bet_level:
                next_max_bet_level = player.bet_level

        if not all(player.is_folded for player in max_level_players):
            break

        max_levels_difference = max_bet_level - next_max_bet_level
        for player in max_level_players:
            player.decrease_bet_level(max_levels_difference)
            player.increase_stack(max_levels_difference)