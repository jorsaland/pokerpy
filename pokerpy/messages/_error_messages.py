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
player_not_int_current_amount_message = "Player current amount increase must be int, not '{}'."
player_negative_increase_message = "Amount increase must be at least zero (received {})."
player_not_smallest_chip_multiple_increase_message = "Amount increase must be a multiple of the smallest chip: {} (received {})."
player_smallest_chip_not_asigned_message = "Player smallest chip has not being linked to a table yet."

# Table messages
table_not_list_players_message = "Table players must be list, not '{}'."
table_not_all_player_instances_message = 'All table players must be instances of class Player.'
table_not_player_instance_message = "Player must be an instance of class Player, not '{}'."
table_not_int_cards_count_message = "Attribute 'cards_count' must be int, not '{}'."
table_player_not_in_table_message = "Player '{}' is not in the table."
table_player_already_folded_message = "Player '{}' already folded."
table_not_int_smallest_chip_message = "Table smallest chip must be int, not '{}'."
table_not_int_central_pot_message = "Table central pot amount increase must be int, not '{}'."
table_not_int_current_amount_message = "Table current amount increase must be int, not '{}'."
table_negative_increase_message = "Amount increase must be at least zero (received {})."
table_not_smallest_chip_multiple_increase_message = "Amount increase must be a multiple of the smallest chip: {} (received {})."
table_smallest_chip_not_more_than_zero_message = "Smallest chip must be more than zero (received {})."
table_already_asigned_players_message = "Players {} have been asigned to another table. Please, create new Player instances."

# Betting round messages
betting_round_not_str_name_message = "Betting round name must be str, not '{}'."
betting_round_not_table_instance_message = "Betting round table must be an instance of class Table, not '{}'."
betting_round_not_int_smallest_bet_message = "Betting round smallest bet must be int, not '{}'."
betting_round_not_starting_player_instance_message = "Betting round starting player must be an instance of class Player, not '{}'."
betting_round_not_stopping_player_instance_message = "Betting round stopping player must be an instance of class Player, not '{}'."
betting_round_exiting_unended_round_message = 'Betting round did not end.'
betting_round_overloaded_round_message = 'Betting round ended before parsing all actions.'
betting_round_already_ended_round_message = 'Betting round has already ended. It cannot start over.'
betting_round_invalid_action_message = 'The requested action is not allowed: {}.'

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