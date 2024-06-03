"""
Defines messages used in exceptions.
"""


# Action messages
action_not_str_name_message = "Action name must be str, not '{}'."
action_not_int_amount_message = "Action amount must be int, not '{}'."
action_invalid_name_message = "'{}' is not a valid action name. Please choose one of the following: {}"
action_amount_not_zero_message = "Action '{}' requires amount being equal to zero (received {})."
action_amount_not_more_than_zero_message = "Action '{}' requires amount being more than zero (received {})."

# Player messages
player_not_str_name_message = "Player name must be str, not '{}'."
player_not_action_instance_message = "Player action must be an instance of class Action, not '{}'."
player_not_card_instance_message = "Player card must be an instance of class Card, not '{}'."
player_not_hand_instance_message = "Player hand must be an instance of class Hand, not '{}'."

# Table messages
table_not_list_players_message = "Table players must be list, not '{}'."
table_not_all_player_instances_message = 'All table players must be instances of class Player.'
table_not_player_instance_message = "Player must be an instance of class Player, not '{}'."
table_not_int_cards_count_message = "Attribute 'cards_count' must be int, not '{}'."
table_player_not_in_table_message = "Player '{}' is not in the table."
table_player_already_folded_message = "Player '{}' already folded."
table_not_int_stack_atom_message = "Table stack atom must be int, not '{}'."
table_stack_atom_not_more_than_zero_message = "Stack atom must be more than zero (received {})."

# Betting round messages
betting_round_not_str_name_message = "Betting round name must be str, not '{}'."
betting_round_not_table_instance_message = "Betting round table must be an instance of class Table, not '{}'."
betting_round_exiting_unended_round_message = 'Betting round did not end.'
betting_round_overloaded_round_message = 'Betting round ended before parsing all actions.'
betting_round_already_ended_round_message = 'Betting round has already ended. It cannot start over.'

# Card messages
card_not_str_value_message = "Card value must be str, not '{}'."
card_not_str_suit_message = "Card suit must be str, not '{}'."
card_invalid_suit_message = 'Card suits must be one of these: {}'
card_invalid_value_message = 'Card values must be one of these: {}'
card_joker_message = 'We live in a society.'

# Hand messages
hand_not_iterable_object_cards_message = "Hand cards must be an iterable object, not '{}'."
hand_not_all_card_instances_message = 'All hand cards must be instances of class Card.'
hand_not_five_cards_message = 'Hands must have exactly five cards.'
hand_repeated_cards_message = 'Cards in a hand cannot be repeated.'