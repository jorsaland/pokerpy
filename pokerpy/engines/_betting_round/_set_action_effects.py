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


from pokerpy.constants import ACTION_BET, ACTION_FOLD, ACTION_RAISE
from pokerpy.logger import get_logger
from pokerpy.structures import Action, Player, Table


logger = get_logger()


def set_action_effects(*, table: Table, player: Player, action: Action):

    """
    Updates statuses according to the chosen action.
    """

    player_current_amount = player.amount
    current_level = table.amount_level
    complete_current_level = table.full_amount_level
    full_raise_increase = table.full_raise_increase

    player.mark_has_played()

    if action.category == ACTION_FOLD:
        player.mark_is_folded()

    if action.amount > 0:
        player.decrease_stack(action.amount)
        player.increase_amount(action.amount)
        player.increase_pot_participation(action.amount)

    if action.category in (ACTION_BET, ACTION_RAISE):
        new_current_amount = player_current_amount + action.amount
        raise_increase = new_current_amount - current_level
        new_level = complete_current_level + raise_increase
        table.set_amount_level(new_level)
        if new_level >= complete_current_level + full_raise_increase:
            table.set_full_amount_level(new_level)
            if (new_full_raise_increase := new_level - complete_current_level) > 0:
                table.set_full_raise_increase(new_full_raise_increase)
        assert (previous_player_in_hand := table.get_previous_active_player(player)) is not None
        table.set_stopping_player(previous_player_in_hand) 

    logger.info(
        f"{''.join(str(card) for card in player.cards)} {player.name} {action.category.upper()}S {action.amount} "
        f"({player.name}'s current amount: {player.amount} | stack: {player.stack})"
    )
    logger.info(f'TABLE CURRENT LEVEL: {table.amount_level}\n')