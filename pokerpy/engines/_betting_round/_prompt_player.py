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
Defines the function that evaluates if the current player is able to request an action and listens to it.
"""


from typing import TYPE_CHECKING


from pokerpy.exceptions import CloseBettingRoundSignal, JumpToNextPlayerSignal
from pokerpy.messages import (
    signal_all_in_player,
    signal_all_in_stopping_player,
    signal_folded_player,
    signal_folded_stopping_player,
    signal_last_player_in_hand,
    signal_passive_stopping_player,
)
from pokerpy.structures import Player


from ._await_player import await_player
from ._set_action_effects import set_action_effects
if TYPE_CHECKING:
    from ._betting_round import BettingRound


def prompt_player(betting_round: "BettingRound", current_player: Player):

    """
    Evaluates if the current player is able to request an action and listens to it.
    """

    # Close the betting round if there is one player remaining
    if len(betting_round.table.players_in_hand) == 1:
        raise CloseBettingRoundSignal(signal_last_player_in_hand)

    # If the player is folded, jump to the next one (or close the betting round if is also the stopping player)
    if current_player not in betting_round.table.players_in_hand:
        if current_player != betting_round.table.stopping_player:
            raise JumpToNextPlayerSignal(signal_folded_player)
        raise CloseBettingRoundSignal(signal_folded_stopping_player)

    # If the player is folded or all-in, jump to the next one (or close the betting round if is also the stopping player)
    if current_player.stack == 0:
        if current_player != betting_round.table.stopping_player:
            raise JumpToNextPlayerSignal(signal_all_in_player)
        raise CloseBettingRoundSignal(signal_all_in_stopping_player)

    # Listen to player until it chooses a valid action
    action = yield from await_player(
        player = current_player,
        table_current_amount = betting_round.table.current_amount,
        smallest_bet_amount = betting_round.table.smallest_bet_amount,
        smallest_raise_amount = betting_round.table.smallest_raise_amount,
        open_fold_allowed = betting_round.open_fold_allowed,
        ignore_invalid_actions = betting_round.ignore_invalid_actions,
    )
    set_action_effects(betting_round=betting_round, player=current_player, action=action)

    # Stop if the current player still is the stopping player
    if current_player == betting_round.table.stopping_player:
        raise CloseBettingRoundSignal(signal_passive_stopping_player)