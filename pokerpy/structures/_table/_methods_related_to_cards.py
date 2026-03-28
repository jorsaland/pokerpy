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
Defines the methods related to cards.
"""


from typing import TYPE_CHECKING


from pokerpy.constants import full_sorted_values_and_suits
from pokerpy.messages import msg_not_card_instance, msg_card_not_in_deck, msg_repeated_cards


from .._card import Card
if TYPE_CHECKING:
    from ._table import Table


def method_remove_card_from_deck(self: "Table", card: Card):
    if not isinstance(card, Card):
        raise TypeError(msg_not_card_instance.format(type(card).__name__))
    if card not in self.deck:
        raise ValueError(msg_card_not_in_deck)
    self._deck.remove(card)


def method_assign_common_card(self: "Table", card: Card):
    if not isinstance(card, Card):
        raise TypeError(msg_not_card_instance.format(type(card).__name__))
    if card in self.common_cards:
        raise ValueError(msg_repeated_cards)
    self._common_cards.append(card)


def method_reset_common_cards(self: "Table"):
    self._common_cards.clear()


def method_reset_deck(self: "Table"):
    self._deck.clear()
    self._deck.extend(Card(value, suit) for value, suit in full_sorted_values_and_suits)