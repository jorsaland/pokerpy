"""
Defines unit tests on alternate_players function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, exceptions, managers, structures


class TestBettingRoundPromptPlayerFunction(TestCase):


    """
    Runs unit tests on prompt_player function.
    """


    def test_one_player_remaining(self):

        """
        Runs test cases where a single player is still in the hand cycle.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            Epa := structures.Player('Epa', 10),            
        ])
        table.add_to_current_amount(1)
        Andy.fold()
        Coral.fold()
        Dino.fold()
        Epa.fold()

        action = structures.Action(constants.ACTION_FOLD)

        betting_round = managers.BettingRound('test round', table, stopping_player=Dino)

        generator = managers.prompt_player(betting_round, Boa)

        # Evaluate states before prompt

        # Evaluate states after prompt        

        with self.assertRaises(exceptions.CloseBettingRoundSignal):
            next(generator)


if __name__ == '__main__':
    main()