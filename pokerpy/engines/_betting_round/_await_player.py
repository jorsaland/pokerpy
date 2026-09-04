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
Defines the function that listens to a player until it chooses a valid action.
"""


from pokerpy.logger import get_logger
from pokerpy.messages import msg_forbidden_action
from pokerpy.structures import Player


from ._get_valid_actions import get_valid_actions


logger = get_logger()


def await_player(
    *, player: Player,
    amount_level: int,
    full_amount_level: int,
    full_bet: int,
    full_raise_increase: int,
    is_last_active_player: bool,
    open_fold_allowed: bool,
    raise_invalid_actions: bool
):

    """
    Listens to a player until it chooses a valid action.
    """

    # Player keeps its turn until selects a valid action

    while True:

        # Await for player's action

        yield player

        # Determine whether action is valid or not

        action = player.requested_action
        if action is None:
            continue

        amount_range_by_action = get_valid_actions(
            player_stack = player.stack,
            player_bet_level = player.bet_level,
            bet_level = amount_level,
            full_bet_level = full_amount_level,
            min_bet = full_bet,
            min_raise_increase = full_raise_increase,
            player_has_played = player.has_played,
            is_last_active_player = is_last_active_player,
            open_fold_allowed = open_fold_allowed,
        )
        amount_range = amount_range_by_action.get(action.category)
        if amount_range is not None and action.amount in amount_range:
            break

        logger.debug(f'--- invalid action: {action.category}s {action.amount}')
        if raise_invalid_actions:
            raise RuntimeError(msg_forbidden_action)

    # Reset player and return requested action

    player.clear_action()
    return action