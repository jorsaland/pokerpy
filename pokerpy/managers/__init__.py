"""
Namespace for manager-like classes.
"""


from ._betting_round._betting_round import BettingRound
from ._betting_round._action_is_valid import get_valid_action_names, action_is_valid
from ._betting_round._prompt_player import prompt_player
from ._betting_round._await_player import await_player

from ._showdown import showdown, no_showdown