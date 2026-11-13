"""
Defines unit tests on BettingRound class run method special cases.
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
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi = self.setup_players

        self.betting_round = engines.BettingRound('test', self.table, open_fold_allowed=True)


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
                self.assertEqual(self.table.current_player, player)
                self.assertEqual(self.betting_round.lap_counts, lap)

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


class TestBettingRoundRunListenerFunctionHavingSBAllInEveryoneFolds(BaseTestCase):


    """
    Runs unit tests on run_listener function when the small blind goes all-in by placing the amount
    and the big blind cannot play because everyone else is either folded or started all-in.
    """


    def test_sb_all_in_when_all_fold_and_no_optional_blinds(self):

        "Tests every one folds being there no optional blinds."

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)

        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.pot_index, 0)
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                elif player == self.Boa:
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.bet_level, 0)
                    self.assertEqual(player.stack, 1000)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (100, 50))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_sb_all_in_when_all_start_all_in_and_no_optional_blinds(self):

        "Tests every one starts all-in, except the blinds, being there no optional blinds."

        # antes
        for player in self.setup_players:
            self.table.increase_central_pot(10) # ante
        self.table.add_side_pot()

        # starting all-in
        for player in (self.Coral, self.Dino, self.Epa, self.Fomi):
            player.decrease_stack(player.stack)

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)
        self.Andy.increase_pot_index()

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)
        self.Boa.increase_pot_index()

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = ()

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (60, 0))

            for player in self.setup_players:
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
                elif player == self.Boa:
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.bet_level, 0)
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (60, 100, 50))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 2)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_sb_all_in_when_all_fold_and_one_optional_blind(self):

        "Tests every one folds including one optional blind."

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        # optional BB
        self.Coral.decrease_stack(100)
        self.Coral.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.pot_index, 0)
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                elif player in (self.Boa, self.Coral):
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                elif player in (self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.bet_level, 0)
                    self.assertEqual(player.stack, 1000)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (150, 100))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_sb_all_in_when_all_start_all_in_and_one_optional_blind(self):

        "Tests every one starts all-in, except the blinds and one optional blind that folds."

        # antes
        for player in self.setup_players:
            self.table.increase_central_pot(10) # ante
        self.table.add_side_pot()

        # starting all-in
        for player in (self.Dino, self.Epa, self.Fomi):
            player.decrease_stack(player.stack)

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)
        self.Andy.increase_pot_index()

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)
        self.Boa.increase_pot_index()

        # optional BB
        self.Coral.decrease_stack(100)
        self.Coral.increase_bet_level(100)
        self.Coral.increase_pot_index()

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 901)}),
        )

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (60, 0))

            for player in self.setup_players:
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Boa, self.Coral):
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.bet_level, 0)
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (60, 150, 100))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 2)
                elif player == self.Coral:
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_sb_all_in_when_all_fold_and_two_optional_blinds(self):

        "Tests every one folds including two optional blinds."

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        # optional BBs
        for player in (self.Coral, self.Dino):
            player.decrease_stack(100)
            player.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(100, 901)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(100, 101), constants.ACTION_RAISE: range(200, 1001)}),
        )

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.pot_index, 0)
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                elif player in (self.Boa, self.Coral, self.Dino):
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                elif player in (self.Epa, self.Fomi):
                    self.assertEqual(player.bet_level, 0)
                    self.assertEqual(player.stack, 1000)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (200, 150))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_sb_all_in_when_all_start_all_in_and_two_optional_blinds(self):

        "Tests every one starts all-in, except the blinds and two optional blinds that fold."

        # antes
        for player in self.setup_players:
            self.table.increase_central_pot(10) # ante
        self.table.add_side_pot()

        # starting all-in
        for player in (self.Epa, self.Fomi):
            player.decrease_stack(player.stack)

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)
        self.Andy.increase_pot_index()

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)
        self.Boa.increase_pot_index()

        # optional BBs
        for player in (self.Coral, self.Dino):
            player.decrease_stack(100)
            player.increase_bet_level(100)
            player.increase_pot_index()

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 901)}),
        )

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (60, 0))

            for player in self.setup_players:
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Boa, self.Coral, self.Dino):
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Epa, self.Fomi):
                    self.assertEqual(player.bet_level, 0)
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (60, 200, 150))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 2)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                elif player in (self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    raise AssertionError()


    def test_sb_all_in_when_all_fold_and_all_optional_blinds(self):

        "Tests every one folds being all optional blinds."

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        # optional BBs
        for player in (self.Coral, self.Dino, self.Epa, self.Fomi):
            player.decrease_stack(100)
            player.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 901)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 901)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(100, 901)}),
        )

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.pot_index, 0)
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                elif player in (self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (300, 250))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900)
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


    def test_sb_all_in_when_all_fold_and_all_different_size_optional_blinds(self):

        """
        Tests every one folds being all optional blinds of different sizes. This is a weird case
        covered by refund function. In a normal game, optional blinds are always big blinds, but
        who knows, there are some awful poker varieties nowadays that people like anyway. Setup for
        cases like this may be delivered in a future version.
        """

        # SB (all-in)
        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_bet_level(50)

        # BB
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        # optional BB 1
        self.Coral.decrease_stack(100)
        self.Coral.increase_bet_level(100)

        # optional BB 2
        for player in (self.Dino, self.Epa):
            player.decrease_stack(200)
            player.increase_bet_level(200)

        # optional BB 3
        self.Fomi.decrease_stack(400)
        self.Fomi.increase_bet_level(400)

        # table starting conditions
        self.table.set_bet_level(400)
        self.table.set_full_bet_level(400)
        self.table.set_min_bet(400) # this is not being set/reset by the engine yet
        self.table.set_min_raise_increase(400)
        self.table.set_starting_player(self.Coral)

        laps_and_players_and_actions_and_ranges = (
            (1, self.Coral, structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(300, 301), constants.ACTION_RAISE: range(700, 901)}),
            (1, self.Dino,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(600, 801)}),
            (1, self.Epa,   structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CALL: range(200, 201), constants.ACTION_RAISE: range(600, 801)}),
            (1, self.Fomi,  structures.Action(constants.ACTION_FOLD), {constants.ACTION_FOLD: range(0, 1), constants.ACTION_CHECK: range(0, 1),    constants.ACTION_BET: range(400, 601)}),
        )

        with self.subTest('initial state'):

            self.assertFalse(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 0)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

            for player in self.setup_players:
                self.assertEqual(player.pot_index, 0)
                if player == self.Andy:
                    self.assertEqual(player.bet_level, 50)
                    self.assertEqual(player.stack, 0)
                elif player in (self.Boa, self.Coral):
                    self.assertEqual(player.bet_level, 100)
                    self.assertEqual(player.stack, 900)
                elif player in (self.Dino, self.Epa):
                    self.assertEqual(player.bet_level, 200)
                    self.assertEqual(player.stack, 800)
                elif player == self.Fomi:
                    self.assertEqual(player.bet_level, 400)
                    self.assertEqual(player.stack, 600)
                else:
                    raise AssertionError()

        self.run_yield_and_closure_tests(laps_and_players_and_actions_and_ranges)

        with self.subTest('final state'):

            self.assertTrue(self.betting_round.is_completed)
            self.assertEqual(self.betting_round.lap_counts, 1)

            self.assertTupleEqual(self.table.split_central_pot, (300, 250))

            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
                if player == self.Andy:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                elif player == self.Boa:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.pot_index, 1)
                elif player in (self.Coral, self.Dino, self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 900) # refunds
                    self.assertIsNone(player.pot_index)
                else:
                    raise AssertionError()


# class TestBettingRoundRunListenerFunctionHavingBBAllIn(BaseTestCase):


#     "Runs unit tests on run_listener function, having the big blind is all-in and the small blind cannot play because everyone else is folded or all-in for equal or less than a small blind."


#     def run_action_tests(
#         self,
#         laps_and_players_and_actions_and_ranges: tuple[
#             tuple[int, structures.Player, structures.Action],
#             ...
#         ],
#     ):

#         "Runs the shared validations for the action tests."

#         generator = engines.run_betting_round_listener(self.betting_round)

#         for lap, player, action in laps_and_players_and_actions_and_ranges:
#             await_state = next(generator)
#             with self.subTest(player=player, action=action):
#                 self.assertEqual(await_state.player, player)
#                 self.assertEqual(self.betting_round.lap_counts, lap)
#             await_state.request_action(action)

#         with self.subTest('last step'):
#             with self.assertRaises(StopIteration) as context:
#                 next(generator)
#             self.assertIsNone(context.exception.value)


#     def test_bb_all_in_when_deepest_pot_has_no_folded_player(self):

#         "Tests an optional big blind folds as well as every one else, so nobody pays the placed amount."

#         # SB
#         self.Andy.decrease_stack(50)
#         self.Andy.increase_bet_level(50)

#         # BB (incomplete, all-in)
#         self.Boa.decrease_stack(self.Boa.stack)
#         self.Boa.increase_bet_level(50)

#         # table starting conditions
#         self.table.set_bet_level(100)
#         self.table.set_full_bet_level(100)
#         self.table.set_starting_player(self.Coral)
#         self.table.set_stopping_player(self.Boa)

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
#             (1, self.Dino,  structures.Action(constants.ACTION_FOLD)),
#             (1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
#         )

#         with self.subTest('before actions'):
#             self.assertEqual(self.betting_round.lap_counts, 0)
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 1000)
#             self.assertEqual(self.Dino.stack, 1000)
#             self.assertEqual(self.Epa.stack, 1000)
#             self.assertEqual(self.Fomi.stack, 1000)
#             self.assertTupleEqual(self.table.split_central_pot, (0,))

#         self.run_action_tests(laps_and_players_and_actions_and_ranges)

#         with self.subTest('after actions'):
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 1000)
#             self.assertEqual(self.Dino.stack, 1000)
#             self.assertEqual(self.Epa.stack, 1000)
#             self.assertEqual(self.Fomi.stack, 1000)
#             self.assertTupleEqual(self.table.split_central_pot, (100,))


#     def test_bb_all_in_when_deepest_pot_has_a_single_folded_player(self):

#         "Tests an optional big blind folds as well as every one else, so nobody pays the placed amount."

#         # SB
#         self.Andy.decrease_stack(50)
#         self.Andy.increase_bet_level(50)

#         # BB (incomplete, all-in)
#         self.Boa.decrease_stack(self.Boa.stack)
#         self.Boa.increase_bet_level(50)

#         # optional BB
#         self.Coral.decrease_stack(100)
#         self.Coral.increase_bet_level(100)

#         # table starting conditions
#         self.table.set_bet_level(100)
#         self.table.set_full_bet_level(100)
#         self.table.set_starting_player(self.Coral)
#         self.table.set_stopping_player(self.Boa)

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
#             (1, self.Dino,  structures.Action(constants.ACTION_FOLD)),
#             (1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
#         )

#         with self.subTest('before actions'):
#             self.assertEqual(self.betting_round.lap_counts, 0)
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 900)
#             self.assertEqual(self.Dino.stack, 1000)
#             self.assertEqual(self.Epa.stack, 1000)
#             self.assertEqual(self.Fomi.stack, 1000)
#             self.assertTupleEqual(self.table.split_central_pot, (0,))

#         self.run_action_tests(laps_and_players_and_actions_and_ranges)

#         with self.subTest('after actions'):
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 950) # refund 50 excess
#             self.assertEqual(self.Dino.stack, 1000)
#             self.assertEqual(self.Epa.stack, 1000)
#             self.assertEqual(self.Fomi.stack, 1000)
#             self.assertTupleEqual(self.table.split_central_pot, (150,))


#     def test_bb_all_in_when_deepest_pot_has_multiple_folded_player(self):

#         "Tests multiple optional big blinds fold as well as every one else, so nobody pays the placed amount."

#         # SB
#         self.Andy.decrease_stack(50)
#         self.Andy.increase_bet_level(50)

#         # BB (incomplete, all-in)
#         self.Boa.decrease_stack(self.Boa.stack)
#         self.Boa.increase_bet_level(50)

#         # optional BB
#         self.Coral.decrease_stack(100)
#         self.Coral.increase_bet_level(100)

#         # optional BB
#         self.Dino.decrease_stack(100)
#         self.Dino.increase_bet_level(100)

#         # table starting conditions
#         self.table.set_bet_level(100)
#         self.table.set_full_bet_level(100)
#         self.table.set_starting_player(self.Coral)
#         self.table.set_stopping_player(self.Boa)

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
#             (1, self.Dino,  structures.Action(constants.ACTION_FOLD)),
#             (1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
#         )

#         with self.subTest('before actions'):
#             self.assertEqual(self.betting_round.lap_counts, 0)
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 900)
#             self.assertEqual(self.Dino.stack, 900)
#             self.assertEqual(self.Epa.stack, 1000)
#             self.assertEqual(self.Fomi.stack, 1000)
#             self.assertTupleEqual(self.table.split_central_pot, (0,))

#         self.run_action_tests(laps_and_players_and_actions_and_ranges)

#         with self.subTest('after actions'):
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 950) # refund 50 excess
#             self.assertEqual(self.Dino.stack, 950) # refund 50 excess
#             self.assertEqual(self.Epa.stack, 1000)
#             self.assertEqual(self.Fomi.stack, 1000)
#             self.assertTupleEqual(self.table.split_central_pot, (200,))


#     def test_bb_all_in_when_two_deepest_pots_have_multiple_folded_player(self):

#         """
#         Tests multiple optional blinds from different sizes fold as well as every one else, so nobody pays the placed amount.
#         This is a weird case because usually optional blind is always a big blind, but who knows, there are some awful poker versions nowadays that people like anyway.
#         """

#         # SB
#         self.Andy.decrease_stack(50)
#         self.Andy.increase_bet_level(50)

#         # BB (incomplete, all-in)
#         self.Boa.decrease_stack(self.Boa.stack)
#         self.Boa.increase_bet_level(50)

#         # optional BB
#         self.Coral.decrease_stack(100)
#         self.Coral.increase_bet_level(100)

#         # optional BB
#         self.Dino.decrease_stack(100)
#         self.Dino.increase_bet_level(100)

#         # optional BB
#         self.Epa.decrease_stack(200)
#         self.Epa.increase_bet_level(200)

#         # optional BB
#         self.Fomi.decrease_stack(200)
#         self.Fomi.increase_bet_level(200)

#         # table starting conditions
#         self.table.set_bet_level(200)
#         self.table.set_full_bet_level(200)
#         self.table.set_starting_player(self.Coral)
#         self.table.set_stopping_player(self.Boa)

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Coral, structures.Action(constants.ACTION_FOLD)),
#             (1, self.Dino,  structures.Action(constants.ACTION_FOLD)),
#             (1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
#         )

#         with self.subTest('before actions'):
#             self.assertEqual(self.betting_round.lap_counts, 0)
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 900)
#             self.assertEqual(self.Dino.stack, 900)
#             self.assertEqual(self.Epa.stack, 800)
#             self.assertEqual(self.Fomi.stack, 800)
#             self.assertTupleEqual(self.table.split_central_pot, (0,))

#         self.run_action_tests(laps_and_players_and_actions_and_ranges)

#         with self.subTest('after actions'):
#             self.assertEqual(self.Andy.stack, 950)
#             self.assertEqual(self.Boa.stack, 0)
#             self.assertEqual(self.Coral.stack, 950) # refund 50 excess
#             self.assertEqual(self.Dino.stack, 950) # refund 50 excess
#             self.assertEqual(self.Epa.stack, 950) # refund 150 excess
#             self.assertEqual(self.Fomi.stack, 950) # refund 150 excess
#             self.assertTupleEqual(self.table.split_central_pot, (300,))


# class TestBettingRoundRunListenerFunctionAllInChain(BaseTestCase):


#     "Runs unit tests on run_listener function chaining actions to make all players go all-in."


#     def test_all_in_chain_starting_with_full_stacks(self):

#         "Tests players going all-in starting with full stacks."

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Andy,  structures.Action(constants.ACTION_CHECK)),
#             (1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
#             (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
#             (1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
#             (1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_BET, 100)), # +100
#             (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Epa, structures.Action(constants.ACTION_RAISE, 300)), # +200
#             (2, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
#             (3, self.Andy,  structures.Action(constants.ACTION_CALL, 200)),
#             (3, self.Boa,   structures.Action(constants.ACTION_CALL, 200)),
#             (3, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
#             (3, self.Dino,  structures.Action(constants.ACTION_RAISE, 500)), # +300
#             (3, self.Epa, structures.Action(constants.ACTION_CALL, 300)),
#             (3, self.Fomi, structures.Action(constants.ACTION_CALL, 300)),
#             (4, self.Andy,  structures.Action(constants.ACTION_CALL, 300)),
#             (4, self.Boa,   structures.Action(constants.ACTION_CALL, 300)),
#             (4, self.Coral, structures.Action(constants.ACTION_RAISE, 700)), # +400
#             (4, self.Dino,  structures.Action(constants.ACTION_CALL, 400)),
#             (4, self.Epa, structures.Action(constants.ACTION_CALL, 400)),
#             (4, self.Fomi, structures.Action(constants.ACTION_CALL, 400)),
#             (5, self.Andy,  structures.Action(constants.ACTION_CALL, 400)),
#             (5, self.Boa,   structures.Action(constants.ACTION_CALL, 400)),
#         )

#         self.run_test(laps_and_players_and_actions_and_ranges)


#     def test_all_in_chain_starting_with_full_stacks_and_forced_bets(self):

#         "Tests players going all-in starting with full stacks, some of them placing forced bets."

#         BaseForcedBetsTestCase.setUp(self)

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
#             (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
#             (1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
#             (1, self.Andy,  structures.Action(constants.ACTION_CALL, 50)),
#             (1, self.Boa,   structures.Action(constants.ACTION_BET, 200)), # +200
#             (2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
#             (2, self.Dino,  structures.Action(constants.ACTION_CALL, 200)),
#             (2, self.Epa, structures.Action(constants.ACTION_CALL, 200)),
#             (2, self.Fomi, structures.Action(constants.ACTION_CALL, 200)),
#             (2, self.Andy,  structures.Action(constants.ACTION_RAISE, 500)), # +300
#             (2, self.Boa,   structures.Action(constants.ACTION_CALL, 300)),
#             (3, self.Coral, structures.Action(constants.ACTION_CALL, 300)),
#             (3, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),
#             (3, self.Epa, structures.Action(constants.ACTION_CALL, 300)),
#             (3, self.Fomi, structures.Action(constants.ACTION_RAISE, 700)), # +400
#             (3, self.Andy,  structures.Action(constants.ACTION_CALL, 400)),
#             (3, self.Boa,   structures.Action(constants.ACTION_CALL, 400)),
#             (4, self.Coral, structures.Action(constants.ACTION_CALL, 400)),
#             (4, self.Dino,  structures.Action(constants.ACTION_CALL, 400)),
#             (4, self.Epa, structures.Action(constants.ACTION_CALL, 400)),
#         )

#         self.run_test(laps_and_players_and_actions_and_ranges)


#     def test_all_in_chain_starting_with_under_stacks(self):

#         "Tests players going all-in starting with stacks smaller than full stacks."

#         for player in self.setup_players:
#             player.decrease_stack(player.stack)

#         self.Andy.increase_stack(200)
#         self.Boa.increase_stack(200)
#         self.Coral.increase_stack(500)
#         self.Dino.increase_stack(500)
#         self.Epa.increase_stack(1000)
#         self.Fomi.increase_stack(1000)

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Andy,  structures.Action(constants.ACTION_CHECK)),
#             (1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
#             (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
#             (1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
#             (1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_BET, 100)), # +100
#             (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Boa,   structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Coral, structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
#             (2, self.Epa, structures.Action(constants.ACTION_RAISE, 300)), # +200
#             (2, self.Fomi, structures.Action(constants.ACTION_RAISE, 500)), # +300
#             (3, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
#             (3, self.Boa,   structures.Action(constants.ACTION_CALL, 100)),
#             (3, self.Coral, structures.Action(constants.ACTION_CALL, 400)),
#             (3, self.Dino,  structures.Action(constants.ACTION_CALL, 400)),
#             (3, self.Epa, structures.Action(constants.ACTION_RAISE, 700)), # +400
#             (3, self.Fomi, structures.Action(constants.ACTION_CALL, 400)),
#         )

#         self.run_test(laps_and_players_and_actions_and_ranges)


#     def test_all_in_chain_starting_with_under_stacks_and_forced_bets(self):

#         "Tests players going all-in starting with stacks smaller than full stacks, some of them placing forced bets."

#         BaseForcedBetsTestCase.setUp(self)

#         for player in self.setup_players:
#             player.decrease_stack(player.stack)

#         self.Andy.increase_stack(150) # already placed 50 SB
#         self.Boa.increase_stack(100) # already placed 100 BB
#         self.Coral.increase_stack(400) # already placed optional 100 BB
#         self.Dino.increase_stack(500)
#         self.Epa.increase_stack(900) # already placed optional 100 BB
#         self.Fomi.increase_stack(1000)

#         laps_and_players_and_actions_and_ranges = (
#             (1, self.Coral, structures.Action(constants.ACTION_CHECK)),
#             (1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
#             (1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
#             (1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
#             (1, self.Andy,  structures.Action(constants.ACTION_CALL, 50)),
#             (1, self.Boa,   structures.Action(constants.ACTION_BET, 100)), # +100
#             (2, self.Coral, structures.Action(constants.ACTION_RAISE, 200)), # +100
#             (2, self.Dino,  structures.Action(constants.ACTION_CALL, 200)),
#             (2, self.Epa, structures.Action(constants.ACTION_CALL, 200)),
#             (2, self.Fomi, structures.Action(constants.ACTION_RAISE, 500)), # +300
#             (2, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
#             (3, self.Coral, structures.Action(constants.ACTION_CALL, 200)),
#             (3, self.Dino,  structures.Action(constants.ACTION_CALL, 200)),
#             (3, self.Epa, structures.Action(constants.ACTION_RAISE, 700)), # +400
#             (3, self.Fomi, structures.Action(constants.ACTION_CALL, 400)),
#         )

#         self.run_test(laps_and_players_and_actions_and_ranges)


if __name__ == '__main__':
    main()