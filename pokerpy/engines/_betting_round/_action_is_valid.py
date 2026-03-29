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
Defines the function that verifies if a betting-round action is valid according to previous actions.
"""


from pokerpy.constants import (
    ACTION_CALL,
    ACTION_BET,
    ACTION_RAISE,
)
from pokerpy.structures import Action


from ._get_valid_action_names import get_valid_action_names


def action_is_valid(
    *, action: Action,
    table_current_amount: int,
    player_current_amount: int,
    player_stack: int,
    smallest_bet_amount: int,
    smallest_raise_amount: int,
    open_fold_allowed: bool
):

    """
    Verifies if a betting-round action is valid according to previous actions.
    """

    # Calculate amount that player has to call
    amount_to_call = table_current_amount - player_current_amount

    # Validate action name makes sense in context
    valid_action_names = get_valid_action_names(
        amount_to_call = amount_to_call,
        stack = player_stack,
        open_fold_allowed = open_fold_allowed,
    )
    if action.name not in valid_action_names:
        return False

    # Validate player has enough chips
    if action.amount > player_stack:
        return False

    # Validate calling amount
    if action.name == ACTION_CALL:
        if player_stack >= amount_to_call:
            return action.amount == amount_to_call
        return action.amount == player_stack ## all-in

    # Validate betting amount
    if action.name == ACTION_BET:
        if player_stack >= smallest_bet_amount:
            return action.amount >= smallest_bet_amount
        return action.amount == player_stack ## all-in

    # Validate raising amount
    if action.name == ACTION_RAISE:
        if action.amount <= amount_to_call: ## the action amount must be larger than the amount to call (otherwise would be call)
            return False
        if player_stack >= amount_to_call + smallest_raise_amount:
            return action.amount - amount_to_call >= smallest_raise_amount
        return action.amount == player_stack ## all-in

    return True