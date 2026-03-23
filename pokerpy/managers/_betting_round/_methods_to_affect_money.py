"""
Defines the methods that affect money attributes.
"""


from typing import TYPE_CHECKING


from pokerpy.messages import msg_not_int, msg_not_positive_value


if TYPE_CHECKING:
    from ._betting_round import BettingRound


def method_overwrite_smallest_rising_amount(self: "BettingRound", amount: int):

    """
    Overwrites the smallest amount expected to make a raise.
    """

    if not isinstance(amount, int):
        raise TypeError(msg_not_int.format(type(amount).__name__))
    
    if amount <= 0:
        raise ValueError(msg_not_positive_value.format(amount))

    self._smallest_rising_amount = amount