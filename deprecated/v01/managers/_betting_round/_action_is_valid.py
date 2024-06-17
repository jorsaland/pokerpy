"""
Defines the function that verifies if a betting-round action is valid.
"""


from deprecated.v01.constants import (
    ACTION_FOLD,
    possible_actions,
    valid_actions_not_under_bet,
    valid_actions_under_bet,
)
from deprecated.v01.messages import undefined_action_message


def action_is_valid(action: str, is_under_bet: bool, fold_to_nothing = False):

    """
    Verifies if a betting-round action is valid.
    """

    # Verify action exists
    if action not in possible_actions:
        error_message = undefined_action_message.format(action)
        raise ValueError(error_message)

    # Select valid actions under bet
    if is_under_bet:
        valid_actions = valid_actions_under_bet
    
    # Select valid actions when not under bet
    else:
        if fold_to_nothing:
            valid_actions = valid_actions_not_under_bet + [ACTION_FOLD]
        else:
            valid_actions = valid_actions_not_under_bet

    # Check if action is valid
    return (action in valid_actions)