"""
Defines the class that represents a poker player.
"""


from deprecated.v03.constants import possible_actions
from deprecated.v03.messages import (
    player_not_card_instance_message,
    player_not_hand_instance_message,
    player_not_str_action_message,
    player_not_str_name_message,
    betting_round_undefined_action_message,
)


from ._card import Card
from ._hand._hand import Hand


class Player:


    """
    Represents a poker player.
    """


    def __init__(self, name: str):

        # Check input
        if not isinstance(name, str):
            raise TypeError(player_not_str_name_message.format(type(name).__name__))

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


    def __repr__(self):
        return f'Player(name={self.name})'


    def request_action(self, action: str):

        """
        Makes the player to request taking an action.
        """

        if not isinstance(action, str):
            raise TypeError(player_not_str_action_message.format(type(action).__name__))

        if action not in possible_actions:
            error_message = betting_round_undefined_action_message.format(action)
            raise ValueError(error_message)

        self._requested_action = action


    def reset_action(self):

        """
        Resets player's request to None.
        """

        self._requested_action = None


    def deliver_card(self, card: Card):

        """
        Delivers a card to the player.
        """

        if not isinstance(card, Card):
            raise TypeError(player_not_card_instance_message.format(type(card).__name__))

        self._cards.append(card)


    def drop_cards(self):

        """
        Empties player cards.
        """

        self._cards.clear()
    

    def assign_hand(self, hand: Hand):

        """
        Assigns a hand to the player.
        """

        if not isinstance(hand, Hand):
            raise TypeError(player_not_hand_instance_message.format(type(hand).__name__))

        self._hand = hand