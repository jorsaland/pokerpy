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


from itertools import cycle
from typing import TYPE_CHECKING


from pokerpy.exceptions import CloseBettingRoundSignal, JumpToNextPlayerSignal
from pokerpy.logger import get_logger


from ._prompt_player import prompt_player
if TYPE_CHECKING:
    from ._betting_round import BettingRound


logger = get_logger()


def run_listener(betting_round: "BettingRound"):

    """
    Starts the betting round generator that rotates the player turns.
    """

    # Do not even iterate if there is only one non-folded player who still has a stack to bet
    if len([player for player in betting_round.table.players_in_hand if player.stack > 0]) > 1:

        # All players are itered, prompt_player decides if plays or not
        for player in cycle(betting_round.table.iter_players()):
            betting_round.set_current_player(player)
            if player == betting_round.table.starting_player:
                betting_round.increase_counter()
            try:
                yield from prompt_player(
                    table = betting_round.table,
                    current_player = player,
                    open_fold_allowed = betting_round.open_fold_allowed,
                    ignore_invalid_actions = betting_round.ignore_invalid_actions
                )
            except JumpToNextPlayerSignal:
                continue
            except CloseBettingRoundSignal:
                break
    
    logger.info(f'Number of laps: {betting_round.lap_counts}')
    
    # Move chips to the center of the table
    for player in betting_round.table.players:
        betting_round.table.add_to_central_pot(player.current_amount)