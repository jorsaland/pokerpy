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