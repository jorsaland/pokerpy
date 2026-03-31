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
Defines the class that represents a poker table.
"""


from pokerpy.constants import full_sorted_values_and_suits
from pokerpy.logger import get_logger
from pokerpy.messages import (
    msg_no_players_in_table,
    msg_not_all_player_instances,
    msg_not_int,
    msg_not_list,
    msg_not_player_instance,
    msg_not_positive_value,
    msg_player_not_in_table,
)


from ._methods_related_to_cards import (
    method_assign_common_card,
    method_reset_common_cards,
    method_remove_card_from_deck,
    method_reset_deck,
)
from ._methods_related_to_money import (
    method_add_to_central_pot,
    method_reset_central_pot,
    method_set_current_level,
    method_set_complete_current_level,
    method_set_full_bet,
    method_set_full_raise_increase,
)
from ._methods_related_to_players import (
    method_get_next_player,
    method_get_previous_active_player,
    method_get_previous_player,
    method_iter_players,
    method_set_starting_player,
    method_set_stopping_player,
)
from .._card import Card
from .._player import Player


logger = get_logger()


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(
        self,
        players: list[Player],
        *,
        full_bet: int = 1,
        starting_player: (Player|None) = None,
        stopping_player: (Player|None) = None,
    ):

        # Type validations

        if not isinstance(players, list):
            raise TypeError(msg_not_list.format(type(players).__name__))
        if not all(isinstance(player, Player) for player in players):
            raise TypeError(msg_not_all_player_instances)
        
        if not isinstance(full_bet, int):
            raise TypeError(msg_not_int.format(type(full_bet).__name__))
        
        if starting_player is not None and not isinstance(starting_player, Player):
            raise TypeError(msg_not_player_instance.format(type(starting_player).__name__))

        if stopping_player is not None and not isinstance(stopping_player, Player):
            raise TypeError(msg_not_player_instance.format(type(stopping_player).__name__))

        # Value validations

        if not players:
            raise ValueError(msg_no_players_in_table)

        if full_bet <= 0:
            raise ValueError(msg_not_positive_value.format(full_bet))

        if starting_player is None:
            starting_player = players[0]
        if starting_player not in players:
            raise ValueError(msg_player_not_in_table.format(starting_player.name))

        if stopping_player is None:
            player_index = players.index(starting_player)
            stopping_player = players[player_index - 1]
        if stopping_player not in players:
            raise ValueError(msg_player_not_in_table.format(stopping_player.name))

        # Assign attributes

        self._players = players
        self._full_bet = full_bet
        self._full_raise_increase = full_bet
        self._starting_player = starting_player
        self._stopping_player = stopping_player

        self._current_level = 0
        self._complete_current_level = 0
        self._central_pot = 0

        self._deck: list[Card] = [Card(value, suit) for value, suit in full_sorted_values_and_suits]
        self._common_cards: list[Card] = []
    

    @property
    def players(self):
        return tuple(self._players)

    @property
    def starting_player(self):
        return self._starting_player

    @property
    def stopping_player(self):
        return self._stopping_player

    @property
    def players_in_hand(self):
        return tuple(player for player in self.players if not player.is_folded)

    @property
    def full_bet(self):
        return self._full_bet

    @property
    def full_raise_increase(self):
        return self._full_raise_increase

    @property
    def current_level(self):
        return self._current_level

    @property
    def complete_current_level(self):
        return self._complete_current_level

    @property
    def central_pot(self):
        return self._central_pot

    @property
    def deck(self):
        return tuple(self._deck)
    
    @property
    def common_cards(self):
        return tuple(self._common_cards)


    # Methods related to cards


    def remove_card_from_deck(self, card: Card):

        """
        Removes a card from the deck.
        """

        return method_remove_card_from_deck(self, card)


    def reset_deck(self):

        """
        Resets the deck by restoring all its cards.
        """

        return method_reset_deck(self)


    def assign_common_card(self, card: Card):

        """
        Deals a common card to the table.
        """

        return method_assign_common_card(self, card)


    def reset_common_cards(self):

        """
        Clears the space for common cards.
        """

        return method_reset_common_cards(self)


    # Methods related to money


    def set_full_bet(self, amount: int):

        """
        Sets the amount needed for a full bet.
        """

        return method_set_full_bet(self, amount)


    def set_full_raise_increase(self, amount: int):

        """
        Sets the amount needed to increase the current complete level for a full raise.
        """

        return method_set_full_raise_increase(self, amount)


    def set_current_level(self, amount: int):

        """
        Sets the current level.
        """

        return method_set_current_level(self, amount)


    def set_complete_current_level(self, amount: int):

        """
        Sets the current full raise or full bet.
        """

        return method_set_complete_current_level(self, amount)


    def add_to_central_pot(self, amount: int):
        
        """
        Increases the pot in the center of the table by an amount.
        """

        return method_add_to_central_pot(self, amount)


    def reset_central_pot(self):

        """
        Resets the central pot to zero.
        """

        return method_reset_central_pot(self)


    # Methods related to players


    def set_starting_player(self, player: Player):

        """
        Marks the player who acts first in the betting round.
        """

        return method_set_starting_player(self, player)
    

    def set_stopping_player(self, player: Player):

        """
        Marks the player who acts last before closing the betting round is closed.
        """

        return method_set_stopping_player(self, player)


    def get_next_player(self, reference_player: Player):

        """
        Retrieves the player next.
        """

        return method_get_next_player(self, reference_player)


    def get_previous_player(self, reference_player: Player):

        """
        Retrieves the player before.
        """

        return method_get_previous_player(self, reference_player)


    def iter_players(self, starting_player: (Player|None) = None, reverse: bool = False):

        """
        Iterates over every player.
        """

        return method_iter_players(self, starting_player, reverse)


    def get_previous_active_player(self, reference_player: Player):

        """
        Retrieves the first player before who is still in the hand cycle, or None if everybody is marked as folded.
        """

        return method_get_previous_active_player(self, reference_player)
