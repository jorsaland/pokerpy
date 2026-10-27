"""
Defines unit tests on BettingRound class run method.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


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
            structures.Player('Goma', 1000),
            structures.Player('Hilo', 0),
            structures.Player('Iris', 0),
        ]

        self.table = structures.Table(self.setup_players, min_bet=100)
        (
            self.Andy,
            self.Boa,
            self.Coral,
            self.Dino,
            self.Epa,
            self.Fomi,
            self.Goma,
            self.Hilo,
            self.Iris
        ) = self.setup_players

        self.hand_cycle = engines.HandCycle(
            'test',
            self.table,
            raise_invalid_actions = True,
            open_fold_allowed = True
        )

        self.table.set_ante(10)
        self.table.set_small_blind(50)
        self.table.set_big_blind(100)
        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        self.Fomi.mark_is_extra_blind()
        self.Goma.mark_is_extra_blind()

        self.extra_blind_candidates = (self.Dino, self.Epa, self.Fomi, self.Goma, self.Andy)


    def run_test(
        self,
        round_and_laps_and_players_and_actions: tuple[
            tuple[str, int, structures.Player, structures.Action],
            ...
        ]
    ):

        "Runs the shared validations for the tests."

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before generator start-up'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in (self.Hilo, self.Iris):
                self.assertFalse(player.is_folded)

        with self.subTest('after generator start-up'):
            next_player = next(generator)
            self.assertIsNotNone(self.hand_cycle.betting_round)
            for player in (self.Hilo, self.Iris):
                self.assertTrue(player.is_folded)

        for i, player in enumerate(self.extra_blind_candidates, 1):
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertEqual(next_player, player)
                if i < len(self.extra_blind_candidates):
                    next_player = next(generator)

        with self.subTest('extra blinds to action transition'):
            self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
            next_player = next(generator)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)

        for i, (round_name, lap, player, action) in enumerate(round_and_laps_and_players_and_actions, 1):
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
                player.request_action(action)
                if i < len(round_and_laps_and_players_and_actions):
                    next_player = next(generator)

        with self.subTest('listener termination'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


class TestHandCycleRunListenerFunctionUpToAnteRound(BaseTestCase):


    "Runs unit tests on run_listener function, ending in the ante round."


    def test_up_to_ante_round_with_no_actionable_player(self):

        "Tests going up to the ante round, with no actionable players left."

        for player in self.setup_players:
            player.decrease_stack(player.stack)
            if player == self.Andy:
                player.increase_stack(1)
            if player in (self.Boa, self.Coral, self.Dino, self.Epa):
                player.increase_stack(5)
            else:
                player.increase_stack(10) # ante

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('listener start-up and termination'):
            self.assertIsNone(self.hand_cycle.betting_round)
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_ante_round_with_one_actionable_player(self):

        "Tests going up to the ante round, with only one actionable player left."

        for player in self.setup_players:
            if player == self.Andy:
                continue
            player.decrease_stack(player.stack)
            if player in (self.Boa, self.Coral, self.Dino, self.Epa):
                player.increase_stack(5)
            else:
                player.increase_stack(10) # ante

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('listener start-up and termination'):
            self.assertIsNone(self.hand_cycle.betting_round)
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_pre_flop_with_all_players_all_in_at_forced_blind_phase(self):

        "Tests going up to the pre-flop, ending in the forced-blind-placing phase."

        for player in self.setup_players:
            player.decrease_stack(player.stack)
            if player == self.Boa:
                player.increase_stack(60) # ante + SB
            elif player == self.Coral:
                player.increase_stack(110) # ante + BB
            else:
                player.increase_stack(10) # ante

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('listener start-up and termination'):
            self.assertIsNone(self.hand_cycle.betting_round)
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_pre_flop_with_all_players_all_in_at_extra_blind_phase(self):

        "Tests going up to the pre-flop, ending in the extra-blind-placing phase."

        for player in self.setup_players:
            player.decrease_stack(player.stack)
            if player == self.Boa:
                player.increase_stack(60) # ante + SB
            elif player in (self.Coral, self.Goma, self.Hilo):
                player.increase_stack(110) # ante + BB
            else:
                player.increase_stack(10) # ante

        self.extra_blind_candidates = (self.Goma, self.Hilo)
        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('listener start-up'):
            self.assertIsNone(self.hand_cycle.betting_round)
            next_player = next(generator)
            self.assertIsNotNone(self.hand_cycle.betting_round)

        for i, player in enumerate(self.extra_blind_candidates, 1):
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertEqual(next_player, player)
                if i < len(self.extra_blind_candidates):
                    next_player = next(generator)

        with self.subTest('listener termination'):
            self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertIsNone(self.hand_cycle.betting_round)


class TestHandCycleRunListenerFunctionUpToPreFlop(BaseTestCase):


    "Runs unit tests on run_listener function, with action parses going up to the pre-flop."


    def test_up_to_pre_flop_with_all_players_folding(self):

        "Tests with action parses going up to the pre-flop, ending with all players fold (but the winner)."

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_BET, 400)),
            (constants.PREFLOP, 2, self.Dino,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.PREFLOP, 2, self.Epa,   structures.Action(constants.ACTION_RAISE, 890)), # all-in
            (constants.PREFLOP, 2, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 2, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 2, self.Andy,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 2, self.Boa,   structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 2, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 3, self.Dino,  structures.Action(constants.ACTION_FOLD)),

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_pre_flop_with_all_players_all_in(self):

        "Tests with action parses going up to the pre-flop, ending with all players going all-in."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_BET, 390)), # all-in
            (constants.PREFLOP, 2, self.Dino,  structures.Action(constants.ACTION_CALL, 390)),
            (constants.PREFLOP, 2, self.Epa,   structures.Action(constants.ACTION_RAISE, 800)),
            (constants.PREFLOP, 2, self.Fomi,  structures.Action(constants.ACTION_CALL, 800)),
            (constants.PREFLOP, 2, self.Goma,  structures.Action(constants.ACTION_CALL, 800)),
            (constants.PREFLOP, 2, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.PREFLOP, 2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.PREFLOP, 3, self.Dino,  structures.Action(constants.ACTION_RAISE, 500)), # all-in
            (constants.PREFLOP, 3, self.Epa,   structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.PREFLOP, 3, self.Fomi,   structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.PREFLOP, 3, self.Goma,   structures.Action(constants.ACTION_CALL, 90)), # all-in

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_pre_flop_with_mixed_final_setups(self):

        "Tests with action parses going up to the pre-flop, with players ending in mixed situations."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_BET, 390)), # all-in
            (constants.PREFLOP, 2, self.Dino,  structures.Action(constants.ACTION_CALL, 390)),
            (constants.PREFLOP, 2, self.Epa,   structures.Action(constants.ACTION_RAISE, 800)),
            (constants.PREFLOP, 2, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 2, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 2, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.PREFLOP, 2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.PREFLOP, 3, self.Dino,  structures.Action(constants.ACTION_RAISE, 500)), # all-in
            (constants.PREFLOP, 3, self.Epa,   structures.Action(constants.ACTION_CALL, 90)), # all-in

        )

        self.run_test(round_and_laps_and_players_and_actions)


class TestHandCycleRunListenerFunctionUpToFlop(BaseTestCase):


    "Runs unit tests on run_listener function, with action parses going up to the flop."


    def test_up_to_flop_with_all_players_folding(self):

        "Tests with action parses going up to the flop, ending with all players fold (but the winner)."

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    2, self.Dino,  structures.Action(constants.ACTION_FOLD)),

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_flop_with_all_players_all_in(self):

        "Tests with action parses going up to the flop, ending with all players going all-in."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.FLOP,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.FLOP,    2, self.Dino,  structures.Action(constants.ACTION_RAISE, 590)), # all-in
            (constants.FLOP,    2, self.Epa,   structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.FLOP,    2, self.Fomi,  structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.FLOP,    2, self.Goma,  structures.Action(constants.ACTION_CALL, 290)), # all-in

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_flop_with_mixed_final_setups(self):

        "Tests with action parses going up to the flop, with players ending in mixed situations."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.FLOP,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.FLOP,    2, self.Dino,  structures.Action(constants.ACTION_RAISE, 590)), # all-in
            (constants.FLOP,    2, self.Epa,   structures.Action(constants.ACTION_CALL, 290)), # all-in

        )

        self.run_test(round_and_laps_and_players_and_actions)


class TestHandCycleRunListenerFunctionUpToTurn(BaseTestCase):


    "Runs unit tests on run_listener function, with action parses going up to the turn."


    def test_up_to_turn_with_all_players_folding(self):

        "Tests with action parses going up to the turn, ending with all players fold (but the winner)."

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),

            (constants.TURN,    1, self.Coral,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_BET, 400)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    2, self.Coral,   structures.Action(constants.ACTION_FOLD)),

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_turn_with_all_players_all_in(self):

        "Tests with action parses going up to the turn, ending with all players going all-in."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.FLOP,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.FLOP,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_BET, 290)), # all-in
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 290)), # all-in

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_turn_with_mixed_final_setups(self):

        "Tests with action parses going up to the turn, with players ending in mixed situations."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.FLOP,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.FLOP,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_BET, 290)), # all-in
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_FOLD)),

        )

        self.run_test(round_and_laps_and_players_and_actions)


class TestHandCycleRunListenerFunctionUpToRiver(BaseTestCase):


    "Runs unit tests on run_listener function, with action parses going up to the river."


    def test_up_to_river_with_all_players_actionable(self):

        "Tests with action parses going up to the river, ending with all players actionable."

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),

            (constants.RIVER,   1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.RIVER,   1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_BET, 400)),
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Fomi,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Goma,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Andy,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   2, self.Boa,   structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   2, self.Coral, structures.Action(constants.ACTION_CALL, 400)),

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_river_with_all_players_folding(self):

        "Tests with action parses going up to the river, ending with all players fold (but the winner)."

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_FOLD)),

            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_BET, 400)),
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_FOLD)),

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_river_with_all_players_all_in(self):

        "Tests with action parses going up to the river, ending with all players going all-in."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.TURN,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.TURN,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.TURN,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_BET, 290)), # all-in
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.RIVER,   1, self.Fomi,  structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.RIVER,   1, self.Goma,  structures.Action(constants.ACTION_CALL, 290)), # all-in

        )

        self.run_test(round_and_laps_and_players_and_actions)


    def test_up_to_river_with_mixed_final_setups(self):

        "Tests with action parses going up to the river, with players ending in mixed situations."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 90)), # all-in
            (constants.TURN,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 390)), # all-in
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_CALL, 290)), # all-in
            (constants.TURN,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_CHECK)),

        )

        self.run_test(round_and_laps_and_players_and_actions)


if __name__ == '__main__':
    main()