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
Defines the functions to reset cycle states.
"""


from pokerpy.messages import msg_not_table_instance
from pokerpy.structures import Table


from ..engines import BettingRound


def reset_cycle_states(table: Table):

    """
    Resets the states for a table and its players to prepare them for a new hand cycle.
    """

    if not isinstance(table, Table):
        raise TypeError(msg_not_table_instance.format(type(table).__name__))

    BettingRound.reset_betting_round_states(table)

    table.reset_deck()
    table.reset_common_cards()
    table.reset_central_pot()

    for player in table.players:
        player.reset_cards()
        player.reset_hand()
        player.unmark_is_folded()