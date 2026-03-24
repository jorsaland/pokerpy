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


from pokerpy.constants import (
    full_sorted_values_and_suits,
    sorted_card_suits,
    sorted_card_values,
    unicode_code_point_by_card_suit,
)
from pokerpy.messages import (
    msg_invalid_card_suit,
    msg_invalid_card_value,
    msg_not_str,
    msg_wildcard,
)


class Card:


    """
    Represents a poker card.
    """


    def __init__(self, value: str, suit: str):

        # Check types
        if not isinstance(value, str):
            raise TypeError(msg_not_str.format(type(value).__name__))
        if not isinstance(suit, str):
            raise TypeError(msg_not_str.format(type(suit).__name__))

        # Convert cases
        value = value.upper()
        suit = suit.lower()

        # Validate and convert input
        if 'joker' in (value.lower(), suit.lower()):
            raise ValueError(msg_wildcard)
        if value not in sorted_card_values:
            message = msg_invalid_card_value.format(', '.join(sorted_card_values))
            raise ValueError(message)
        if suit not in sorted_card_suits:
            message = msg_invalid_card_suit.format(', '.join(sorted_card_suits))
            raise ValueError(message)

        # Fixed variables
        self._value = value
        self._suit = suit


    @property
    def value(self):
        return self._value
    
    @property
    def suit(self):
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
        Gets the card position in a sorted deck.
        """

        value_and_suit = (self.value, self.suit)
        return full_sorted_values_and_suits.index(value_and_suit)