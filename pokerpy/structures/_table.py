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
    msg_card_not_in_deck,
    msg_not_all_player_instances,
    msg_not_card_instance,
    msg_not_int,
    msg_not_list,
    msg_not_player_instance,
    msg_not_positive_or_zero_value,
    msg_player_not_in_table,
    msg_repeated_cards,
)


from ._card import Card
from ._player import Player


logger = get_logger()


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(
        self,
        players: list[Player],
    ):

        # Validations

        if not isinstance(players, list):
            raise TypeError(msg_not_list.format(type(players).__name__))
        if not all(isinstance(player, Player) for player in players):
            raise TypeError(msg_not_all_player_instances)

        # Fixed variables

        self._players = players

        # State variables

        self._current_amount = 0
        self._central_pot = 0

        self._deck: list[Card] = [Card(value, suit) for value, suit in full_sorted_values_and_suits]
        self._common_cards: list[Card] = []
    

    @property
    def players(self):
        return tuple(self._players)

    @property
    def players_in_hand(self):
        return tuple(player for player in self.players if not player.is_folded)

    @property
    def current_amount(self):
        return self._current_amount

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

        if not isinstance(card, Card):
            raise TypeError(msg_not_card_instance.format(type(card).__name__))
        
        if card not in self.deck:
            raise ValueError(msg_card_not_in_deck)

        self._deck.remove(card)


    def deal_common_card(self, card: Card):

        """
        Deals a common card to the table.
        """

        if not isinstance(card, Card):
            raise TypeError(msg_not_card_instance.format(type(card).__name__))
        
        if card in self.common_cards:
            raise ValueError(msg_repeated_cards)

        self._common_cards.append(card)


    # Methods related to money


    def add_to_current_amount(self, amount: int):

        """
        Increases the current chip amount that needs to be responded by players.
        """

        if not isinstance(amount, int):
            raise TypeError(msg_not_int.format(type(amount).__name__))
        
        if amount < 0:
            raise ValueError(msg_not_positive_or_zero_value.format(amount))

        self._current_amount += amount


    def add_to_central_pot(self, amount: int):
        
        """
        Increases the pot in the center of the table by an amount.
        """

        if not isinstance(amount, int):
            raise TypeError(msg_not_int.format(type(amount).__name__))

        if amount < 0:
            raise ValueError(msg_not_positive_or_zero_value.format(amount))

        self._central_pot += amount


    # Methods related to players


    def get_next_player(self, reference_player: Player):

        """
        Retrieves the player next.
        """

        if reference_player not in self.players:
            raise ValueError(msg_player_not_in_table.format(reference_player.name))

        if reference_player == self.players[-1]:
            return self.players[0]

        reference_player_index = self.players.index(reference_player)
        return self.players[reference_player_index + 1]


    def get_previous_player(self, reference_player: Player):

        """
        Retrieves the player before.
        """

        if not isinstance(reference_player, Player):
            raise TypeError(msg_not_player_instance.format(type(reference_player).__name__))

        if reference_player not in self.players:
            raise ValueError(msg_player_not_in_table.format(reference_player.name))

        if reference_player == self.players[0]:
            return self.players[-1]

        player_index = self.players.index(reference_player)
        return self.players[player_index - 1]


    def iter_players(self, starting_player: (Player|None) = None, reverse: bool = False):

        """
        Iterates over every player.
        """

        if not self.players:
            def generator():
                yield from ()
            return generator()

        if starting_player is None:
            starting_player = self.players[0]

        if not isinstance(starting_player, Player):
            raise TypeError(msg_not_player_instance.format(type(starting_player).__name__))

        if starting_player not in self.players:
            raise ValueError(msg_player_not_in_table.format(starting_player.name))

        if reverse:
            get_player = self.get_previous_player
        else:
            get_player = self.get_next_player

        def generator():
            yield starting_player
            next_player = get_player(starting_player)
            while next_player != starting_player:
                yield next_player
                next_player = get_player(next_player)
        
        return generator()


    def get_previous_active_player(self, reference_player: Player):

        """
        Retrieves the first player before who is still in the hand cycle, or None if everybody is marked as folded.
        """

        if not isinstance(reference_player, Player):
            raise TypeError(msg_not_player_instance.format(type(reference_player).__name__))

        if reference_player not in self.players:
            raise ValueError(msg_player_not_in_table.format(reference_player.name))

        for player in self.iter_players(self.get_previous_player(reference_player), reverse=True):
            if not player.is_folded and player.stack > 0:
                return player


    # Methods to reset manager states


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self._current_amount = 0


    def reset_cycle_states(self):

        """
        Resets all state variables that are restricted to cycles.
        """

        self.reset_betting_round_states()

        self._deck.clear()
        self._deck.extend(Card(value, suit) for value, suit in full_sorted_values_and_suits)

        self._common_cards.clear()

        self._central_pot = 0
