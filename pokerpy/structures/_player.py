"""
Defines the class that represents a poker player.
"""


from pokerpy.constants import possible_actions
from pokerpy.messages import (
    not_str_action_message,
    not_str_player_name_message,
    undefined_action_message,
)


class Player:


    """
    Represents a poker player.
    """


    def __init__(self, name: str):

        # Check input
        if not isinstance(name, str):
            raise TypeError(not_str_player_name_message.format(type(name).__name__))

        # Input variables
        self._name = name

        # State variables
        self._requested_action: (str|None) = None


    @property
    def name(self):
        return self._name

    @property
    def requested_action(self):
        return self._requested_action


    def __repr__(self):
        return f'Player(name={self.name})'


    def request(self, action: str):

        """
        Makes the player to request taking an action.
        """

        if not isinstance(action, str):
            raise TypeError(not_str_action_message.format(type(action).__name__))

        if action not in possible_actions:
            error_message = undefined_action_message.format(action)
            raise ValueError(error_message)

        self._requested_action = action
    

    def reset(self):

        """
        Resets player's request to None.
        """

        self._requested_action = None