"""
Defines unit tests on BettingRound class run method.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, messages, structures


class TestBettingRoundRunListenerFunctionWithInvalidParsing(TestCase):


    """
    Runs unit tests on BettingRound class run method when requests are not parsed correctly.
    """


    def test_skip_requests_and_parse_a_valid_action(self):

        """
        Runs test cases where a player skips requests and has to play again until a valid action is chosen.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.run_listener(betting_round)

        # Before states
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Skip requests
        for _ in range(3):
            self.assertEqual(betting_round.lap_counts, 1)
            self.assertEqual(next(generator), Andy)

        # Request a valid action
        Andy.request_action(action)
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)


    def test_skip_requests_and_hard_parse_an_invalid_action(self):

        """
        Runs test cases where a player skips requests and has to play again until an invalid action is chosen, with the generator set to raise an error.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False)

        action = structures.Action(constants.ACTION_RAISE, 1)

        generator = managers.run_listener(betting_round)

        # Before states
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Skip requests
        for _ in range(3):
            self.assertEqual(betting_round.lap_counts, 1)
            self.assertEqual(next(generator), Andy)

        # Request an invalid action
        Andy.request_action(action)
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(RuntimeError) as context:
            next(generator)
        self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)


    def test_skip_requests_soft_parse_invalid_actions_and_parse_a_valid_action(self):

        """
        Runs test cases where a player skips requests and chooses invalid actions, and has to play again until a valid action is chosen, with the generator set to ignore invalid actions.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table)

        valid_action = structures.Action(constants.ACTION_CHECK)
        invalid_actions = [
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_RAISE, 1),
            structures.Action(constants.ACTION_CALL, 1),
        ]

        generator = managers.run_listener(betting_round)

        # Before states
        self.assertEqual(betting_round.lap_counts, 0)

        # Skip requests
        for _ in range(3):
            self.assertEqual(next(generator), Andy)
            self.assertEqual(betting_round.lap_counts, 1)

        # Request invalid actions
        for action in invalid_actions:
            Andy.request_action(action)
            self.assertEqual(next(generator), Andy)
            self.assertEqual(betting_round.lap_counts, 1)

        # Request a valid action
        Andy.request_action(valid_action)
        self.assertEqual(next(generator), Boa)
        self.assertEqual(betting_round.lap_counts, 1)


class TestBettingRoundRunListenerFunctionStartingWithFold(TestCase):


    """
    Runs unit tests on BettingRound class run method when the first requested action is fold.
    """


    def test_folds(self):

        """
        Runs test cases where every player folds (except the last one).
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False, open_fold_allowed=True)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 1)


    def test_folds_to_checks(self):

        """
        Runs test cases where players fold and check.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False, open_fold_allowed=True)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        Dino.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 1)


    def test_folds_to_bet_to_folds(self):

        """
        Runs test cases every player folds, except for one that bets.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False, open_fold_allowed=True)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        Dino.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 1)
        self.assertEqual(betting_round.lap_counts, 1)


class TestBettingRoundRunListenerFunctionStartingWithCheck(TestCase):


    """
    Runs unit tests on BettingRound class run method when the first requested action is check.
    """


    def test_checks(self):

        """
        Runs test cases where every player checks.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        Dino.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 1)


    def test_checks_to_folds(self):

        """
        Runs test cases where players check and fold.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False, open_fold_allowed=True)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        Dino.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 1)


    def test_checks_to_bet_to_folds(self):

        """
        Runs test cases where some players check, another one bets and everyone folds (except for the player who bet).
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        Dino.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Andy)

        Andy.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 2)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 2)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 2)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 1)
        self.assertEqual(betting_round.lap_counts, 2)


class TestBettingRoundRunListenerFunctionStartingWithBet(TestCase):


    """
    Runs unit tests on BettingRound class run method when the first requested action is bet.
    """


    def test_bet_to_folds(self):

        """
        Runs test cases where a player bets and the others fold.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        Dino.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 1)
        self.assertEqual(betting_round.lap_counts, 1)


    def test_bet_to_calls(self):

        """
        Runs test cases where a player bets and the others call.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Actions

        Andy.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        Boa.request_action(structures.Action(constants.ACTION_CALL, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        Coral.request_action(structures.Action(constants.ACTION_CALL, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        Dino.request_action(structures.Action(constants.ACTION_CALL, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 4)
        self.assertEqual(betting_round.lap_counts, 1)


class TestBettingRoundRunListenerFunctionWithMultipleLaps(TestCase):


    """
    Runs unit tests on BettingRound class run method with multiple laps.
    """


    def test_multiple_laps(self):

        """
        Runs test cases in a betting round with multiple laps.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),     
        ])

        betting_round = managers.BettingRound('test round', table, ignore_invalid_actions=False, open_fold_allowed=True)

        generator = managers.run_listener(betting_round)

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(generator), Andy)

        # Lap 1

        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Andy.stack, 10)
        Andy.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Boa.stack, 10)
        Boa.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Coral)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Coral.stack, 10)
        Coral.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Dino)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)
        self.assertEqual(Dino.stack, 10)
        Dino.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(betting_round.lap_counts, 1)
        self.assertEqual(next(generator), Boa)

        # Lap 2

        self.assertEqual(betting_round.table.stopping_player, Coral)
        self.assertEqual(table.current_amount, 1)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Boa.stack, 10)
        Boa.request_action(structures.Action(constants.ACTION_CALL, 1))
        self.assertEqual(betting_round.lap_counts, 2)
        self.assertEqual(next(generator), Coral)

        self.assertEqual(betting_round.table.stopping_player, Coral)
        self.assertEqual(table.current_amount, 1)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Coral.stack, 10)
        Coral.request_action(structures.Action(constants.ACTION_RAISE, 2))
        self.assertEqual(betting_round.lap_counts, 2)
        self.assertEqual(next(generator), Dino)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        self.assertEqual(table.current_amount, 2)
        self.assertEqual(Dino.current_amount, 1)
        self.assertEqual(Dino.stack, 9)
        Dino.request_action(structures.Action(constants.ACTION_CALL, 1))
        self.assertEqual(betting_round.lap_counts, 2)
        self.assertEqual(next(generator), Boa)

        # Lap 3

        self.assertEqual(betting_round.table.stopping_player, Boa)
        self.assertEqual(table.current_amount, 2)
        self.assertEqual(Boa.current_amount, 1)
        self.assertEqual(Boa.stack, 9)
        Boa.request_action(structures.Action(constants.ACTION_RAISE, 3))
        self.assertEqual(betting_round.lap_counts, 3)
        self.assertEqual(next(generator), Coral)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(table.current_amount, 4)
        self.assertEqual(Coral.current_amount, 2)
        self.assertEqual(Coral.stack, 8)
        Coral.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(betting_round.lap_counts, 3)
        self.assertEqual(next(generator), Dino)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(table.current_amount, 4)
        self.assertEqual(Dino.current_amount, 2)
        self.assertEqual(Dino.stack, 8)
        Dino.request_action(structures.Action(constants.ACTION_RAISE, 6))
        self.assertEqual(betting_round.lap_counts, 3)
        self.assertEqual(next(generator), Boa)

        # Lap 4

        self.assertEqual(betting_round.table.stopping_player, Boa)
        self.assertEqual(table.current_amount, 8)
        self.assertEqual(Boa.current_amount, 4)
        self.assertEqual(Boa.stack, 6)
        Boa.request_action(structures.Action(constants.ACTION_RAISE, 6))
        self.assertEqual(betting_round.lap_counts, 4)
        self.assertEqual(next(generator), Dino)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(table.current_amount, 10)
        self.assertEqual(Dino.current_amount, 8)
        self.assertEqual(Dino.stack, 2)
        Dino.request_action(structures.Action(constants.ACTION_CALL, 2))
        self.assertEqual(betting_round.lap_counts, 4)
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 22)
        self.assertEqual(betting_round.lap_counts, 4)



if __name__ == '__main__':
    main()