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
        self._name = name

        # State variables
        self._requested_action: (str|None) = None
        self._cards: list[Card] = []
        self._hand: (Hand|None) = None


    @property
    def name(self):
        return self._name

    @property
    def requested_action(self):
        return self._requested_action

    @property
    def cards(self):
        return tuple(self._cards)

    @property
    def hand(self):
        return self._hand


    def request(self, action: str):

        """
        Makes the player to request taking an action.
        """

        if action not in possible_actions:
            error_message = undefined_action_message.format(action=action)
            raise ValueError(error_message)

        self._requested_action = action


    def drop_cards(self):

        """
        Empties player cards.
        """

        self._cards.clear()