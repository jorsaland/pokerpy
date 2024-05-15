"""
Defines the class that represents a poker player.
"""


class Player:


    """
    Represents a poker player.
    """


    def __init__(self, name: str):
        self.name = name


    def play(self, betting_round: str):

        """
        Makes the player to take an action.
        """

        print(f'{self.name} plays {betting_round}')