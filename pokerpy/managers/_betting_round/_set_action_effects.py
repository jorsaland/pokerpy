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
Defines the function that updates statuses according to the chosen action.
"""


from typing import TYPE_CHECKING


from pokerpy.constants import ACTION_FOLD, aggressive_action_names
from pokerpy.logger import get_logger
from pokerpy.structures import Action, Player


if TYPE_CHECKING:
    from ._betting_round import BettingRound


logger = get_logger()


def set_action_effects(*, betting_round: "BettingRound", player: Player, action: Action):

    """
    Updates statuses according to the chosen action.
    """

    if action.amount > 0:
        player.remove_from_stack(action.amount)
        player.add_to_current_amount(action.amount)

    if action.name in aggressive_action_names:
        raise_amount = player.current_amount - betting_round.table.current_amount
        betting_round.table.set_smallest_raise_amount(raise_amount)
        betting_round.table.add_to_current_amount(raise_amount)
        assert (previous_player_in_hand := betting_round.table.get_previous_active_player(player)) is not None
        betting_round.table.set_stopping_player(previous_player_in_hand)

    if action.name == ACTION_FOLD:
        player.set_as_folded()

    logger.info(
        f"{''.join(str(card) for card in player.cards)} {player.name} {action.name.upper()}S {action.amount} "
        f"({player.name}'s current amount: {player.current_amount} | stack: {player.stack})"
    )
    logger.info(f'TABLE CURRENT AMOUNT: {betting_round.table.current_amount}\n')