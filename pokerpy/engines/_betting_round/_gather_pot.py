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
    Gathers the chips from the users bet levels into the central pot. Bet levels are iterated from
    lowest to highest to gather them into the central pot. After gathering each pot, a new side pot
    may be added based on the following rules:
    - If no player is all-in for the gathered pot, no side pot is added and this is the last
      iteration.
    - If any player is all-in for the gathered pot and any other players still have chips to be
      gathered, a new side pot is created and they are assigned to it to gather their chips in the
      next iteration.
    - If any player is all-in for the gathered pot and there are no more chips to be gathered, but
      some players are still able to play, then a new side pot is created and they are assigned to
      it, being this the last iteration. 
    - If any player is all-in for the gathered pot, but there are neither chips to gather nor
      players still able to play, then no side pot is added and this is the last iteration.
    """

    while table.bettor_players:

        smallest_bet_level = min(player.bet_level for player in table.bettor_players)

        some_participants_go_all_in = any(
            player.stack == 0 for player in table.bettor_players
            if player.bet_level == smallest_bet_level
        )

        for player in table.bettor_players:
            player.decrease_bet_level(smallest_bet_level)
            table.increase_central_pot(smallest_bet_level)

        new_side_pot_participants = table.bettor_players or table.actionable_players

        if some_participants_go_all_in and new_side_pot_participants:
            table.add_side_pot()
            for player in new_side_pot_participants:
                player.increase_pot_index()