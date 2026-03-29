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


def get_valid_action_names(*, amount_to_call: int, stack: int, open_fold_allowed: bool):

    """
    Lists the valid possible actions depending on previous actions taken during the betting round.
    """

    if amount_to_call != 0:
        if amount_to_call >= stack:
            valid_action_names = [ACTION_FOLD, ACTION_CALL]
        else:
            valid_action_names = [ACTION_FOLD, ACTION_CALL, ACTION_RAISE]

    else:
        if open_fold_allowed:
            valid_action_names = [ACTION_CHECK, ACTION_BET, ACTION_FOLD]
        else:
            valid_action_names = [ACTION_CHECK, ACTION_BET]

    return valid_action_names