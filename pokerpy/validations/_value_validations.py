
"Defines the function that validates values."


from collections.abc import Iterable
from typing import TYPE_CHECKING


from pokerpy import constants, messages
if TYPE_CHECKING:
    from pokerpy import structures


def validate_card_in_deck(card: "structures.Card", deck: Iterable["structures.Card"]):

    "Validates a card is in the deck."

    if card not in deck:
        raise ValueError(messages.msg_card_not_in_deck)


def validate_int_amount_smaller_than_bet_level(amount: int, bet_level: int):

    "Validates an integer amount is smaller than the bet level."

    if amount > bet_level:
        raise ValueError(messages.msg_amount_larger_than_bet_level.format(amount, bet_level))


def validate_int_amount_smaller_than_stack(amount: int, stack: int):

    "Validates an integer amount is smaller than the stack."

    if amount > stack:
        raise ValueError(messages.msg_amount_larger_than_stack.format(amount, stack))


def validate_int_positive(amount: int):

    "Validates an integer is positive."

    if amount <= 0:
        raise ValueError(messages.msg_not_positive_value.format(amount))


def validate_int_positive_or_zero(amount: int):

    "Validates an integer is positive or zero."

    if amount < 0:
        raise ValueError(messages.msg_not_positive_or_zero_value.format(amount))


def validate_int_zero(amount: int):

    "Validates an integer is zero."

    if amount != 0:
        raise ValueError(messages.msg_not_zero_value.format(amount))


def validate_iterable_5_cards_hand(cards: Iterable["structures.Card"]):

    "Validates a hand contains exactly five cards."

    if len(cards) != 5:
        raise ValueError(messages.msg_not_five_cards_hand)


def validate_iterable_not_repeated_cards(cards: Iterable["structures.Card"]):

    "Validates cards in a set are not repeated."

    if len(cards) != len(set(cards)):
        raise ValueError(messages.msg_repeated_cards)


def validate_iterable_not_contains_card(card: "structures.Card", cards: Iterable["structures.Card"]):

    "Validates a card is not in a card set."

    if card in cards:
        raise ValueError(messages.msg_repeated_cards)


def validate_player_in_table(player: "structures.Player", table: Iterable["structures.Player"]):

    "Validates a player is in the table."

    if player not in table:
        raise ValueError(messages.msg_player_not_in_table.format(player.name))


def validate_not_empty_table(players: Iterable["structures.Player"]):

    "Validates a table is not empty."

    if not players:
        raise ValueError(messages.msg_no_players_in_table)


def validate_str_action_category(category: str):

    "Validates an action category is in a valid option."

    if category not in constants.possible_action_names:
        raise ValueError(
            messages.msg_invalid_action_name.format(', '.join(constants.possible_action_names))
        )


def validate_str_card_joker(value: str, suit: str):

    "Validates a card value or suit is not the wildcard."

    if 'joker' in (value.lower(), suit.lower()):
        raise ValueError(messages.msg_wildcard)


def validate_str_card_suit(suit: str):

    "Validates a card suit is in a valid option."

    if suit not in constants.sorted_card_suits:
        raise ValueError(
            messages.msg_invalid_card_suit.format(', '.join(constants.sorted_card_suits))
        )


def validate_str_card_value(value: str):

    "Validates a card value is in a valid option."

    if value not in constants.sorted_card_values:
        raise ValueError(
            messages.msg_invalid_card_value.format(', '.join(constants.sorted_card_values))
        )