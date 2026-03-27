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
Defines the methods to reset states.
"""


from typing import TYPE_CHECKING


from pokerpy.constants import full_sorted_values_and_suits


from .._card import Card
if TYPE_CHECKING:
    from ._table import Table


def method_reset_betting_round_states(self: "Table"):
    self._smallest_raise_amount = self.smallest_bet_amount
    self._current_amount = 0
    self._stopping_player = self.get_previous_player(self.starting_player)


def method_reset_cycle_states(self: "Table"):
    self.reset_betting_round_states()
    self._deck.clear()
    self._deck.extend(Card(value, suit) for value, suit in full_sorted_values_and_suits)
    self._common_cards.clear()
    self._central_pot = 0
