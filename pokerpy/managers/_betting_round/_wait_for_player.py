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
Defines the function that waits for a player to choose a valid action.
"""


from pokerpy.logger import get_logger
from pokerpy.messages import msg_forbidden_action
from pokerpy.structures import Player


from ._action_is_valid import action_is_valid



logger = get_logger()


def wait_for_player(
    *, player: Player,
    table_current_amount: int,
    smallest_bet: int,
    smallest_raising_amount: int,
    open_fold_allowed: bool,
    ignore_invalid_actions: bool
):

    """
    Waits for a player to choose a valid action. Once the generator ends, returns the chosen action.
    """

    # Player keeps its turn until selects a valid action

    while True:

        # Await for player's action

        yield player

        # Determine whether action is valid or not

        action = player.requested_action
        if action is None:
            continue

        if action_is_valid(
            action = action,
            table_current_amount = table_current_amount,
            player_current_amount = player.current_amount,
            player_stack = player.stack,
            smallest_bet = smallest_bet,
            smallest_raising_amount = smallest_raising_amount,
            open_fold_allowed = open_fold_allowed
        ):
            break

        logger.debug(f'--- invalid action: {action.name}s {action.amount}')
        if not ignore_invalid_actions:
            raise RuntimeError(msg_forbidden_action)

    # Reset player and return requested action

    player.reset_action()
    return action