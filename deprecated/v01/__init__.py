"""
PokerPy under development!
"""


# Info
__version__ = '0.1.3'


# Content
from .constants import (
    ACTION_FOLD,
    aggressive_actions,
    possible_actions,
)
from deprecated.v01.managers import BettingRound, action_is_valid
from deprecated.v01.structures import Player, Table
from deprecated.v01 import switches