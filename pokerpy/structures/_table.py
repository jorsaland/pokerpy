"""
Defines the class that represents a poker table.
"""


import random
from typing import Iterable


from pokerpy.constants import full_sorted_values_and_suits


from ._card import Card
from ._player import Player


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(self, players: Iterable[Player]):

        # Input variables
        self.players = list(players)

        # State variables
        self.active_players: set[Player] = set()
        self.is_under_bet = False
        self.last_aggressive_player: (Player|None) = None
        self.deck: set[Card] = set()
        self.common_cards: set[Card] = set()


    def reset_cycle_states(self):

        """
        Resets all state variables that are restricted to cycles.
        """

        # Reset players
        self.active_players.clear()
        self.active_players.update(self.players)

        # Reset cards
        self.deck.update({Card(value, suit) for value, suit in full_sorted_values_and_suits})
        self.common_cards.clear()
        for player in self.players:
            player.cards.clear()


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self.is_under_bet = False
        self.last_aggressive_player = None


    def deal(self, betting_round: str):

        """
        Makes the dealer to deal the cards.
        """

        print(f'Dealer deals cards for {betting_round}.\n')


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