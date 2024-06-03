"""
Defines the function that verifies if a betting-round action is valid according to previous actions.
"""


from pokerpy.constants import ACTION_FOLD, valid_action_names_not_under_bet, valid_action_names_under_bet
from pokerpy.structures import Action
from pokerpy import switches


def action_is_valid(*, action: Action, is_under_bet: bool, stack_atom: int):

    """
    Verifies if a betting-round action is valid according to previous actions.
    """

    # Select valid actions under bet

    if is_under_bet:
        valid_action_names = valid_action_names_under_bet
    
    # Select valid actions when not under bet
    else:
        if switches.ONLY_ALLOW_FOLDING_UNDER_BET:
            valid_action_names = valid_action_names_not_under_bet
        else:
            valid_action_names = valid_action_names_not_under_bet + [ACTION_FOLD]

    # Validate name
    if action.name not in valid_action_names:
        return False
    
    # Validate amount
    if not action.amount % stack_atom == 0:
        return False

    return True