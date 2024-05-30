"""
Defines the class that represents a poker hand.
"""


from collections.abc import Iterable
from typing import NewType


from pokerpy import constants
from pokerpy.messages import (
    hand_not_all_card_instances_message,
    hand_not_iterable_object_cards_message,
)


from .._card import Card

from ._arrange_cards import arrange_cards
from ._get_category import get_category


HandTuple = NewType('HandTuple', tuple[Card])


class Hand:


    """
    Represents a poker hand.
    """


    def __init__(self, cards: Iterable[Card]):

        # Check input type
        if not isinstance(cards, Iterable):
            raise TypeError(hand_not_iterable_object_cards_message.format(type(cards).__name__))

        cards_list = list(cards)
        if not all(isinstance(card, Card) for card in cards_list):
            raise TypeError(hand_not_all_card_instances_message)

        # Transform input
        hand_tuple = arrange_cards(cards_list)
        category = get_category(cards_list)
        
        # Static attributes
        self._cards = hand_tuple
        self._category = category


    @property
    def cards(self):
        return self._cards

    @property
    def category(self):
        return self._category


    def __repr__(self):
        return f'Hand({", ".join(repr(card) for card in self.cards)})'


    def __str__(self):
        return f'<{"".join(str(card) for card in self.cards)}>'


    def __eq__(self, other):

        if not isinstance(other, Hand):
            return NotImplemented
        
        # If both hands have the same values, they are equally good, no matter the suit
        self_values = [card.value for card in self.cards]
        other_values = [card.value for card in other.cards]

        return (self.category == other.category) and (self_values == other_values)

    
    def __gt__(self, other):
        
        if not isinstance(other, Hand):
            return NotImplemented

        # The higher a category is in the categories tuple, the better the hand is
        self_category_index = constants.sorted_hand_categories.index(self.category)
        other_category_index = constants.sorted_hand_categories.index(other.category)

        # Within a hand category, the higher its values are in the values tuple, the better the hand is
        self_values_indices = [constants.sorted_card_values.index(card.value) for card in self.cards]
        other_values_indices = [constants.sorted_card_values.index(card.value) for card in other.cards]
        
        return (self_category_index, self_values_indices) > (other_category_index, other_values_indices)
    
    
    def __ge__(self, other):
        
        if not isinstance(other, Hand):
            return NotImplemented
        
        return (self == other) or (self > other)