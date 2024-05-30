"""
Defines messages used in exceptions.
"""


# Player messages
not_str_player_name_message = "Player name must be str, not '{}'."
not_str_action_message = "Player action must be str, not '{}'."
not_card_instance_message = "Player card must be an instance of class Card, not '{}'."
not_hand_instance_message = "Player hand must be an instance of class Hand, not '{}'."

# Table messages
not_list_players_message = "Players must be list, not '{}'."
not_all_player_instances_message = 'All players must be instances of class Player.'
not_player_instance_message = "Player must be an instance of class Player, not '{}'."
not_int_cards_count_message = "Attribute 'cards_count' must be int, not '{}'."
player_not_in_table_message = "Player '{}' is not in the table."
player_already_folded_message = "Player '{}' already folded."

# Betting round messages
not_str_betting_round_name_message = "Betting round name must be str, not '{}'."
not_table_instance_message = "Betting round table must be an instance of class Table, not '{}'."
exiting_unended_betting_round_message = 'Betting round did not end.'
overloaded_betting_round_message = 'Betting round ended before parsing all actions.'
starting_already_ended_betting_round_message = 'Betting round has already ended. It cannot start over.'
undefined_action_message = "'{}' is not a betting-round action."

# Card messages
not_str_card_value_message = "Card value must be str, not '{}'."
not_str_card_suit_message = "Card suit must be str, not '{}'."
invalid_card_suit_message = 'Card suits must be one of these: {}'
invalid_card_value_message = 'Card values must be one of these: {}'
joker_card_message = 'We live in a society.'

# Hand messages
not_iterable_object_cards_message = "Hand cards must be an iterable object, not '{}'."
not_all_card_instances_message = 'All cards must be instances of class Card.'
not_five_cards_hand_message = 'Hands must have exactly five cards.'
repeated_cards_hand_message = 'Cards in a hand cannot be repeated.'
