"""
Defines the constants regarding to actions used when playing.
"""


# All possible actions

possible_action_names = [
    ACTION_CHECK := 'check',
    ACTION_FOLD := 'fold',
    ACTION_CALL := 'call',
    ACTION_BET := 'bet',
    ACTION_RAISE := 'raise',
]


# Actions classified by aggressive-passive nature

aggressive_action_names = [
    ACTION_BET,
    ACTION_RAISE
]

passive_action_names = [action for action in possible_action_names if action not in aggressive_action_names]


# Actions classified by whether they are valid or not under bet

valid_action_names_not_under_bet = [
    ACTION_CHECK,
    ACTION_BET,
]

valid_action_names_under_bet = [
    ACTION_FOLD,
    ACTION_CALL,
    ACTION_RAISE,
]