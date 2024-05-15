"""
Defines the class that represents a poker table.
"""


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

        print(f'\n=== Dealer deals cards for {betting_round} ===\n')


    def respond(self, player: Player):

        """
        Makes the dealer to respond to a player.
        """
        
        print(f'Dealer responds to {player.name}\n')