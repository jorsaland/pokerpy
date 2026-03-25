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
Defines the function that alternates players within the betting round.
"""


from typing import TYPE_CHECKING


from pokerpy.constants import ACTION_FOLD, aggressive_action_names
from pokerpy.logger import get_logger


from ._wait_for_player import wait_for_player
if TYPE_CHECKING:
    from ._betting_round import BettingRound


logger = get_logger()


def alternate_players(betting_round: "BettingRound"):

    """
    Alternates players within the betting round. Once the generator ends, returns whether round must stop or not.
    """

    round_must_stop = False

    # All players are itered but only active ones are allowed to act
    for player in betting_round.table.players:

        # Stop if there is one player remaining
        if len(betting_round.table.players_in_hand) == 1:
            round_must_stop = True
            break

        # Jump until the starting player has to play
        if betting_round.table.players.index(player) < betting_round.table.players.index(betting_round.starting_player):
            continue

        # Determine whether player should be allowed to choose an action
        if player in betting_round.table.players_in_hand:
            if player.stack == 0:
                if player == betting_round.stopping_player:
                    round_must_stop = True
                    break
                continue
        else:
            if player == betting_round.stopping_player:
                round_must_stop = True
                break
            continue

        # Player keeps its turn until selects a valid action
        action = yield from wait_for_player(
            player = player,
            table_current_amount = betting_round.table.current_amount,
            smallest_bet = betting_round.smallest_bet,
            smallest_raising_amount = betting_round.smallest_rising_amount,
            open_fold_allowed = betting_round.open_fold_allowed,
            ignore_invalid_actions = betting_round.ignore_invalid_actions,
        )

        # Set consequences of aggressive actions
        if action.name in aggressive_action_names:
            raising_amount = player.current_amount - betting_round.table.current_amount
            betting_round.overwrite_smallest_rising_amount(raising_amount) 
            betting_round.table.add_to_current_amount(raising_amount)
            player_index = betting_round.table.players.index(player)
            stopping_player = betting_round.table.players[player_index-1] if player_index != 0 else betting_round.table.players[-1]
            betting_round.set_stopping_player(stopping_player)

        # Determine whether the player becomes inactive or not
        if action.name == ACTION_FOLD:
            player.fold()

        # Log table current amount before breaking (or not) in the next block
        logger.info(f'TABLE CURRENT AMOUNT: {betting_round.table.current_amount}\n')

        # Stop if the current player still is the stopping player
        if player == betting_round.stopping_player:
            round_must_stop = True
            break

    return round_must_stop