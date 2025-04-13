"""
Defines the function that determines the name of the hand.
"""


from deprecated.v04 import constants


from .._card import Card
from ._arrange_cards import arrange_cards


def get_category(cards: list[Card]):

    """
    Determines the name of the hand.
    """

    # Convert cards iterable

    hand_tuple = arrange_cards(cards)
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