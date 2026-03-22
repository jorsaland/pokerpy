"""
Defines the class that represents an action taken by a player within a betting round.
"""


from pokerpy.constants import (
    ACTION_CHECK,
    ACTION_FOLD,
    possible_action_names,
)
from pokerpy.messages import (
    action_msg_not_positive_amount,
    action_msg_not_zero_amount,
    action_msg_not_int_amount,
    action_msg_not_str_name,
    action_msg_invalid_name,
)


class Action:


    """
    Represents an action taken by a player within a betting round.
    """


    def __init__(self, name: str, amount: int = 0):

        # Check types
        if not isinstance(name, str):
            raise TypeError(action_msg_not_str_name.format(type(name).__name__))
        if not isinstance(amount, int):
            raise TypeError(action_msg_not_int_amount.format(type(amount).__name__))

        # Validate input
        if name not in possible_action_names:
            error_message = action_msg_invalid_name.format(name, ', '.join(possible_action_names))
            raise ValueError(error_message)
        
        # Validate amount
        if name in (ACTION_FOLD, ACTION_CHECK):
            if amount != 0:
                raise ValueError(action_msg_not_zero_amount.format(name, amount))
        else:
            if not amount > 0:
                raise ValueError(action_msg_not_positive_amount.format(name, amount))

        # Fixed variables
        self._name = name
        self._amount = amount


    @property
    def name(self):
        return self._name
    
    @property
    def amount(self):
        return self._amount


    def __repr__(self):
        return f'Action(name={self.name}, amount={self.amount})'
    

    def __eq__(self, other):

        if not isinstance(other, Action):
            return NotImplemented

        return (self.name == other.name) and (self.amount == other.amount)