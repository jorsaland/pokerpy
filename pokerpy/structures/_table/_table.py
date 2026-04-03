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


from ._get_split_pot import get_split_pot
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
        "Players that are part of the table."
        return tuple(self._players)

    @property
    def starting_player(self):
        "Player who acts first in the betting round."
        return self._starting_player

    @property
    def stopping_player(self):
        "Player who acts last in the betting round."
        return self._stopping_player

    @property
    def players_in_hand(self):
        "Players that are playing for the pot."
        return tuple(player for player in self.players if not player.is_folded)
    
    @property
    def active_players(self):
        "Players that are playing for the pot and are not all-in"
        return tuple(player for player in self.players if not player.is_folded and player.stack > 0)

    @property
    def full_bet(self):
        "Minimum amount to bet (unless going all-in)."
        return self._full_bet

    @property
    def full_raise_increase(self):
        "Minimum amount to raise (unless going all-in)."
        return self._full_raise_increase

    @property
    def current_level(self):
        "Largest amount a player has placed in front during the current betting round."
        return self._current_level

    @property
    def complete_current_level(self):
        """
        Largest amount a player has placed in front during the current betting round that can be
        considered as a full bet or raise.
        """
        return self._complete_current_level

    @property
    def central_pot(self):
        """
        Pot chips that have already been placed in the center of the table in previous betting
        rounds.
        """
        return self._central_pot

    @property
    def split_pot(self):
        """
        Pot chips that have already been placed in the center of the table in previous betting
        rounds.
        """
        return get_split_pot(self.central_pot, [player.pot_participation for player in self.players_in_hand])



    @property
    def deck(self):
        "Cards that are available to be dealt."
        return tuple(self._deck)
    
    @property
    def common_cards(self):
        "Dealt cards that are common to all players."
        return tuple(self._common_cards)


    # Methods related to cards


    def remove_card_from_deck(self, card: Card):
        "Removes a card from the deck property."
        return method_remove_card_from_deck(self, card)


    def reset_deck(self):
        "Resets the deck property back to have all the cards."
        return method_reset_deck(self)


    def assign_common_card(self, card: Card):
        "Adds a card to the common_cards property."
        return method_assign_common_card(self, card)


    def reset_common_cards(self):
        "Clears the common_cards property."
        return method_reset_common_cards(self)


    # Methods related to money


    def set_full_bet(self, amount: int):
        "Sets the full_bet property."
        return method_set_full_bet(self, amount)


    def set_full_raise_increase(self, amount: int):
        "Sets the full_raise_increase property."
        return method_set_full_raise_increase(self, amount)


    def set_current_level(self, amount: int):
        "Sets the current_level property."
        return method_set_current_level(self, amount)


    def set_complete_current_level(self, amount: int):
        "Sets the complete_current_level property."
        return method_set_complete_current_level(self, amount)


    def add_to_central_pot(self, amount: int):
        "Adds an amount to the central_pot property."
        return method_add_to_central_pot(self, amount)


    def reset_central_pot(self):
        "Resets the central_pot property back to zero."
        return method_reset_central_pot(self)


    # Methods related to players


    def set_starting_player(self, player: Player):
        "Sets the starting_player property."
        return method_set_starting_player(self, player)
    

    def set_stopping_player(self, player: Player):
        "Sets the stopping_player property."
        return method_set_stopping_player(self, player)


    def get_next_player(self, reference_player: Player):
        "Retrieves the player next to a reference player."
        return method_get_next_player(self, reference_player)


    def get_previous_player(self, reference_player: Player):
        "Retrieves the player before a reference player."
        return method_get_previous_player(self, reference_player)


    def iter_players(self, starting_player: (Player|None) = None, reverse: bool = False):
        "Iterates over all the players."
        return method_iter_players(self, starting_player, reverse)


    def get_previous_active_player(self, reference_player: Player):
        "Retrieves the player before a reference player that is not either folded or all-in."
        return method_get_previous_active_player(self, reference_player)
