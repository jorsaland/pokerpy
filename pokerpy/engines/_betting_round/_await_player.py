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


from pokerpy.logger import logger
from pokerpy.messages import msg_forbidden_action, msg_missing_action
from pokerpy.states import PlayerActionAwait
from pokerpy.structures import Player


def await_player(player: Player, action_ranges: dict[str, range]):

    """
    Awaits for a player's action choice.
    """

    yield (await_state := PlayerActionAwait(player=player, ranges=action_ranges))
    action = await_state.requested_action

    if action is None:
        logger.debug(f'--- skipped action')
        raise RuntimeError(msg_missing_action)

    amount_range = action_ranges.get(action.category)
    if amount_range is None or action.amount not in amount_range:
        logger.debug(f'--- invalid action: {action.category}s {action.amount}')
        raise RuntimeError(msg_forbidden_action)

    return action