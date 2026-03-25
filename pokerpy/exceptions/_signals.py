"""
Defines the exceptions that send signals to the managers.
"""


class JumpToNextPlayerSignal(Exception):

    """
    Signal that tells the betting round to jump to the next player.
    """

    pass


class CloseBettingRoundSignal(Exception):

    """
    Signal that tells the BettingRound to finish.
    """

    pass