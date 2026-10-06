"""
Defines unit tests on BettingRound class run method.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, messages, structures


class BaseTestCase(TestCase):


    "Base class for test cases that require a shared setup."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]

        self.table = structures.Table(self.setup_players, min_bet=100)

        self.Andy = self.setup_players[0]
        self.Boa = self.setup_players[1]
        self.Coral = self.setup_players[2]
        self.Dino = self.setup_players[3]
        self.Epa = self.setup_players[4]
        self.Fomi = self.setup_players[5]

        self.betting_round = engines.BettingRound(
            'test',
            self.table,
            raise_invalid_actions = True,
            open_fold_allowed = True
        )


class BaseForcedBetsTestCase(TestCase):


    "Base class for test cases that require a shared setup with forced bets."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]

        self.table = structures.Table(self.setup_players, min_bet=100)

        self.Andy = self.setup_players[0]
        self.Boa = self.setup_players[1]
        self.Coral = self.setup_players[2]
        self.Dino = self.setup_players[3]
        self.Epa = self.setup_players[4]
        self.Fomi = self.setup_players[5]

        self.betting_round = engines.BettingRound(
            'test',
            self.table,
            raise_invalid_actions = True,
            open_fold_allowed = True,
            starting_player = self.Coral,
        )

        self.Andy.decrease_stack(50)
        self.Andy.increase_bet_level(50)

        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.Coral.decrease_stack(100)
        self.Coral.increase_bet_level(100)

        self.Epa.decrease_stack(100)
        self.Epa.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)


class TestBettingRoundRunListenerFunctionStartingWithFold(BaseTestCase):


    "Runs unit tests on run_listener function when the first requested action is fold."


    def test_folds(self):

        "Tests all players folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_fold_to_checks(self):

        "Tests first two players folding and others checking."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (1, self.Dino, structures.Action(constants.ACTION_CHECK)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Fomi, structures.Action(constants.ACTION_CHECK)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_fold_to_bet_to_folds(self):

        "Tests first two players folding, next betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_fold_to_bet_to_calls(self):

        "Tests first two players folding, next betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_check_to_folds(self):

        "Tests first player folding, next checking and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_checks(self):

        "Tests first player folding and others checking."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (1, self.Dino, structures.Action(constants.ACTION_CHECK)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Fomi, structures.Action(constants.ACTION_CHECK)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_check_to_bet_to_folds(self):

        "Tests first player folding, next checking, next betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Boa, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_check_to_bet_to_calls(self):

        "Tests first player folding, next checking, next betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_bet_to_folds(self):

        "Tests first player folding, next betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_bet_to_calls(self):

        "Tests first players fold, next betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_bet_to_raise_to_folds(self):

        "Tests first player folding, next betting, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Boa, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_fold_to_bet_to_raise_to_calls(self):

        "Tests first player folding, next betting, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


class TestBettingRoundRunListenerFunctionStartingWithCheck(BaseTestCase):


    "Runs unit tests on run_listener function when the first requested action is check."


    def test_check_to_folds(self):

        "Tests first player checking and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_fold_to_checks(self):

        "Tests first player checking, next folding and others checking."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (1, self.Dino, structures.Action(constants.ACTION_CHECK)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Fomi, structures.Action(constants.ACTION_CHECK)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_fold_to_bet_to_folds(self):

        "Tests first player checking, next folding, next betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_fold_to_bet_to_calls(self):

        "Tests first player checking, next folding, next betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_check_to_folds(self):

        "Tests first two players checking and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_checks(self):

        "Tests all players checking."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (1, self.Dino, structures.Action(constants.ACTION_CHECK)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Fomi, structures.Action(constants.ACTION_CHECK)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_check_to_bet_to_folds(self):

        "Tests first two players checking, next betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (2, self.Boa, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_check_to_bet_to_calls(self):

        "Tests first two players checking, next betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_bet_to_folds(self):

        "Tests first player checking, next betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_bet_to_calls(self):

        "Tests first player checking, next betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_bet_to_raise_to_folds(self):

        "Tests first player checking, next betting, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (2, self.Boa, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_check_to_bet_to_raise_to_calls(self):

        "Tests first player checking, next betting, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


class TestBettingRoundRunListenerFunctionStartingWithBet(BaseTestCase):


    "Runs unit tests on run_listener function when the first requested action is bet."


    def test_bet_to_folds(self):

        "Tests first player betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_fold_to_calls(self):

        "Tests first player betting, next folding and others checking."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_fold_to_raise_to_folds(self):

        "Tests first player betting, next folding, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_fold_to_raise_to_calls(self):

        "Tests first player betting, next folding, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_call_to_folds(self):

        "Tests first player betting, next calling and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_calls(self):

        "Tests first player betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_call_to_raise_to_folds(self):

        "Tests first player betting, next calling, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (2, self.Boa, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_call_to_raise_to_calls(self):

        "Tests first player betting, next calling, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_raise_to_folds(self):

        "Tests first player betting, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_raise_to_calls(self):

        "Tests first player betting, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_raise_to_raise_to_folds(self):

        "Tests first player betting, next two raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 300)),
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)),
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (2, self.Andy, structures.Action(constants.ACTION_FOLD)),
            (2, self.Boa, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_bet_to_raise_to_raise_to_calls(self):

        "Tests first player betting, next two raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_BET, 100)),
            (1, self.Boa, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 300)),
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 300)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 300)),
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


class TestBettingRoundRunListenerFunctionWithForcedBetsStartingWithFold(BaseForcedBetsTestCase):


    "Runs unit tests on run_listener function when there are forced bets and the first requested action is fold."


    def test_with_blinds_folds(self):

        "Tests all players folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_fold_to_checks_or_calls(self):

        "Tests first two players folding and others checking or calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 50)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_fold_to_bet_to_folds(self):

        "Tests first two players folding, next betting and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_fold_to_bet_to_calls(self):

        "Tests first two players folding, next betting and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_check_or_call_to_folds(self):

        "Tests first player folding, next checking or calling and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_checks_or_calls(self):

        "Tests first player folding and others checking or calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 50)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_check_or_call_to_bet_or_raise_to_folds(self):

        "Tests first player folding, next checking or calling, next betting or raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Dino, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_check_or_call_to_bet_or_raise_to_calls(self):

        "Tests first player folding, next checking or calling, next betting or raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_bet_or_raise_to_folds(self):

        "Tests first player folding, next betting or raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_bet_or_raise_to_calls(self):

        "Tests first player folding, next betting or raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_bet_or_raise_to_raise_to_folds(self):

        "Tests first player folding, next betting or raising, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Dino, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_fold_to_bet_or_raise_to_raise_to_calls(self):

        "Tests first player folding, next betting or raising, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 250)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 200)), # BB
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


class TestBettingRoundRunListenerFunctionWithForcedBetsStartingWithCheckOrCall(BaseForcedBetsTestCase):


    "Runs unit tests on run_listener function when there are forced bets and the first requested action is fold."


    def test_with_blinds_check_or_call_to_folds(self):

        "Tests first player checking or calling and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_or_call_to_fold_to_checks_or_calls(self):

        "Tests player checking or calling, next folding and others checking or calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 50)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_or_call_to_fold_to_bet_or_raise_to_folds(self):

        "Tests first player checking or calling, next folding, next betting or raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_or_call_to_fold_to_bet_or_raise_to_calls(self):

        "Tests first player checking or calling, next folding, next betting or raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_or_call_to_check_or_call_to_folds(self):

        "Tests first two players checking or calling and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_checks_or_calls(self):

        "Tests all players checking or calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 50)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_or_call_to_check_or_call_to_bet_or_raise_to_folds(self):

        "Tests first two players checking or calling, next betting or raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (2, self.Dino, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_or_call_to_check_or_call_to_bet_or_raise_to_calls(self):

        "Tests first two players checking or calling, next betting or raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (1, self.Epa, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_to_bet_or_raise_to_folds(self):

        "Tests first player checking, next betting or raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_to_bet_or_raise_to_calls(self):

        "Tests first player checking, next betting or raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_to_bet_or_raise_to_raise_to_folds(self):

        "Tests first player checking, next betting or raising, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (2, self.Dino, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_check_to_bet_or_raise_to_raise_to_calls(self):

        "Tests first player checking, next betting or raising, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 250)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 200)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


class TestBettingRoundRunListenerFunctionWithForcedBetsStartingWithBet(BaseForcedBetsTestCase):


    "Runs unit tests on run_listener function when there are forced bets and the first requested action is bet."


    def test_with_blinds_bet_or_raise_to_folds(self):

        "Tests first player betting or raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_fold_to_calls(self):

        "Tests player betting or raising, next folding and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_fold_to_raise_to_folds(self):

        "Tests first player betting or raising, next folding, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_fold_to_raise_to_calls(self):

        "Tests first player betting or raising, next folding, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_FOLD)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 250)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 200)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_call_to_folds(self):

        "Tests first player betting or raising, next calling and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_calls(self):

        "Tests first player betting or raising and next calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 100)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 150)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 100)), # BB
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_call_to_raise_to_folds(self):

        "Tests first player betting or raising, next calling, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (2, self.Dino, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_call_to_raise_to_calls(self):

        "Tests first player betting or raising, next calling, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_CALL, 200)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 250)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 200)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_raise_to_folds(self):

        "Tests first player betting or raising, next raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 300)),
            (1, self.Epa, structures.Action(constants.ACTION_FOLD)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_raise_to_calls(self):

        "Tests first player betting or raising, next raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 300)),
            (1, self.Epa, structures.Action(constants.ACTION_CALL, 200)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 250)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 200)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_raise_to_raise_to_folds(self):

        "Tests first player betting or raising, next two raising and others folding."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 300)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 300)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_FOLD)),
            (1, self.Andy, structures.Action(constants.ACTION_FOLD)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_FOLD)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (2, self.Dino, structures.Action(constants.ACTION_FOLD)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_with_blinds_bet_or_raise_to_raise_to_raise_to_calls(self):

        "Tests first player betting or raising, next two raising and others calling."

        laps_and_players_and_actions = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino, structures.Action(constants.ACTION_RAISE, 300)),
            (1, self.Epa, structures.Action(constants.ACTION_RAISE, 300)), # BB
            (1, self.Fomi, structures.Action(constants.ACTION_CALL, 400)),
            (1, self.Andy, structures.Action(constants.ACTION_CALL, 350)), # SB
            (1, self.Boa, structures.Action(constants.ACTION_CALL, 300)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


class TestBettingRoundRunListenerFunctionAllInChain(BaseTestCase):


    "Runs unit tests on run_listener function chaining actions to make all players go all-in."


    def test_starting_with_full_stacks(self):

        "Tests players starting with full stacks."

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (1, self.Dino, structures.Action(constants.ACTION_CHECK)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Fomi, structures.Action(constants.ACTION_BET, 100)), # +100
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Epa, structures.Action(constants.ACTION_RAISE, 300)), # +200
            (2, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
            (3, self.Andy, structures.Action(constants.ACTION_CALL, 200)),
            (3, self.Boa, structures.Action(constants.ACTION_CALL, 200)),
            (3, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
            (3, self.Dino, structures.Action(constants.ACTION_RAISE, 500)), # +300
            (3, self.Epa, structures.Action(constants.ACTION_CALL, 300)),
            (3, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
            (4, self.Andy, structures.Action(constants.ACTION_CALL, 300)),
            (4, self.Boa, structures.Action(constants.ACTION_CALL, 300)),
            (4, self.Coral, structures.Action(constants.ACTION_RAISE, 700)), # +400
            (4, self.Dino, structures.Action(constants.ACTION_CALL, 400)),
            (4, self.Epa, structures.Action(constants.ACTION_CALL, 400)),
            (4, self.Fomi, structures.Action(constants.ACTION_CALL, 400)),
            (5, self.Andy, structures.Action(constants.ACTION_CALL, 400)),
            (5, self.Boa, structures.Action(constants.ACTION_CALL, 400)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


    def test_starting_with_under_stacks(self):

        "Tests players starting with stacks smaller than full stacks."

        for player in self.setup_players:
            player.decrease_stack(player.stack)

        self.Andy.increase_stack(200)
        self.Boa.increase_stack(200)
        self.Coral.increase_stack(500)
        self.Dino.increase_stack(500)
        self.Epa.increase_stack(1000)
        self.Fomi.increase_stack(1000)

        laps_and_players_and_actions = (
            (1, self.Andy, structures.Action(constants.ACTION_CHECK)),
            (1, self.Boa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (1, self.Dino, structures.Action(constants.ACTION_CHECK)),
            (1, self.Epa, structures.Action(constants.ACTION_CHECK)),
            (1, self.Fomi, structures.Action(constants.ACTION_BET, 100)), # +100
            (2, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (2, self.Epa, structures.Action(constants.ACTION_RAISE, 300)), # +200
            (2, self.Fomi, structures.Action(constants.ACTION_RAISE, 500)), # +300
            (3, self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (3, self.Boa, structures.Action(constants.ACTION_CALL, 100)),
            (3, self.Coral, structures.Action(constants.ACTION_CALL, 400)),
            (3, self.Dino, structures.Action(constants.ACTION_CALL, 400)),
            (3, self.Epa, structures.Action(constants.ACTION_RAISE, 700)), # +400
            (3, self.Fomi, structures.Action(constants.ACTION_CALL, 400)),
        )

        generator = engines.run_listener(self.betting_round)

        with self.subTest('before actions'):
            self.assertEqual(self.betting_round.lap_counts, 0)

        for lap, player, action in laps_and_players_and_actions:
            player.request_action(action)
            with self.subTest(player=player, action=action):
                self.assertEqual(next(generator), player)
                self.assertEqual(self.betting_round.lap_counts, lap)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, lap)


if __name__ == '__main__':
    main()