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


from deprecated.v06.exceptions import CloseBettingRoundSignal, JumpToNextPlayerSignal
from deprecated.v06.messages import (
    signal_all_in_player,
    signal_all_in_stopping_player,
    signal_folded_player,
    signal_folded_stopping_player,
    signal_last_player_in_hand,
    signal_passive_stopping_player,
    signal_no_further_action_possible,
)
from deprecated.v06.structures import Table


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

    if len(table.live_players) == 1:
        raise CloseBettingRoundSignal(signal_last_player_in_hand)

    # An edge case may happen when the small blind is all-in and every other player folds. Then,
    # the big blind is not allowed to play because there are no players to bet (he is the last
    # actionable player) or to call (the bet level difference between the table and the player is
    # zero). If the bet level difference was larger than zero, that would mean that the player
    # still has the choice to call or fold. Another case is where the small blind closes the round
    # because the big blind is already all-in for an amount smaller than the small blind. That
    # player should not be allowed to complete the big blind amount because there is no one to
    # compit against for that amount.
    if (
        len(table.actionable_players) == 1 and
        all(
            player.is_folded for player in table.players
            if player.bet_level > table.current_player.bet_level
        )
    ):
        raise CloseBettingRoundSignal(signal_no_further_action_possible)

    if table.current_player.is_folded:
        if table.current_player == table.stopping_player:
            raise CloseBettingRoundSignal(signal_folded_stopping_player)
        raise JumpToNextPlayerSignal(signal_folded_player)

    if table.current_player.stack == 0:
        if table.current_player == table.stopping_player:
            raise CloseBettingRoundSignal(signal_all_in_stopping_player)
        raise JumpToNextPlayerSignal(signal_all_in_player)

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

    if table.current_player == table.stopping_player:
        raise CloseBettingRoundSignal(signal_passive_stopping_player)