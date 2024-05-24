"""
Defines the class that represents a poker hand.
"""


from collections.abc import Iterable
from typing import NewType


from pokerpy import constants
from pokerpy.messages import not_five_cards_hand_message, repeated_cards_hand_message


from ._card import Card


HandTuple = NewType('HandTuple', tuple[Card])


class Hand:


    """
    Represents a poker hand.
    """


    def __init__(self, cards: Iterable[Card]):
        
        # Transform input
        hand_tuple = self.arrange_cards(cards)
        category = self.get_category(hand_tuple)
        
        # Static attributes
        self.cards = hand_tuple
        self.category = category


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
    

    @classmethod
    def arrange_cards(cls, cards: Iterable[Card]):

        """
        Arranges a list of cards from most to least repeated and from highest to lowest value.
        """

        # Validate input

        cards_list = list(cards)
        if len(cards_list) != 5:
            raise ValueError(not_five_cards_hand_message)
        if len(cards) != len(set(cards)):
            raise ValueError(repeated_cards_hand_message)

        # Convert to list and sort from higher to lower value

        cards_list = list(cards)
        cards_list.sort(key=Card.get_deck_position, reverse=True)

        # Arrange cards in a special way if hand is a five-to-ace straight

        wrongly_sorted_five_to_ace = [
            constants.ACES,
            constants.FIVES,
            constants.FOURS,
            constants.THREES,
            constants.DEUCES,
        ]
        
        if [card.value for card in cards_list] == wrongly_sorted_five_to_ace: # special sorting case --> A5432 becomes 5432A
            cards_list.append(cards_list.pop(0))
            return HandTuple(tuple(cards_list))
        
        # Otherwise, arrange cards from most to least repeated value

        card_values = [card.value for card in cards_list]
        counts_by_value = {value: card_values.count(value) for value in card_values}

        cards_list.sort(reverse=True, key=(lambda card: counts_by_value[card.value]))
        return HandTuple(tuple(cards_list))


    @classmethod
    def get_category(cls, cards: Iterable[Card]):

        """
        Takes an iterable object with arranged cards (see _arrange_hand_cards.py) and determines the name
        of the hand.
        """

        # Convert cards iterable

        hand_tuple = cls.arrange_cards(cards)
        merged_card_values = ''.join(card.value for card in hand_tuple) # example --> 'JT987'

        # Check if cards match flush

        unique_suits = {card.suit for card in hand_tuple}
        cards_match_flush = (len(unique_suits) == 1)

        # Check if cards match straight

        merged_full_straight = ''.join(reversed(constants.sorted_card_values)) + constants.ACES ## this is literally --> 'AKQJT98765432A'
        cards_match_straight = (merged_card_values in merged_full_straight) ## membership comparison between strings --> '76543' is contained in 'AKQJT98765432A'

        # Match flushes and straights

        if cards_match_flush and cards_match_straight:
            if hand_tuple[0].value == constants.ACES:
                return constants.ROYAL_FLUSH
            return constants.STRAIGHT_FLUSH

        if cards_match_flush:
            return constants.FLUSH

        if cards_match_straight:
            return constants.STRAIGHT

        # Match other categories

        value_counts = {merged_card_values.count(value) for value in merged_card_values}

        if 4 in value_counts:
            return constants.FOUR_OF_A_KIND

        if 3 in value_counts:
            if 2 in value_counts:
                return constants.FULL_HOUSE
            return constants.THREE_OF_A_KIND

        if 2 in value_counts:
            if len(set(merged_card_values)) == 3: ## 2 pairs and 1 unpaired card
                return constants.TWO_PAIR
            return constants.ONE_PAIR ## 1 pair and 3 single cards

        return constants.HIGH_CARD