"""
Defines the class that represents a poker card.
"""


from pokerpy.constants import (
    full_sorted_values_and_suits,
    sorted_card_suits,
    sorted_card_values,
    unicode_code_point_by_card_suit,
)
from pokerpy.messages import invalid_card_suit_message, invalid_card_value_message, joker_card_message


class Card:


    """
    Represents a poker card.
    """


    def __init__(self, value: str, suit: str):

        # Convert cases
        value = value.upper()
        suit = suit.lower()

        # Validate and convert input
        if 'joker' in [value.lower(), suit.lower()]:
            raise ValueError(joker_card_message)
        if value not in sorted_card_values:
            message = invalid_card_value_message.format(valid_values=', '.join(sorted_card_values))
            raise ValueError(message)
        if suit not in sorted_card_suits:
            message = invalid_card_suit_message.format(valid_suits=', '.join(sorted_card_suits))
            raise ValueError(message)

        # Input variables
        self.value = value
        self.suit = suit


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
            return False

        return (self.value == other.value) and (self.suit == other.suit)


    def get_deck_position(self):

        """
        Gets the card position in a sorted deck.
        """

        value_and_suit = (self.value, self.suit)
        return full_sorted_values_and_suits.index(value_and_suit)