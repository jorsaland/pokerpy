"""
Defines the class that represents a poker table.
"""


import random


from ._player import Player


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(self, players: list[Player]):
        self.players = players


    def deal(self, betting_round: str):

        """
        Makes the dealer to deal the cards.
        """

        print(f'Dealer deals cards for {betting_round}.\n')


    def showdown(self):

        """
        Makes the dealer to determine who is the winner among remaining players.
        """

        winner = random.choice(self.players)
        print(f'{winner.name} wins!')