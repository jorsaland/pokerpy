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


from pokerpy.exceptions import CloseBettingRoundSignal, JumpToNextPlayerSignal
from pokerpy.messages import (
    signal_all_in_player,
    signal_all_in_stopping_player,
    signal_folded_player,
    signal_folded_stopping_player,
    signal_last_player_in_hand,
    signal_passive_stopping_player,
)
from pokerpy.structures import Table


from ._await_player import await_player
from ._set_action_effects import set_action_effects


def prompt_player(
        *,
        table: Table,
        open_fold_allowed: bool,
        raise_invalid_actions: bool
    ):

    """
    Evaluates if the current player is able to request an action and listens to it.
    """

    # Close the betting round if every player is folded
    if len(table.live_players) == 1:
        raise CloseBettingRoundSignal(signal_last_player_in_hand)

    # If the player is folded, jump to the next one (or close the betting round if is also the stopping player)
    if table.current_player.is_folded:
        if table.current_player == table.stopping_player:
            raise CloseBettingRoundSignal(signal_folded_stopping_player)
        raise JumpToNextPlayerSignal(signal_folded_player)

    # If the player is folded or all-in, jump to the next one (or close the betting round if is also the stopping player)
    if table.current_player.stack == 0:
        if table.current_player == table.stopping_player:
            raise CloseBettingRoundSignal(signal_all_in_stopping_player)
        raise JumpToNextPlayerSignal(signal_all_in_player)

    # Listen to player until it chooses a valid action
    action = yield from await_player(
        player = table.current_player,
        bet_level = table.bet_level,
        full_bet_level = table.full_bet_level,
        min_bet = table.min_bet,
        min_raise_increase = table.min_raise_increase,
        is_last_actionable_player = (table.current_player in table.actionable_players and len(table.actionable_players) == 1),
        open_fold_allowed = open_fold_allowed,
        raise_invalid_actions = raise_invalid_actions,
    )
    set_action_effects(table=table, player=table.current_player, action=action)

    # Stop if the current player still is the stopping player
    if table.current_player == table.stopping_player:
        raise CloseBettingRoundSignal(signal_passive_stopping_player)