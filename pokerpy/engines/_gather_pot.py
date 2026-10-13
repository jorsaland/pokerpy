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
Defines the function that gathers the chips from the users into the central pot.
"""


from pokerpy.structures import Table


def gather_pot(table: Table):

    """
    Gathers the chips from the users into the central pot.
    """

    while table.bettor_players:

        must_add_side_pot = True

        smallest_chip_level = min(player.bet_level for player in table.bettor_players)
        if all(player.is_folded for player in table.players if player.bet_level == smallest_chip_level):
            must_add_side_pot = False

        for player in table.bettor_players:
            player.decrease_bet_level(smallest_chip_level)
            table.increase_central_pot(smallest_chip_level)

        if table.bettor_players and must_add_side_pot:
            table.add_side_pot()
            for player in table.bettor_players:
                player.increase_pot_index()