"""
Defines the exceptions that send signals to the managers.
"""


class BaseSignal(Exception):

    """
    Is raised to break a game loop.
    """

    def __init__(self, cause: str):
        self.cause = cause


class JumpToNextPlayerSignal(BaseSignal):

    """
    Signal that tells the betting round to jump to the next player.
    """

    pass


class CloseBettingRoundSignal(BaseSignal):

    """
    Signal that tells the BettingRound to finish.
    """

    pass