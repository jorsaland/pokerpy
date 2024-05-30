"""
Defines the class that represents a poker table.
"""


import secrets


from pokerpy.constants import full_sorted_values_and_suits
from pokerpy.messages import (
    not_int_cards_count_message,
    not_list_players_message,
    not_all_player_instances_message,
    not_player_instance_message,
    player_not_in_table_message,
    player_already_folded_message,
)


from ._card import Card
from ._player import Player


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(self, players: list[Player]):

        # Check input
        if not isinstance(players, list):
            raise TypeError(not_list_players_message.format(type(players).__name__))
        if not all(isinstance(player, Player) for player in players):
            raise TypeError(not_all_player_instances_message)

        # Input variables
        self._players = players

        # State variables
        self._active_players: list[Player] = []
        self._is_under_bet = False
        self._last_aggressive_player: (Player|None) = None
        self._deck: list[Card] = [Card(value, suit) for value, suit in full_sorted_values_and_suits]
        self._common_cards: list[Card] = []
    

    @property
    def players(self):
        return tuple(self._players)
    
    @property
    def active_players(self):
        return tuple(self._active_players)

    @property
    def is_under_bet(self):
        return self._is_under_bet

    @property
    def last_aggressive_player(self):
        return self._last_aggressive_player

    @property
    def deck(self):
        return tuple(self._deck)
    
    @property
    def common_cards(self):
        return tuple(self._common_cards)


    def reset_cycle_states(self):

        """
        Resets all state variables that are restricted to cycles.
        """

        # Reset players
        self._active_players.clear()
        self._active_players.extend(self._players)

        # Reset deck
        self._deck.clear()
        self._deck.extend(Card(value, suit) for value, suit in full_sorted_values_and_suits)

        # Reset common and player cards
        self._common_cards.clear()
        for player in self.players:
            player.drop_cards()


    def activate_player(self, player: Player):
        
        """
        Make a single player to become available to play.
        """

        if not isinstance(player, Player):
            raise TypeError(not_player_instance_message.format(type(player).__name__))
        
        if player not in self.players:
            raise ValueError(player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            self._active_players.append(player)


    def become_under_bet(self):

        """
        Makes the betting round to become under bet.
        """

        self._is_under_bet = True
    

    def fold_player(self, player: Player):

        """
        Removes a player from a hand cycle.
        """

        if not isinstance(player, Player):
            raise TypeError(not_player_instance_message.format(type(player).__name__))
        
        if player not in self.players:
            raise ValueError(player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            raise ValueError(player_already_folded_message.format(player.name))

        self._active_players.remove(player)


    def set_last_aggressive_player(self, player: Player):

        """
        Marks a player as the last one to take an aggressive action.
        """

        if not isinstance(player, Player):
            raise TypeError(not_player_instance_message.format(type(player).__name__))

        if player not in self.players:
            raise ValueError(player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            raise ValueError(player_already_folded_message.format(player.name))

        self._last_aggressive_player = player


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self._is_under_bet = False
        self._last_aggressive_player = None


    def deal_to_players(self, cards_count: int):

        """
        Deals cards to players in equal amounts.
        """

        if not isinstance(cards_count, int):
            raise TypeError(not_int_cards_count_message.format(type(cards_count).__name__))

        for _ in range(cards_count):
            for player in self.active_players:
                print(f'Dealer deals card to {player.name}.')
                card = secrets.choice(self.deck)
                self._deck.remove(card)
                player.deliver_card(card)


    def deal_common_cards(self, cards_count: int):

        """
        Deals common cards to table.
        """

        if not isinstance(cards_count, int):
            raise TypeError(not_int_cards_count_message.format(type(cards_count).__name__))

        print(f'Dealer deals common cards.')
        for _ in range(cards_count):
            card = secrets.choice(self.deck)
            self._deck.remove(card)
            self._common_cards.append(card)


    def showdown(self):

        """
        Makes the dealer to determine who is the winner among remaining players.
        """

        print(f'Remaining players: {", ".join(p.name for p in self.active_players)}')

        winners: list[Player] = []
        for player in self.active_players:

            player_is_unbeaten = True
            for oponent in self.active_players:
                if oponent.name == player.name:
                    continue
                if oponent.hand > player.hand:
                    player_is_unbeaten = False
                    break

            if player_is_unbeaten:
                winners.append(player)

        if len(winners) == 1:
            print(f'{winners[0].name} wins!')

        else:
            print(f'It is a tie! Winners: {", ".join([w.name for w in winners])}.')
