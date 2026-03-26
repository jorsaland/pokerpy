"""
Defines unit tests on alternate_players function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, exceptions, managers, messages, structures


class TestBettingRoundPromptPlayerFunction(TestCase):


    """
    Runs unit tests on prompt_player function.
    """


    def test_last_remaining_player(self):

        """
        Runs test cases where the prompted player cannot parse an action because is the last one remaining in the hand cycle.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])
        table.add_to_current_amount(1)
        Boa.fold()
        Coral.fold()
        Dino.fold()

        betting_round = managers.BettingRound('test round', table, stopping_player=Coral)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_last_player_in_hand)


    def test_non_closing_folded_player(self):

        """
        Runs test cases where the prompted player cannot parse an action because has already folded, given there are more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])
        table.add_to_current_amount(1)
        Andy.fold()

        betting_round = managers.BettingRound('test round', table, stopping_player=Coral)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        with self.assertRaises(exceptions.JumpToNextPlayerSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_folded_player)


    def test_closing_folded_player(self):

        """
        Runs test cases where the prompted player cannot parse an action because has already folded, given there are no more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])
        table.add_to_current_amount(1)
        Andy.fold()

        betting_round = managers.BettingRound('test round', table, stopping_player=Andy)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_folded_stopping_player)


    def test_non_closing_all_in_player(self):

        """
        Runs test cases where the prompted player cannot parse an action because is already all-in, given there are more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])
        Andy.remove_from_stack(10)
        Andy.add_to_current_amount(10)
        table.add_to_current_amount(10)

        betting_round = managers.BettingRound('test round', table, stopping_player=Coral)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        with self.assertRaises(exceptions.JumpToNextPlayerSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_all_in_player)


    def test_closing_all_in_player(self):

        """
        Runs test cases where the prompted player cannot parse an action because is already all-in, given there are no more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])
        Andy.remove_from_stack(10)
        Andy.add_to_current_amount(10)
        table.add_to_current_amount(10)

        betting_round = managers.BettingRound('test round', table, stopping_player=Andy)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_all_in_stopping_player)


    def test_non_closing_passive_player(self):

        """
        Runs test cases where the prompted player parses a passive action, given there are more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])

        action = structures.Action(constants.ACTION_CHECK)

        betting_round = managers.BettingRound('test round', table, stopping_player=Coral)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        self.assertEqual(next(generator), Andy)

        # After parsing an action
        Andy.request_action(action)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)


    def test_closing_passive_player(self):

        """
        Runs test cases where the prompted player parses a passive action, given there are more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])

        action = structures.Action(constants.ACTION_CHECK)

        betting_round = managers.BettingRound('test round', table, stopping_player=Andy)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        self.assertEqual(next(generator), Andy)

        # After parsing an action
        Andy.request_action(action)
        with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_passive_stopping_player)


    def test_non_closing_agressive_player(self):

        """
        Runs test cases where the prompted player parses an aggressive action, given there are more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])

        action = structures.Action(constants.ACTION_BET, 1)

        betting_round = managers.BettingRound('test round', table, stopping_player=Coral)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        self.assertEqual(next(generator), Andy)

        # After parsing an action
        Andy.request_action(action)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)


    def test_closing_agressive_player(self):

        """
        Runs test cases where the prompted player parses an aggressive action, given there are no more players to listen.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),       
        ])

        action = structures.Action(constants.ACTION_BET, 1)

        betting_round = managers.BettingRound('test round', table, stopping_player=Andy)

        generator = managers.prompt_player(betting_round, Andy)

        # Before parsing an action
        self.assertEqual(next(generator), Andy)

        # After parsing an action
        Andy.request_action(action)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)


if __name__ == '__main__':
    main()