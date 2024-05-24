"""
Defines the class that represents a poker player.
"""


from pokerpy.constants import possible_actions
from pokerpy.messages import undefined_action_message


from ._card import Card
from ._hand import Hand


class Player:


    """
    Represents a poker player.
    """


    def __init__(self, name: str):

        # Input variables
        self.name = name

        # State variables
        self.requested_action: (str|None) = None
        self.cards: list[Card] = []
        self.hand: (Hand|None) = None


    def request(self, action: str):

        """
        Makes the player to request taking an action.
        """

        if action not in possible_actions:
            error_message = undefined_action_message.format(action=action)
            raise ValueError(error_message)

        self.requested_action = action