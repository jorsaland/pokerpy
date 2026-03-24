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
Defines the function that starts the betting round generator that rotates the player turns.
"""


from typing import TYPE_CHECKING


from ._alternate_players import alternate_players
if TYPE_CHECKING:
    from ._betting_round import BettingRound


def run_listener(self: "BettingRound"):

    """
    Starts the betting round generator that rotates the player turns.
    """

    # Define state variables
    round_must_stop = False
    lap_counter = 0
            
    # Extend betting round until the last aggressive action has been responded
    while not round_must_stop:

        # Add to lap counter
        lap_counter += 1

        # All players are itered but only active ones are allowed to act
        round_must_stop = yield from alternate_players(self)

        # After the first lap, reset the starting player as the first one on the list
        self._starting_player = self.table.players[0]
    
    # Move chips to the center of the table
    for player in self.table.players:
        self.table.add_to_central_pot(player.current_amount)