"""
Defines the function that verifies if a betting-round action is valid according to previous actions.
"""


from pokerpy.constants import (
    ACTION_FOLD,
    ACTION_CALL,
    ACTION_BET,
    ACTION_RAISE,
    valid_action_names_not_under_bet,
    valid_action_names_under_bet,
)
from pokerpy.structures import Action, Player, Table


def get_valid_action_names(*, amount_to_call: int, open_fold_allowed: bool):

    """
    Lists the valid possible actions depending on previous actions taken during the betting round.
    """

    if amount_to_call != 0:
        valid_action_names = valid_action_names_under_bet

    else:
        if open_fold_allowed:
            valid_action_names = valid_action_names_not_under_bet + [ACTION_FOLD]
        else:
            valid_action_names = valid_action_names_not_under_bet

    return valid_action_names


def action_is_valid(*, action: Action, table: Table, player: Player):

    """
    Verifies if a betting-round action is valid according to previous actions.
    """

    # Calculate amount that player has to call
    amount_to_call = table.current_amount - player.current_amount

    # Validate action per se
    valid_action_names = get_valid_action_names(
        amount_to_call = amount_to_call,
        open_fold_allowed = table.open_fold_allowed,
    )
    if action.name not in valid_action_names:
        return False

    # Validate amount being multiple of smallest chip
    if not action.amount % table.smallest_chip == 0:
        return False

    # Validate calling amount
    if action.name == ACTION_CALL:
        return action.amount == amount_to_call
    
    # Validate betting amount
    if action.name == ACTION_BET:
        return action.amount >= table.smallest_bet
    
    # Validate raising amount
    if action.name == ACTION_RAISE:
        validation_conditions = [
            action.amount > amount_to_call,
            action.amount - amount_to_call >= table.smallest_rising_amount,
        ]
        return all(validation_conditions)

    return True