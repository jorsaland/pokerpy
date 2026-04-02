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
Defines the function that retrieves the valid actions according to the betting round current status.
"""


from pokerpy.constants import (
    ACTION_BET,
    ACTION_CALL,
    ACTION_CHECK,
    ACTION_FOLD,
    ACTION_RAISE,
)


def get_valid_actions(
    *,
    player_stack: int,
    player_current_amount: int,
    player_has_played: bool,
    current_level: int,
    complete_current_level: int,
    full_bet: int,
    full_raise_increase: int,
    open_fold_allowed: bool
):

    """
    Retrieves the valid actions according to the betting round current status.
    """

    assert player_stack >= 0
    assert player_current_amount >= 0
    assert current_level >= 0
    assert complete_current_level >= 0
    assert full_bet > 0
    assert full_raise_increase > 0

    assert full_raise_increase >= full_bet
    assert (complete_current_level + full_raise_increase) > current_level >= complete_current_level

    amount_to_call = current_level - player_current_amount
    amount_to_full_level = complete_current_level - player_current_amount
    amount_to_full_raise = amount_to_full_level + full_raise_increase

    def get_fold_range():
        return range(0, 1)

    def get_check_range():
        return range(0, 1)
    
    def get_call_range():
        if player_stack > amount_to_call:
            return range(amount_to_call, amount_to_call + 1)
        return range(player_stack, player_stack + 1)

    def get_bet_range():
        if player_stack > full_bet:
            return range(full_bet, player_stack + 1)
        elif player_stack > amount_to_call:
            return range(player_stack, player_stack + 1)

    def get_raise_range():
        if player_stack > amount_to_full_raise:
            return range(amount_to_full_raise, player_stack + 1)
        elif player_stack > amount_to_call:
            return range(player_stack, player_stack + 1)

    amount_range_by_action: dict[str, range|None] = {}

    # passive actions
    if amount_to_call > 0:
        amount_range_by_action[ACTION_CALL] = get_call_range()
        amount_range_by_action[ACTION_FOLD] = get_fold_range()
    else:
        amount_range_by_action[ACTION_CHECK] = get_check_range()
        if open_fold_allowed:
            amount_range_by_action[ACTION_FOLD] = get_fold_range()

    # the player stack may be enough only to call
    if player_stack <= amount_to_call:
        return amount_range_by_action

    # a player who has not played yet and has enough chips, always can take an aggressive action
    if not player_has_played:
        if amount_to_full_level == 0:
            amount_range_by_action[ACTION_BET] = get_bet_range()
        else:
            amount_range_by_action[ACTION_RAISE] = get_raise_range()
        return amount_range_by_action

    # a player who has already played and is not facing a full bet/raise, cannot take an aggressive action
    if amount_to_full_level == 0:
        return amount_range_by_action

    # in any other case, it counts as a raise
    amount_range_by_action[ACTION_RAISE] = get_raise_range()
    return amount_range_by_action