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

    player_bet_level = player.bet_level
    table_bet_level = table.bet_level
    table_full_bet_level = table.full_bet_level
    min_raise_increase = table.min_raise_increase

    player.mark_has_played()

    if action.category == ACTION_FOLD:

        player.mark_is_folded()

    if action.amount > 0:

        player.decrease_stack(action.amount)
        player.increase_bet_level(action.amount)

    if action.category in (ACTION_BET, ACTION_RAISE):

        new_current_amount = player_bet_level + action.amount
        raise_increase = new_current_amount - table_bet_level
        new_level = table_full_bet_level + raise_increase
        table.set_bet_level(new_level)

        if new_level >= table_full_bet_level + min_raise_increase:
            table.set_full_bet_level(new_level)
            if (new_full_raise_increase := new_level - table_full_bet_level) > 0:
                table.set_min_raise_increase(new_full_raise_increase)

        for previous_player in table.iter_players(table.get_previous_player(player), reverse=True):
            if previous_player in table.actionable_players:
                previous_actionable_player = previous_player
                break
        else:
            raise AssertionError

        table.set_stopping_player(previous_actionable_player)

    logger.info(
        f"{''.join(str(card) for card in player.cards)} {player.name} {action.category.upper()}S {action.amount} "
        f"({player.name}'s bet level: {player.bet_level} | stack: {player.stack})"
    )
    logger.info(f'TABLE BET LEVEL: {table.bet_level}\n')