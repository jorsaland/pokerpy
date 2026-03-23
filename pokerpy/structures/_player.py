"""
Defines the class that represents a poker player.
"""


from pokerpy.messages import (
    msg_amount_larger_than_stack,
    msg_not_action_instance,
    msg_not_card_instance,
    msg_not_hand_instance,
    msg_not_int,
    msg_not_positive_or_zero_value,
    msg_not_positive_value,
    msg_not_str,
    msg_repeated_cards,
)


from ._action import Action
from ._card import Card
from ._hand._hand import Hand


class Player:


    """
    Represents a poker player.
    """


    def __init__(self, name: str, *, stack: int):

        # Validations

        if not isinstance(name, str):
            raise TypeError(msg_not_str.format(type(name).__name__))

        if not isinstance(stack, int):
            raise TypeError(msg_not_int.format(type(stack).__name__))

        if stack <= 0:
            raise ValueError(msg_not_positive_value.format(stack))

        # Fixed variables
        self._name = name

        # State variables
        self._requested_action: (Action|None) = None
        self._cards: list[Card] = []
        self._hand: (Hand|None) = None
        self._current_amount = 0 # this is set by instance methods
        self._stack = stack


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
        return self._current_amount
    
    @property
    def stack(self):
        return self._stack


    def __repr__(self):
        return f'Player(name={self.name})'


    # Methods to affect actions


    def request_action(self, action: Action):

        """
        Makes the player to request taking an action.
        """

        if not isinstance(action, Action):
            raise TypeError(msg_not_action_instance.format(type(action).__name__))

        self._requested_action = action


    def reset_action(self):

        """
        Resets player's request to None.
        """

        self._requested_action = None


    # Methods to affect cards and hand


    def deal_card(self, card: Card):

        """
        Deals a card to the player.
        """

        if not isinstance(card, Card):
            raise TypeError(msg_not_card_instance.format(type(card).__name__))

        if card in self.cards:
            raise ValueError(msg_repeated_cards)

        self._cards.append(card)


    def assign_hand(self, hand: Hand):

        """
        Assigns a hand to the player.
        """

        if not isinstance(hand, Hand):
            raise TypeError(msg_not_hand_instance.format(type(hand).__name__))

        self._hand = hand


    # Methods to affect stack and current amount


    def add_to_current_amount(self, amount: int):

        """
        Increases the current chip amount bet by a player during a betting round.
        """

        if not isinstance(amount, int):
            raise TypeError(msg_not_int.format(type(amount).__name__))

        if amount < 0:
            raise ValueError(msg_not_positive_or_zero_value.format(amount))

        self._current_amount += amount


    def add_to_stack(self, amount: int):

        """
        Adds chips to the stack.
        """

        if not isinstance(amount, int):
            raise TypeError(msg_not_int.format(type(amount).__name__))

        if amount < 0:
            raise ValueError(msg_not_positive_or_zero_value.format(amount))

        self._stack += amount


    def remove_from_stack(self, amount: int):

        """
        Removes chips from the stack.
        """

        if not isinstance(amount, int):
            raise TypeError(msg_not_int.format(type(amount).__name__))

        if amount < 0:
            raise ValueError(msg_not_positive_or_zero_value.format(amount))
        
        if amount > self.stack:
            raise ValueError(msg_amount_larger_than_stack.format(amount, self.stack))

        self._stack -= amount


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