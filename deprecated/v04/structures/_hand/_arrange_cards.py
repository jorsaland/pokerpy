"""
Defines the function that arranges a list of cards from most to least repeated and from highest to lowest value.
"""


from typing import NewType


from deprecated.v04 import constants
from deprecated.v04.messages import hand_not_five_cards_message, hand_repeated_cards_message


from .._card import Card


HandTuple = NewType('HandTuple', tuple[Card])


def arrange_cards(cards: list[Card]):

    """
    Arranges a list of cards from most to least repeated and from highest to lowest value.
    """

    cards = cards.copy()

    # Validate input

    if len(cards) != 5:
        raise ValueError(hand_not_five_cards_message)
    if len(cards) != len(set(cards)):
        raise ValueError(hand_repeated_cards_message)

    # Sort from higher to lower value

    cards.sort(key=Card.get_deck_position, reverse=True)

    # Arrange cards in a special way if hand is a five-to-ace straight

    wrongly_sorted_five_to_ace = [
        constants.ACES,
        constants.FIVES,
        constants.FOURS,
        constants.THREES,
        constants.DEUCES,
    ]
    
    if [card.value for card in cards] == wrongly_sorted_five_to_ace: # special sorting case --> A5432 becomes 5432A
        cards.append(cards.pop(0))
        return HandTuple(tuple(cards))
    
    # Otherwise, arrange cards from most to least repeated value

    card_values = [card.value for card in cards]
    counts_by_value = {value: card_values.count(value) for value in card_values}

    cards.sort(reverse=True, key=(lambda card: counts_by_value[card.value]))
    return HandTuple(tuple(cards))