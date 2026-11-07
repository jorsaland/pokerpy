"""
Defines unit tests on await_player function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, messages, structures


class TestBettingRoundAwaitPlayerFunction(TestCase):


    "Runs unit tests on await_player function."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]

        self.table = structures.Table(self.setup_players)
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi = self.setup_players


    def test_parse_a_valid_action(self):

        "Tests parsing a valid action"

        action = structures.Action(constants.ACTION_CHECK)

        generator = engines.await_player(
            player = self.Andy,
            bet_level = self.table.bet_level,
            full_bet_level = self.table.full_bet_level,
            min_bet = 2,
            min_raise_increase = 2,
            is_last_actionable_player = False,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.subTest('before request'):
            self.assertEqual(next(generator), self.Andy)
            self.assertIsNone(self.Andy.requested_action)

        self.Andy.request_action(action)
        with self.subTest('after valid request'):
            self.assertEqual(self.Andy.requested_action, action)

        with self.subTest('generator termination', action=action):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertEqual(context.exception.value, action)
            self.assertIsNone(self.Andy.requested_action)


    def test_hard_skip_action(self):

        "Tests skipping action parsing, with the generator set to raise an error."

        generator = engines.await_player(
            player = self.Andy,
            bet_level = self.table.bet_level,
            full_bet_level = self.table.full_bet_level,
            min_bet = 2,
            min_raise_increase = 2,
            is_last_actionable_player = False,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.subTest('before skipping'):
            self.assertEqual(next(generator), self.Andy)
            self.assertIsNone(self.Andy.requested_action)

        with self.subTest('generator termination'):
            with self.assertRaises(RuntimeError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_missing_action)
            self.assertIsNone(self.Andy.requested_action)


    def test_soft_skip_actions_and_parse_a_valid_action(self):

        "Tests skipping action parsing multiple times and finally parsing a valid action."

        action = structures.Action(constants.ACTION_CHECK)

        generator = engines.await_player(
            player = self.Andy,
            bet_level = self.table.bet_level,
            full_bet_level = self.table.full_bet_level,
            min_bet = 2,
            min_raise_increase = 2,
            is_last_actionable_player = False,
            open_fold_allowed = False,
            raise_invalid_actions = False,
        )

        with self.subTest('before request'):
            self.assertEqual(next(generator), self.Andy)
            self.assertIsNone(self.Andy.requested_action)

        for i in range(5):
            with self.subTest('after skipping', i=i):
                self.assertEqual(next(generator), self.Andy)
                self.assertIsNone(self.Andy.requested_action)

        self.Andy.request_action(action)
        with self.subTest('after valid request'):
            self.assertEqual(self.Andy.requested_action, action)

        with self.subTest('generator termination'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertEqual(context.exception.value, action)
            self.assertIsNone(self.Andy.requested_action)


    def test_hard_parse_an_invalid_action(self):

        "Tests parsing an invalid action, with the generator set to raise an error."

        self.table.set_bet_level(2)
        self.table.set_full_bet_level(2)

        action = structures.Action(constants.ACTION_CHECK)

        generator = engines.await_player(
            player = self.Andy,
            bet_level = self.table.bet_level,
            full_bet_level = self.table.full_bet_level,
            min_bet = 2,
            min_raise_increase = 2,
            is_last_actionable_player = False,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.subTest('before request'):
            self.assertEqual(next(generator), self.Andy)
            self.assertIsNone(self.Andy.requested_action)

        self.Andy.request_action(action)
        with self.subTest('after invalid request'):
            self.assertEqual(self.Andy.requested_action, action)

        with self.subTest('generator termination'):
            with self.assertRaises(RuntimeError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            self.assertEqual(self.Andy.requested_action, action)


    def test_soft_parse_invalid_actions_and_parse_a_valid_action(self):

        "Tests parsing an invalid action multiple times and finally parsing a valid action."

        self.table.set_bet_level(2)
        self.table.set_full_bet_level(2)

        invalid_action = structures.Action(constants.ACTION_CHECK)
        valid_action = structures.Action(constants.ACTION_CALL, 2)

        generator = engines.await_player(
            player = self.Andy,
            bet_level = self.table.bet_level,
            full_bet_level = self.table.full_bet_level,
            min_bet = 2,
            min_raise_increase = 2,
            is_last_actionable_player = False,
            open_fold_allowed = False,
            raise_invalid_actions = False,
        )

        with self.subTest('before request'):
            self.assertEqual(next(generator), self.Andy)
            self.assertIsNone(self.Andy.requested_action)

        self.Andy.request_action(invalid_action)
        for i in range(5):
            with self.subTest('after invalid request', i=i):
                self.assertEqual(next(generator), self.Andy)
                self.assertEqual(self.Andy.requested_action, invalid_action)

        self.Andy.request_action(valid_action)
        with self.subTest('after valid request'):
            self.assertEqual(self.Andy.requested_action, valid_action)

        with self.subTest('generator termination'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertEqual(context.exception.value, valid_action)
            self.assertIsNone(self.Andy.requested_action)


    def test_soft_skip_actions_and_parse_invalid_actions_and_parse_a_valid_action(self):

        "Tests skipping action parsing and parsing multiple invalid actions, with the generator set to ignore them, and finally parsing a valid action."

        self.table.set_bet_level(2)
        self.table.set_full_bet_level(2)

        invalid_action = structures.Action(constants.ACTION_CHECK)
        valid_action = structures.Action(constants.ACTION_CALL, 2)

        generator = engines.await_player(
            player = self.Andy,
            bet_level = self.table.bet_level,
            full_bet_level = self.table.full_bet_level,
            min_bet = 2,
            min_raise_increase = 2,
            is_last_actionable_player = False,
            open_fold_allowed = False,
            raise_invalid_actions = False,
        )

        with self.subTest('before request'):
            self.assertEqual(next(generator), self.Andy)
            self.assertIsNone(self.Andy.requested_action)

        for i in range(5):
            with self.subTest('after skipping', i=i):
                self.assertEqual(next(generator), self.Andy)
                self.assertIsNone(self.Andy.requested_action)

        self.Andy.request_action(invalid_action)
        for i in range(5):
            with self.subTest('after invalid request', i=i):
                self.assertEqual(next(generator), self.Andy)
                self.assertEqual(self.Andy.requested_action, invalid_action)

        self.Andy.request_action(valid_action)
        with self.subTest('after valid request'):
            self.assertEqual(self.Andy.requested_action, valid_action)

        with self.subTest('generator termination'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertEqual(context.exception.value, valid_action)
            self.assertIsNone(self.Andy.requested_action)


if __name__ == '__main__':
    main()