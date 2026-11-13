"""
Defines unit tests on BettingRound class run method action chains.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, states, structures


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
        self.Andy, self.Boa,   self.Coral, self.Dino,  self.Epa, self.Fomi = self.setup_players

        self.betting_round = engines.BettingRound('test', self.table, open_fold_allowed=True)


    def run_initial_tests(self):

        "Runs the unit tests for the initial state."

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                self.assertEqual(player.pot_index, 0)


    def run_yield_and_closure_tests(
            self,
            laps_and_players_and_actions_and_ranges: tuple[
                tuple[int, structures.Player, structures.Action, dict[str, range]],
                ...
            ],
        ):

        "Runs the unit tests for the yield and closure states."

        generator = engines.run_betting_round_listener(self.betting_round)
        current_lap = 0

        for lap, player, action, action_ranges in laps_and_players_and_actions_and_ranges:

            with self.subTest('yield state', player=player, action=action):
                await_state = next(generator)
                self.assertIsInstance(await_state, states.PlayerActionAwait)
                self.assertDictEqual(await_state.ranges, action_ranges)
                self.assertEqual(await_state.player, player)
                self.assertEqual(self.betting_round.lap_counts, lap)
                self.assertEqual(self.table.current_player, player)

            await_state.request_action(action)
            current_lap = lap

        with self.subTest('closure state'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertEqual(self.betting_round.lap_counts, current_lap)


class BaseForcedBetsTestCase(BaseTestCase):


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
        self.Andy, self.Boa,   self.Coral, self.Dino,  self.Epa, self.Fomi = self.setup_players

        self.table = structures.Table(self.setup_players, min_bet=100)
        self.table.set_starting_player(self.Coral)

        self.betting_round = engines.BettingRound('test', self.table, open_fold_allowed=True)
        self.betting_round.reset_betting_round_states(self.table)

        # SB
        self.Andy.decrease_stack(50)
        self.Andy.increase_bet_level(50)

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        # optional BB
        self.Coral.decrease_stack(100)
        self.Coral.increase_bet_level(100)

        # optional BB
        self.Epa.decrease_stack(100)
        self.Epa.increase_bet_level(100)

        # bet level on BB
        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)


    def run_initial_tests(self):

        "Runs the unit tests for the initial state."

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 950)
                elif player in (self.Boa, self.Coral, self.Epa):
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                elif player in (self.Dino, self.Fomi):
                    self.assertEqual(player.bet_level, 0)
                    self.assertEqual(player.stack, 1000)
                else:
                    raise AssertionError()


class TestBettingRoundRunListenerFunctionStartingWithFold(BaseTestCase):


    "Runs unit tests on run_listener function when the first requested action is fold."


    def test_folds(self):

        "Tests all players folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                if player in (self.Andy, self.Boa, self.Coral, self.Dino, self.Epa):
                    self.assertIsNone(player.pot_index)
                elif player == self.Fomi:
                    self.assertEqual(player.pot_index, 0)


    def test_fold_to_fold_to_checks(self):

        "Tests first two players folding and others checking."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                if player in (self.Andy, self.Boa):
                    self.assertIsNone(player.pot_index)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_fold_to_bet_to_folds(self):

        "Tests first two players folding, next betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_fold_to_bet_to_calls(self):

        "Tests first two players folding, next betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (400,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_check_to_folds(self):

        "Tests first player folding, next checking and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                if player in (self.Andy, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_checks(self):

        "Tests first player folding and others checking."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                if player == self.Andy:
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_check_to_bet_to_folds(self):

        "Tests first player folding, next checking, next betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),    {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_check_to_bet_to_calls(self):

        "Tests first player folding, next checking, next betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (500,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_bet_to_folds(self):

        "Tests first player folding, next betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_bet_to_calls(self):

        "Tests first players fold, next betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (500,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_bet_to_raise_to_folds(self):

        "Tests first player folding, next betting, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (300,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_fold_to_bet_to_raise_to_calls(self):

        "Tests first player folding, next betting, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1000,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


class TestBettingRoundRunListenerFunctionStartingWithCheck(BaseTestCase):


    "Runs unit tests on run_listener function when the first requested action is check."


    def test_check_to_folds(self):

        "Tests first player checking and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                if player == self.Andy:
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertIsNone(player.pot_index)


    def test_check_to_fold_to_checks(self):

        "Tests first player checking, next folding and others checking."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                if player in (self.Andy, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_check_to_fold_to_bet_to_folds(self):

        "Tests first player checking, next folding, next betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),    {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_check_to_fold_to_bet_to_calls(self):

        "Tests first player checking, next folding, next betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (500,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_check_to_check_to_folds(self):

        "Tests first two players checking and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_checks(self):

        "Tests all players checking."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 1000)
                self.assertEqual(player.pot_index, 0)


    def test_check_to_check_to_bet_to_folds(self):

        "Tests first two players checking, next betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),    {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),    {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_check_to_check_to_bet_to_calls(self):

        "Tests first two players checking, next betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (600,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.pot_index, 0)


    def test_check_to_bet_to_folds(self):

        "Tests first player checking, next betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),    {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_check_to_bet_to_calls(self):

        "Tests first player checking, next betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (600,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.pot_index, 0)


    def test_check_to_bet_to_raise_to_folds(self):

        "Tests first player checking, next betting, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (300,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_check_to_bet_to_raise_to_calls(self):

        "Tests first player checking, next betting, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_CHECK),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1200,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 800)
                self.assertEqual(player.pot_index, 0)


class TestBettingRoundRunListenerFunctionStartingWithBet(BaseTestCase):


    "Runs unit tests on run_listener function when the first requested action is bet."


    def test_bet_to_folds(self):

        "Tests first player betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_bet_to_fold_to_calls(self):

        "Tests first player betting, next folding and others checking."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (500,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_bet_to_fold_to_raise_to_folds(self):

        "Tests first player betting, next folding, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (300,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_bet_to_fold_to_raise_to_calls(self):

        "Tests first player betting, next folding, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1000,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_bet_to_call_to_folds(self):

        "Tests first player betting, next calling and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (200,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_bet_to_calls(self):

        "Tests first player betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (600,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.pot_index, 0)


    def test_bet_to_call_to_raise_to_folds(self):

        "Tests first player betting, next calling, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (400,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_bet_to_call_to_raise_to_calls(self):

        "Tests first player betting, next calling, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1200,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 800)
                self.assertEqual(player.pot_index, 0)


    def test_bet_to_raise_to_folds(self):

        "Tests first player betting, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (300,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_bet_to_raise_to_calls(self):

        "Tests first player betting, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1200,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 800)
                self.assertEqual(player.pot_index, 0)


    def test_bet_to_raise_to_raise_to_folds(self):

        "Tests first player betting, next two raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (600,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 800)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_bet_to_raise_to_raise_to_calls(self):

        "Tests first player betting, next two raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Andy,  structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 1001)}),
            (1, self.Boa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Coral, structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (2, self.Andy,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1800,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 700)
                self.assertEqual(player.pot_index, 0)


class TestBettingRoundRunListenerFunctionWithForcedBetsStartingWithFold(BaseForcedBetsTestCase):


    "Runs unit tests on run_listener function when there are forced bets and the first requested action is fold."


    def test_with_blinds_folds(self):

        "Tests all players folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (350,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Coral, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Dino, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_fold_to_checks_or_calls(self):

        "Tests first two players folding and others checking or calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 50),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (500,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_fold_to_bet_to_folds(self):

        "Tests first two players folding, next betting and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151),   constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101),   constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (450,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Dino, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_fold_to_bet_to_calls(self):

        "Tests first two players folding, next betting and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (900,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_check_or_call_to_folds(self):

        "Tests first player folding, next checking or calling and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (450,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_checks_or_calls(self):

        "Tests first player folding and others checking or calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 50),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (600,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 900)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Coral:
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_check_or_call_to_bet_or_raise_to_folds(self):

        "Tests first player folding, next checking or calling, next betting or raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (550,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Dino):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_check_or_call_to_bet_or_raise_to_calls(self):

        "Tests first player folding, next checking or calling, next betting or raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_bet_or_raise_to_folds(self):

        "Tests first player folding, next betting or raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (550,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_bet_or_raise_to_calls(self):

        "Tests first player folding, next betting or raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (1100,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_bet_or_raise_to_raise_to_folds(self):

        "Tests first player folding, next betting or raising, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (750,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 800)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_fold_to_bet_or_raise_to_raise_to_calls(self):

        "Tests first player folding, next betting or raising, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 250),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1600,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


class TestBettingRoundRunListenerFunctionWithForcedBetsStartingWithCheckOrCall(BaseForcedBetsTestCase):


    "Runs unit tests on run_listener function when there are forced bets and the first requested action is fold."


    def test_with_blinds_check_or_call_to_folds(self):

        "Tests first player checking or calling and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (350,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Dino, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_check_or_call_to_fold_to_checks_or_calls(self):

        "Tests player checking or calling, next folding and others checking or calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 50),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (500,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Coral, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_check_or_call_to_fold_to_bet_or_raise_to_folds(self):

        "Tests first player checking or calling, next folding, next betting or raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),    {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (450,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Dino, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_with_blinds_check_or_call_to_fold_to_bet_or_raise_to_calls(self):

        "Tests first player checking or calling, next folding, next betting or raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1000,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Coral, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_check_or_call_to_check_or_call_to_folds(self):

        "Tests first two players checking or calling and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (450,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_checks_or_calls(self):

        "Tests all players checking or calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 50),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(50, 51),   constants.ACTION_RAISE: range(150, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (600,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.pot_index, 0)


    def test_with_blinds_check_or_call_to_check_or_call_to_bet_or_raise_to_folds(self):

        "Tests first two players checking or calling, next betting or raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (550,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Dino):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_check_or_call_to_check_or_call_to_bet_or_raise_to_calls(self):

        "Tests first two players checking or calling, next betting or raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1200,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 800)
                self.assertEqual(player.pot_index, 0)


    def test_with_blinds_check_or_call_to_bet_or_raise_to_folds(self):

        "Tests first player checking or calling, next betting or raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (550,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_check_or_call_to_bet_or_raise_to_calls(self):

        "Tests first player checking or calling, next betting or raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1200,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 800)
                self.assertEqual(player.pot_index, 0)


    def test_with_blinds_check_or_call_to_bet_or_raise_to_raise_to_folds(self):

        "Tests first player checking or calling, next betting or raising, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (750,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Coral):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 800)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_check_or_call_to_bet_or_raise_to_raise_to_calls(self):

        "Tests first player checking or calling, next betting or raising, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_CHECK),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 250),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1800,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 700)
                self.assertEqual(player.pot_index, 0)


class TestBettingRoundRunListenerFunctionWithForcedBetsStartingWithBet(BaseForcedBetsTestCase):


    "Runs unit tests on run_listener function when there are forced bets and the first requested action is bet."


    def test_with_blinds_bet_or_raise_to_folds(self):

        "Tests first player betting or raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),     {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (450,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Dino, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_fold_to_calls(self):

        "Tests player betting or raising, next folding and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (1000,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Coral, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_fold_to_raise_to_folds(self):

        "Tests first player betting or raising, next folding, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (650,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Dino, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_fold_to_raise_to_calls(self):

        "Tests first player betting or raising, next folding, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 250),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1500,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player in (self.Andy, self.Boa, self.Coral, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_call_to_folds(self):

        "Tests first player betting or raising, next calling and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),      {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (650,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 800)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_calls(self):

        "Tests first player betting or raising and next calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 150), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(150, 151), constants.ACTION_RAISE: range(250, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 100), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (1200,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 800)
                self.assertEqual(player.pot_index, 0)


    def test_with_blinds_bet_or_raise_to_call_to_raise_to_folds(self):

        "Tests first player betting or raising, next calling, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
            (2, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (850,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 800)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_call_to_raise_to_calls(self):

        "Tests first player betting or raising, next calling, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 200), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 250),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
            (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1800,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 700)
                self.assertEqual(player.pot_index, 0)


    def test_with_blinds_bet_or_raise_to_raise_to_folds(self):

        "Tests first player betting or raising, next raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (750,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Boa, self.Epa):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 700)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_raise_to_calls(self):

        "Tests first player betting or raising, next raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 250),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(250, 251), constants.ACTION_RAISE: range(350, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 801)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1800,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 700)
                self.assertEqual(player.pot_index, 0)


    def test_with_blinds_bet_or_raise_to_raise_to_raise_to_folds(self):

        "Tests first player betting or raising, next two raising and others folding."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(400, 401), constants.ACTION_RAISE: range(500, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(350, 351), constants.ACTION_RAISE: range(450, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 801)}),
            (2, self.Dino,  structures.Action(constants.ACTION_FOLD),       {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 701)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (1050,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 950)
                    self.assertIsNone(player.pot_index)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 800)
                    self.assertIsNone(player.pot_index)
                elif player == self.Dino:
                    self.assertEqual(player.stack, 700)
                    self.assertIsNone(player.pot_index)
                elif player == self.Epa:
                    self.assertEqual(player.stack, 600)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Fomi:
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_with_blinds_bet_or_raise_to_raise_to_raise_to_calls(self):

        "Tests first player betting or raising, next two raising and others calling."

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100)), # BB
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 300)), # BB
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 400)),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 350)), # SB
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 300)), # BB
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
            (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
        )

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_BET, 100),   {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_RAISE, 300), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 400),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(400, 401), constants.ACTION_RAISE: range(500, 1001)}),
            (1, self.Andy,  structures.Action(constants.ACTION_CALL, 350),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(350, 351), constants.ACTION_RAISE: range(450, 951)}),
            (1, self.Boa,   structures.Action(constants.ACTION_CALL, 300),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(400, 901)}),
            (2, self.Coral, structures.Action(constants.ACTION_CALL, 200),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(300, 801)}),
            (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100),  {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 701)}),
        )

        self.run_initial_tests()
        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 2)

            self.assertTupleEqual(self.table.split_central_pot, (2400,))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                self.assertEqual(player.stack, 600)
                self.assertEqual(player.pot_index, 0)


if __name__ == '__main__':
    main()