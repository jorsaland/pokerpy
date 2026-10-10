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
Defines the functions that display status info logs.
"""


from pokerpy.logger import logger, wrap_internal_log
from pokerpy.structures import Table


def display_cards_and_money(table: Table):

    "Displays info logs with the current status of cards and money."

    logger.info(wrap_internal_log())
    logger.info(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | pot: {table.pot} | divided pot: {list(table.split_central_pot)}')

    max_name_length = max(len(player.name) for player in table.players)
    max_stack_length = max(len(str(player.stack)) for player in table.players)

    for player in table.players:
        logger.info(
            f"{'(F)' if player.is_folded else '   '} {player.name.ljust(max_name_length)} | "
            f"cards: {''.join(str(c) for c in player.cards) if player.cards else 'N/A'} | "
            f"stack: {str(player.stack).ljust(max_stack_length)} | "
            f"hand: {f'{str(player.hand)} {player.hand.category}' if player.hand is not None else 'N/A'}"
        )
    logger.info(wrap_internal_log())


def display_pot_indexes(table: Table):

    "Displays info logs with the current status of the split pot."

    logger.info(wrap_internal_log())

    for pot_index, pot in enumerate(table.split_central_pot):
        logger.info(f"{'Main pot' if pot_index == 0 else f'Side pot {pot_index}'} ({pot}):")
        for player in table.live_players:
            if player.pot_index >= pot_index:
                logger.info(f"  {player.name}: hand: {f'{str(player.hand)} {player.hand.category}' if player.hand is not None else 'N/A'}")

    logger.info(wrap_internal_log())