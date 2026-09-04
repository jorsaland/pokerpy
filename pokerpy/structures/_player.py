# Copyright 2026 Andrés Saldarriaga Jordan (jorsaland)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Defines the class that represents a poker player.
"""


from pokerpy.validations import (
    validate_int_amount_smaller_than_bet_level,
    validate_int_amount_smaller_than_stack,
    validate_int_positive,
    validate_int_positive_or_zero,
    validate_iterable_not_contains_card,
    validate_type_action,
    validate_type_card,
    validate_type_hand,
    validate_type_int,
    validate_type_str,
)


from ._action import Action
from ._card import Card
from ._hand._hand import Hand


class Player:


    """
    Represents a poker player.
    """


    def __init__(self, name: str, stack: int):

        # Validations

        validate_type_str(name)
        validate_type_int(stack)

        validate_int_positive(stack)

        # Fixed variables
        self._name = name

        # State variables
        self._cards: list[Card] = []
        self._hand: (Hand|None) = None
        self._requested_action: (Action|None) = None
        self._stack = stack
        self._bet_level = 0
        self._pot_index = 0
        self._is_folded = False
        self._has_played = False


    @property
    def name(self):
        "Player's identifier, unique within the table."
        return self._name

    @property
    def cards(self):
        "Cards dealt to the player."
        return tuple(self._cards)

    @property
    def hand(self):
        "Hand the player holds, according to the game rules."
        return self._hand

    @property
    def requested_action(self):
        "Action the player has requested in a betting round."
        return self._requested_action

    @property
    def stack(self):
        "Amount of chips the player has placed in front during the current betting round."
        return self._stack

    @property
    def bet_level(self):
        "Amount of chips that the player has placed in front during the betting round."
        return self._bet_level

    @property
    def is_folded(self):
        "Whether the player has already folded in the current hand cycle."
        return self._is_folded

    @property
    def has_played(self):
        """
        Whether the player has already taken a voluntary action during the current betting round
        (not including forced bets)
        """
        return self._has_played

    @property
    def pot_index(self):
        "Index of the pot the player is playing for, being 0 the main pot."
        return self._pot_index


    def __repr__(self):
        return f'Player(name={self.name}, stack={self.stack})'


    # Methods to affect actions


    def request_action(self, action: Action):
        "Sets the requested_action property."
        validate_type_action(action)
        self._requested_action = action


    def clear_action(self):
        "Resets the requested_action property back to None."
        self._requested_action = None


    # Methods to affect cards and hand


    def assign_card(self, card: Card):
        "Adds a card to the cards property."
        validate_type_card(card)
        validate_iterable_not_contains_card(card, self.cards)
        self._cards.append(card)


    def reset_cards(self):
        "Clears the cards property."
        self._cards.clear()


    def assign_hand(self, hand: Hand):
        "Sets the hand property."
        validate_type_hand(hand)
        self._hand = hand


    def clear_hand(self):
        "Resets the hand property back to None."
        self._hand = None


    # Methods to affect stack and current amount


    def increase_bet_level(self, amount: int):
        "Adds an amount to the bet_level property."
        validate_type_int(amount)
        validate_int_positive_or_zero(amount)
        self._bet_level += amount

    def decrease_bet_level(self, amount: int):
        "Removes an amount to the bet_level property."
        validate_type_int(amount)
        validate_int_positive_or_zero(amount)
        validate_int_amount_smaller_than_bet_level(amount, self.bet_level)
        self._bet_level -= amount

    def increase_stack(self, amount: int):
        "Adds an amount to the stack property."
        validate_type_int(amount)
        validate_int_positive_or_zero(amount)
        self._stack += amount

    def decrease_stack(self, amount: int):
        "Removes an amount from the stack property."
        validate_type_int(amount)
        validate_int_positive_or_zero(amount)
        validate_int_amount_smaller_than_stack(amount, self.stack)
        self._stack -= amount

    def increase_pot_index(self):
        "Increases in 1 the pot_index property."
        self._pot_index += 1

    def reset_pot_index(self):
        "Resets the pot_index back to zero."
        self._pot_index = 0


    # Methods to affect playing status


    def mark_has_played(self):
        "Marks the has_played property."
        self._has_played = True


    def unmark_has_played(self):
        "Unmarks the has_played property."
        self._has_played = False


    def mark_is_folded(self):
        "Marks the is_folded property."
        self._is_folded = True


    def unmark_is_folded(self):
        "Unmarks the is_folded property."
        self._is_folded = False