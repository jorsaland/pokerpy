"""
Defines the function that verifies if a betting-round action is valid according to previous actions.
"""


from pokerpy.constants import ACTION_FOLD, valid_action_names_not_under_bet, valid_action_names_under_bet
from pokerpy.structures import Action
from pokerpy import switches


def action_is_valid(action: Action, is_under_bet: bool):

    """
    Verifies if a betting-round action is valid according to previous actions.
    """

    # Select valid actions under bet
    if is_under_bet:
        valid_actions = valid_action_names_under_bet
    
    # Select valid actions when not under bet
    else:
        if switches.ONLY_ALLOW_FOLDING_UNDER_BET:
            valid_actions = valid_action_names_not_under_bet
        else:
            valid_actions = valid_action_names_not_under_bet + [ACTION_FOLD]

    # Check if action is valid
    return (action.name in valid_actions)