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
Defines the class that represents a poker card.
"""


from pokerpy.constants import sorted_card_values_and_suits, unicode_code_point_by_card_suit
from pokerpy.validations import (
    validate_str_card_joker,
    validate_str_card_suit,
    validate_str_card_value,
    validate_type_str,
)


class Card:


    """
    Represents a poker card.
    """


    def __init__(self, value: str, suit: str):

        validate_type_str(value)
        validate_type_str(suit)

        value = value.upper()
        suit = suit.lower()

        validate_str_card_joker(value, suit)
        validate_str_card_value(value)
        validate_str_card_suit(suit)

        self._value = value
        self._suit = suit


    @property
    def value(self):
        "Rank of the card (numbers from 2 to 10, jacks, queens, kings and aces)."
        return self._value
    
    @property
    def suit(self):
        "Symbol paired with the value (clubs, diamonds, hearts and spades)."
        return self._suit


    def __repr__(self):
        return f'Card(value={self.value}, suit={self.suit})'


    def __str__(self):
        unicode_code_point = unicode_code_point_by_card_suit[self.suit]
        pretty_suit = chr(unicode_code_point)
        return f'[{self.value}{pretty_suit}]'


    def __hash__(self):
        return hash((Card, self.value, self.suit))


    def __eq__(self, other):

        if not isinstance(other, Card):
            return NotImplemented

        return (self.value == other.value) and (self.suit == other.suit)


    def get_deck_position(self):
        """
        Retrieves the position of the card in a deck that is sorted from lowest value to highest
        value, and from lowest suit to highest suit.
        """
        value_and_suit = (self.value, self.suit)
        return sorted_card_values_and_suits.index(value_and_suit)