"""
Defines the function that verifies if a betting-round action is valid according to previous actions.
"""


from pokerpy.constants import (
    ACTION_FOLD,
    ACTION_CALL,
    ACTION_RAISE,
    valid_action_names_not_under_bet,
    valid_action_names_under_bet,
)
from pokerpy.structures import Action, Player, Table
from pokerpy import switches


def action_is_valid(*, action: Action, table: Table, player: Player):

    """
    Verifies if a betting-round action is valid according to previous actions.
    """

    # Calculate amount that player has to call
    amount_to_call = table.current_amount - player.current_amount

    # Select valid actions under bet
    if amount_to_call != 0:
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

    # Validate stack atom
    if not action.amount % table.stack_atom == 0:
        return False
        
    # Validate calling amount
    if action.name == ACTION_CALL:
        return action.amount == amount_to_call
    
    # Validate raising amount
    if action.name == ACTION_RAISE:
        return action.amount > amount_to_call

    return True