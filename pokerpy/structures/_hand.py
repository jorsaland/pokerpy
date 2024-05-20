"""
Defines the class that represents a poker hand.
"""


from collections.abc import Iterable


from pokerpy.messages import not_five_cards_hand_message, repeated_cards_hand_message


from ._card import Card


class Hand:


    """
    Represents a poker hand.
    """


    def __init__(self, cards: Iterable[Card]):

        # Validate input
        cards_list = list(cards)
        if len(cards_list) != 5:
            raise ValueError(not_five_cards_hand_message)
        if len(cards) != len(set(cards)):
            raise ValueError(repeated_cards_hand_message)
        
        # Input variables
        self.cards = tuple(cards)