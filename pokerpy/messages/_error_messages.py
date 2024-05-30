"""
Defines messages used in exceptions.
"""


# Player messages
not_str_player_name_message = "Player name must be str, not '{}'."
not_str_action_message = "Player action must be str, not '{}'."

# Table messages
not_list_players_message = "Players must be list, not '{}'."
not_all_player_instances_message = 'All players must be instances of class Player.'
not_player_instance_message = "Player must be an instance of class Player, not '{}'."
player_not_in_table_message = "Player '{}' is not in the table."
player_already_folded_message = "Player '{}' already folded."

# Betting round messages
not_str_betting_round_name_message = "Betting round name must be str, not '{}'."
not_table_instance_message = "Betting round table must be an instance of class Table, not '{}'."
exiting_unended_betting_round_message = 'Betting round did not end.'
overloaded_betting_round_message = 'Betting round ended before parsing all actions.'
starting_already_ended_betting_round_message = 'Betting round has already ended. It cannot start over.'
undefined_action_message = "'{}' is not a betting-round action."