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


"Defines the function that runs the round where all players place antes"


from pokerpy.logger import logger, wrap_middle_log
from pokerpy.structures import Table


from .._betting_round._gather_pot import gather_pot
from ._display_status import display_cards_and_money


def ante_round(table: Table, *, ante: int):

    "Runs the round where all players place antes."

    logger.info(wrap_middle_log('placing antes'))

    logger.info(f'Ante size: {ante}')
    for player in table.players:
        amount = ante if player.stack > ante else player.stack
        player.decrease_stack(amount)
        player.increase_bet_level(amount)

    gather_pot(table)
    display_cards_and_money(table)
    logger.info(wrap_middle_log('antes placed', new_line=True))