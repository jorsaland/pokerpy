"""
Defines messages used to raise errors.
"""


# Type errors
msg_no_players_in_table = "at least one player is expected in the table"
msg_not_action_instance = "an instance of Action is expected, not {}"
msg_not_all_card_instances = "all entries are expected to be Card instances"
msg_not_all_player_instances = "all entries are expected to be Player instances"
msg_not_card_instance = "an instance of Card is expected, not {}"
msg_not_hand_instance = "an instance of Hand is expected, not {}"
msg_not_int = "an integer is expected, not {}"
msg_not_iterable_object = "an iterable object is expected, not {}"
msg_not_list = "a list is expected, not {}"
msg_not_player_instance = "an instance of Player is expected, not {}"
msg_not_str = "a string is expected, not {}"
msg_not_table_instance = "an instance of Table is expected, not {}"

# General value errors
msg_not_positive_or_zero_value = "the value must be positive or zero (received {})"
msg_not_positive_value = "the value must be positive (received {})"
msg_not_zero_value = "the value must be zero (received {})"

# Specific value errors
msg_amount_larger_than_stack = "the amount ({}) cannot be larger than stack ({})"
msg_card_not_in_deck = "the requested card is not in the deck"
msg_invalid_action_name = "invalid action name, must be one of the following: {}"
msg_invalid_card_suit = "invalid card suit, must be be one of the following: {}"
msg_invalid_card_value = "invalid card value, must be one of the following: {}"
msg_not_five_cards_hand = "a hand expects exactly five cards"
msg_player_not_in_table = "player '{}' is not in the table"
msg_repeated_cards = "cards cannot be repeated"
msg_some_players_not_in_table = "some parsed players are not in the table"
msg_wildcard = "we live in a society"

# Runtime errors
msg_betting_round_was_not_completed = "the betting round was closed before being completed"
msg_overloaded_betting_round_message = "some players could not be listened because the betting round already ended"

# Invalid action error
msg_forbidden_action = "the requested action is not allowed in this situation"