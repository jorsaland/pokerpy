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
from pokerpy.structures import Player, Table


from ._await_player import await_player
from ._set_action_effects import set_action_effects


def prompt_player(
        *,
        table: Table,
        current_player: Player,
        open_fold_allowed: bool,
        ignore_invalid_actions: bool
    ):

    """
    Evaluates if the current player is able to request an action and listens to it.
    """

    # Close the betting round if every player is folded or all-in
    if len(table.players_in_hand) == 1:
        raise CloseBettingRoundSignal(signal_last_player_in_hand)

    # If the player is folded, jump to the next one (or close the betting round if is also the stopping player)
    if current_player.is_folded:
        if current_player != table.stopping_player:
            raise JumpToNextPlayerSignal(signal_folded_player)
        raise CloseBettingRoundSignal(signal_folded_stopping_player)

    # If the player is folded or all-in, jump to the next one (or close the betting round if is also the stopping player)
    if current_player.stack == 0:
        if current_player != table.stopping_player:
            raise JumpToNextPlayerSignal(signal_all_in_player)
        raise CloseBettingRoundSignal(signal_all_in_stopping_player)

    # Listen to player until it chooses a valid action
    action = yield from await_player(
        player = current_player,
        current_level = table.current_level,
        complete_current_level = table.complete_current_level,
        full_bet = table.full_bet,
        full_raise_increase = table.full_raise_increase,
        is_last_active_player = (current_player in table.active_players and len(table.active_players) == 1),
        open_fold_allowed = open_fold_allowed,
        ignore_invalid_actions = ignore_invalid_actions,
    )
    set_action_effects(table=table, player=current_player, action=action)

    # Stop if the current player still is the stopping player
    if current_player == table.stopping_player:
        raise CloseBettingRoundSignal(signal_passive_stopping_player)