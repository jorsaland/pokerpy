"""
Defines the function that lists the valid possible actions depending on previous actions taken during the betting round.
"""


from pokerpy.constants import (
    ACTION_FOLD,
    ACTION_CALL,
    ACTION_CHECK,
    ACTION_BET,
    ACTION_RAISE,
)


def get_valid_action_names(*, amount_to_call: int, stack: int, open_fold_allowed: bool):

    """
    Lists the valid possible actions depending on previous actions taken during the betting round.
    """

    if amount_to_call != 0:
        if amount_to_call >= stack:
            valid_action_names = [ACTION_FOLD, ACTION_CALL]
        else:
            valid_action_names = [ACTION_FOLD, ACTION_CALL, ACTION_RAISE]

    else:
        if open_fold_allowed:
            valid_action_names = [ACTION_CHECK, ACTION_BET, ACTION_FOLD]
        else:
            valid_action_names = [ACTION_CHECK, ACTION_BET]

    return valid_action_names