"""
Defines unit tests on await_player function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, messages, structures


class TestBettingRoundAwaitPlayerFunctionParsingAValidAction(TestCase):


    """
    Runs unit tests on await_player function when a valid action is parsed.
    """


    def test_parse_a_valid_action(self):

        """
        Runs test cases where a valid action is parsed.
        """
        
        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = False,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after request
        Andy.request_action(action)
        self.assertEqual(Andy.requested_action, action)

        # Evaluate next states
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertEqual(context.exception.value, action)
        self.assertIsNone(Andy.requested_action)


    def test_skip_actions(self):

        """
        Runs test cases where action parsing is skipped multiple times.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = False,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after skipping
        for _ in range(5):
            self.assertEqual(next(generator), Andy)
            self.assertIsNone(Andy.requested_action)

        # Evaluate final states
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)


    def test_skip_actions_and_parse_a_valid_action(self):

        """
        Runs test cases where action parsing is skipped multiple times and finally a valid action is parsed.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = False,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after skipping
        for _ in range(4):
            self.assertEqual(next(generator), Andy)
            self.assertIsNone(Andy.requested_action)

        # Evaluate states after request
        Andy.request_action(action)
        self.assertEqual(Andy.requested_action, action)

        # Evaluate final states
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertEqual(context.exception.value, action)
        self.assertIsNone(Andy.requested_action)


class TestBettingRoundAwaitPlayerFunctionParsingInvalidActions(TestCase):


    """
    Runs unit tests on await_player function when invalid actions are parsed.
    """


    def test_soft_parse_an_invalid_action(self):

        """
        Runs test cases where an invalid action is parsed, with the generator set to ignore it.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = True,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after request
        Andy.request_action(action)
        self.assertEqual(Andy.requested_action, action)

        # Evaluate next states
        self.assertEqual(next(generator), Andy)
        self.assertEqual(Andy.requested_action, action)


    def test_hard_parse_an_invalid_action(self):

        """
        Runs test cases where an invalid action is parsed, with the generator set to raise an error.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = False,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after request
        Andy.request_action(action)
        self.assertEqual(Andy.requested_action, action)

        # Evaluate next states
        with self.assertRaises(RuntimeError) as context:
            next(generator)
        self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
        self.assertEqual(Andy.requested_action, action)


    def test_skip_actions_and_soft_parse_an_invalid_action(self):

        """
        Runs test cases where action parsing is skipped multiple times and finally an invalid action is parsed, with the generator set to ignore it.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = True,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after skipping
        for _ in range(4):
            self.assertEqual(next(generator), Andy)
            self.assertIsNone(Andy.requested_action)

        # Evaluate states after request
        Andy.request_action(action)
        self.assertEqual(Andy.requested_action, action)

        # Evaluate next states
        self.assertEqual(next(generator), Andy)
        self.assertEqual(Andy.requested_action, action)


    def test_skip_actions_and_hard_parse_an_invalid_action(self):

        """
        Runs test cases where action parsing is skipped multiple times and finally an invalid action is parsed, with the generator set to raise an error.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = False,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after skipping
        for _ in range(4):
            self.assertEqual(next(generator), Andy)
            self.assertIsNone(Andy.requested_action)

        # Evaluate states after request
        Andy.request_action(action)
        self.assertEqual(Andy.requested_action, action)

        # Evaluate next states
        with self.assertRaises(RuntimeError) as context:
            next(generator)
        self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
        self.assertEqual(Andy.requested_action, action)


    def test_skip_actions_and_soft_parse_multiple_invalid_actions(self):

        """
        Runs test cases where action parsing is skipped multiple times and multiple invalid actions are parsed (with the generator set to ignore them).
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        actions = [
            structures.Action(constants.ACTION_CHECK),
            structures.Action(constants.ACTION_CALL, 1),
            structures.Action(constants.ACTION_RAISE, 1),
        ]

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = True,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after skipping
        for _ in range(2):
            self.assertEqual(next(generator), Andy)
            self.assertIsNone(Andy.requested_action)

        # Evaluate states after actions
        for action in actions:
            self.assertEqual(next(generator), Andy)
            Andy.request_action(action)
            self.assertEqual(Andy.requested_action, action)

        # Evaluate final states
        self.assertEqual(next(generator), Andy)
        self.assertEqual(Andy.requested_action, action)


    def test_skip_actions_soft_parse_multiple_invalid_actions_and_parse_a_valid_action(self):

        """
        Runs test cases where action parsing is skipped multiple times, then multiple invalid actions are parsed (with the generator set to ignore them) and finally a valid action is parsed.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        actions = [
            structures.Action(constants.ACTION_CHECK),
            structures.Action(constants.ACTION_CALL, 1),
            structures.Action(constants.ACTION_FOLD),
        ]

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = True,
        )

        # Evaluate states before request
        self.assertEqual(next(generator), Andy)
        self.assertIsNone(Andy.requested_action)

        # Evaluate states after skipping
        for _ in range(2):
            self.assertEqual(next(generator), Andy)
            self.assertIsNone(Andy.requested_action)

        # Evaluate states after actions
        for action in actions:
            self.assertEqual(next(generator), Andy)
            Andy.request_action(action)
            self.assertEqual(Andy.requested_action, action)

        # Evaluate final states
        with self.assertRaises(StopIteration) as context:
            next(generator)
        self.assertEqual(context.exception.value, actions[-1])
        self.assertIsNone(Andy.requested_action)


if __name__ == '__main__':
    main()