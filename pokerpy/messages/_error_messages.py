"""
Defines messages used in exceptions.
"""


exiting_unended_betting_round_message = 'Betting round did not end.'
invalid_card_suit_message = 'Card suits must be one of these: {valid_suits}'
invalid_card_value_message = 'Card values must be one of these: {valid_values}'
joker_card_message = 'We live in a society.'
not_five_cards_hand_message = 'Hands must have exactly five cards.'
overloaded_betting_round_message = 'Betting round ended before parsing all actions.'
repeated_cards_hand_message = 'Cards in a hand cannot be repeated.'
starting_already_ended_betting_round_message = 'Betting round has already ended. It cannot start over.'
undefined_action_message = "'{action}' is not a betting-round action."