"""
Defines messages used in exceptions.
"""


# Action messages
action_msg_invalid_name = "'{}' is not a valid action name. Please choose one of the following: {}"
action_msg_not_positive_amount = "Action '{}' requires amount being more than zero (received {})."
action_msg_not_int_amount = "Action amount must be int, not '{}'."
action_msg_not_str_name = "Action name must be str, not '{}'."
action_msg_not_zero_amount = "Action '{}' requires amount being equal to zero (received {})."

# Player messages
player_msg_amount_larger_than_stack = "Amount ({}) cannot be larger than stack ({})."
player_msg_not_action_instance = "Player action must be an instance of class Action, not '{}'."
player_msg_not_card_instance = "Player card must be an instance of class Card, not '{}'."
player_msg_not_hand_instance = "Player hand must be an instance of class Hand, not '{}'."
player_msg_not_int_amount = "Amount must be int, not '{}'."
player_msg_not_int_stack = "Player stack must be int, not '{}'."
player_msg_not_positive_stack = "The stack must be positive (received {})."
player_msg_not_positive_or_zero_amount = "The amount must be positive or zero (received {})."
player_msg_not_str_name = "Player name must be str, not '{}'."

# Table messages
table_msg_not_all_player_instances = 'All table players must be instances of class Player.'
table_msg_not_int_cards_count = "Attribute 'cards_count' must be int, not '{}'."
table_msg_not_int_central_pot = "Table central pot amount increase must be int, not '{}'."
table_msg_not_int_current_amount = "Table amount increase must be int, not '{}'."
table_msg_not_int_smallest_bet = "Table smallest bet must be int, not '{}'."
table_msg_not_int_smallest_raise = "Table smallest raising amount increase must be int, not '{}'."
table_msg_not_list_players = "Table players must be list, not '{}'."
table_msg_not_player_instance = "Player must be an instance of class Player, not '{}'."
table_msg_not_positive_or_zero_amount = "The amount must be positive or zero (received {})."
table_msg_not_positive_smallest_bet = "The smallest valid bet must be positive (received {})."
table_msg_not_positive_smallest_raise = "The amount must be positive (received {})."
table_msg_player_already_folded = "Player '{}' already folded."
table_msg_player_not_in_table = "Player '{}' is not in the table."

# Betting round messages
betting_round_msg_already_ended_round = 'Betting round has already ended. It cannot start over.'
betting_round_msg_exiting_unended_round = 'Betting round did not end.'
betting_round_msg_invalid_action = 'The requested action is not allowed: {}.'
betting_round_msg_not_starting_player_instance = "Betting round starting player must be an instance of class Player, not '{}'."
betting_round_msg_not_stopping_player_instance = "Betting round stopping player must be an instance of class Player, not '{}'."
betting_round_msg_not_str_name = "Betting round name must be str, not '{}'."
betting_round_msg_not_table_instance = "Betting round table must be an instance of class Table, not '{}'."
betting_round_msg_overloaded_round = 'Betting round ended before parsing all actions.'

# Card messages
card_msg_invalid_suit = 'Card suits must be one of these: {}'
card_msg_invalid_value = 'Card values must be one of these: {}'
card_msg_joker = 'We live in a society.'
card_msg_not_str_suit = "Card suit must be str, not '{}'."
card_msg_not_str_value = "Card value must be str, not '{}'."

# Hand messages
hand_msg_cards_not_iterable_object = "Hand cards must be an iterable object, not '{}'."
hand_msg_not_all_card_instances = 'All hand cards must be instances of class Card.'
hand_msg_not_five_cards = 'Hands must have exactly five cards.'
hand_msg_repeated_cards = 'Cards in a hand cannot be repeated.'