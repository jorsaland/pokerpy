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
Defines the function that lists the valid possible actions depending on previous actions taken during the betting round.
"""


from pokerpy.constants import (
    ACTION_FOLD,
    ACTION_CALL,
    ACTION_CHECK,
    ACTION_BET,
    ACTION_RAISE,
)


def get_valid_action_names(
        *,
        stack: int,
        amount_to_call: int,
        table_current_amount: int,
        smallest_bet_amount: int,
        smallest_raise_amount: int,
        open_fold_allowed: bool
    ):

    """
    Lists the valid possible actions depending on previous actions taken during the betting round.
    """

    # No previous bet/raise
    if amount_to_call == 0:
        if open_fold_allowed:
            return [ACTION_CHECK, ACTION_BET, ACTION_FOLD]
        return [ACTION_CHECK, ACTION_BET]

    # Not enough chips for a full call
    if amount_to_call >= stack:
        return [ACTION_FOLD, ACTION_CALL]

    # Facing an incomplete bet/raise
    if amount_to_call < smallest_raise_amount:
        if table_current_amount < smallest_bet_amount:
            return [ACTION_FOLD, ACTION_CALL, ACTION_BET] ## facing an incomplete bet, completing a bet is an option
        return [ACTION_FOLD, ACTION_CALL] ## facing an incomplete raise, re-raising is locked

    # Enough chips for a full raise
    return [ACTION_FOLD, ACTION_CALL, ACTION_RAISE]