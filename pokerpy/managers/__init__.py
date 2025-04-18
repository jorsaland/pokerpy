"""
Namespace for manager-like classes.
"""


from ._betting_round._betting_round import BettingRound
from ._betting_round._action_is_valid import get_valid_action_names, action_is_valid
from ._betting_round._alternate_players import alternate_players
from ._betting_round._wait_for_player import wait_for_player