"""
Defines the class that represents a poker player.
"""


from pokerpy.messages import (
    player_negative_increase_message,
    player_not_action_instance_message,
    player_not_card_instance_message,
    player_not_int_current_amount_message,
    player_not_hand_instance_message,
    player_not_str_name_message,
    player_smallest_chip_not_asigned_message,
    player_not_smallest_chip_multiple_increase_message,
)


from ._action import Action
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
        self._requested_action: (Action|None) = None
        self._cards: list[Card] = []
        self._hand: (Hand|None) = None
        self._current_amount = 0 # this is set by instance methods
        self._already_asigned = False # this is set by the table when instanced
        self._smallest_chip = 0 # this is set by the table when instanced


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

    @property
    def current_amount(self):
        assert self._current_amount % self._smallest_chip == 0 ## should never fail, except for direct manipulation
        return self._current_amount
    
    @property
    def already_asigned(self):
        return self._already_asigned
    
    @property
    def smallest_chip(self):
        if self._smallest_chip == 0:
            raise ValueError(player_smallest_chip_not_asigned_message)
        return self._smallest_chip


    def __repr__(self):
        return f'Player(name={self.name})'


    # Methods to set/unset requested action


    def request_action(self, action: Action):

        """
        Makes the player to request taking an action.
        """

        if not isinstance(action, Action):
            raise TypeError(player_not_action_instance_message.format(type(action).__name__))

        self._requested_action = action


    def reset_action(self):

        """
        Resets player's request to None.
        """

        self._requested_action = None


    # Methods to assign cards and hand


    def deliver_card(self, card: Card):

        """
        Delivers a card to the player.
        """

        if not isinstance(card, Card):
            raise TypeError(player_not_card_instance_message.format(type(card).__name__))

        self._cards.append(card)


    def assign_hand(self, hand: Hand):

        """
        Assigns a hand to the player.
        """

        if not isinstance(hand, Hand):
            raise TypeError(player_not_hand_instance_message.format(type(hand).__name__))

        self._hand = hand


    # Methods to affect current amount bet by player


    def add_to_current_amount(self, amount: int):

        """
        Increases the current chip amount bet by a player during a betting round.
        """

        if not isinstance(amount, int):
            raise TypeError(player_not_int_current_amount_message.format(type(amount).__name__))

        if amount < 0:
            raise ValueError(player_negative_increase_message.format(amount))

        if not amount % self.smallest_chip == 0:
            raise ValueError(player_not_smallest_chip_multiple_increase_message.format(self.smallest_chip, amount))

        self._current_amount += amount


    # Methods to reset managers


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self._requested_action: (Action|None) = None
        self._current_amount = 0
    

    def reset_cycle_states(self):

        """
        Resets all state variables that are restricted to cycles.
        """

        # Reset betting_round_states
        self.reset_betting_round_states()

        # Drop cards and reset hand
        self._cards.clear()
        self._hand: (Hand|None) = None