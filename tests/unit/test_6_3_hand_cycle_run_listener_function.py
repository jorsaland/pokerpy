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
            structures.Player('Goma', 1000),
            structures.Player('Hilo', 1000),
            structures.Player('Iris', 1000),
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

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)
        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)


class TestHandCycleRunListenerFunctionUpToTurn(BaseTestCase):


    "Runs unit tests on run_listener function, going up to the turn."


    def test_up_to_river_with_all_players_folding(self):

        "Tests going up to the turn, ending with all players fold (but the winner)."

        self.Goma.mark_is_extra_blind()
        self.Hilo.mark_is_extra_blind()

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Iris,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Hilo,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),

            (constants.TURN,    1, self.Coral,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_BET, 400)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    2, self.Coral,   structures.Action(constants.ACTION_FOLD)),

        )

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before actions'):
            self.assertIsNone(self.hand_cycle.betting_round)

        for player in (self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(next_player, player)

        for round_name, lap, player, action in round_and_laps_and_players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
            player.request_action(action)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_river_with_all_players_all_in(self):

        "Tests going up to the turn, ending with all players going all-in."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        self.Goma.mark_is_extra_blind()
        self.Hilo.mark_is_extra_blind()

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Iris,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Hilo,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Iris,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)), # all-in
            (constants.FLOP,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 400)), # all-in
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.FLOP,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_BET, 300)), # all-in
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.TURN,    1, self.Hilo,  structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.TURN,    1, self.Iris,  structures.Action(constants.ACTION_CALL, 300)), # all-in

        )

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before actions'):
            self.assertIsNone(self.hand_cycle.betting_round)

        for player in (self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(next_player, player)

        for round_name, lap, player, action in round_and_laps_and_players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
            player.request_action(action)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_river_with_mixed_final_setups(self):

        "Tests going up to the turn, with players ending in mixed situations."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        self.Goma.mark_is_extra_blind()
        self.Hilo.mark_is_extra_blind()

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Iris,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Hilo,  structures.Action(constants.ACTION_FOLD)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)), # all-in
            (constants.FLOP,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 400)), # all-in
            (constants.FLOP,    2, self.Coral, structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.FLOP,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_BET, 300)), # all-in
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),

        )

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before actions'):
            self.assertIsNone(self.hand_cycle.betting_round)

        for player in (self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(next_player, player)

        for round_name, lap, player, action in round_and_laps_and_players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
            player.request_action(action)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


class TestHandCycleRunListenerFunctionUpToRiver(BaseTestCase):


    "Runs unit tests on run_listener function, going up to the river."


    def test_up_to_river_with_all_players_actionable(self):

        "Tests going up to the river, ending with all players actionable."

        self.Goma.mark_is_extra_blind()
        self.Hilo.mark_is_extra_blind()

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Iris,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Iris,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Hilo,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Iris,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_CALL, 200)),

            (constants.RIVER,   1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.RIVER,   1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_BET, 400)),
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Fomi,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Goma,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Hilo,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Iris,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   1, self.Andy,  structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   2, self.Boa,   structures.Action(constants.ACTION_CALL, 400)),
            (constants.RIVER,   2, self.Coral, structures.Action(constants.ACTION_CALL, 400)),

        )

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before actions'):
            self.assertIsNone(self.hand_cycle.betting_round)

        for player in (self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(next_player, player)

        for round_name, lap, player, action in round_and_laps_and_players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
            player.request_action(action)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_river_with_all_players_folding(self):

        "Tests going up to the river, ending with all players fold (but the winner)."

        self.Goma.mark_is_extra_blind()
        self.Hilo.mark_is_extra_blind()

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Iris,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    1, self.Hilo,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_FOLD)),

            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_BET, 400)),
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_FOLD)),
            (constants.RIVER,   1, self.Fomi,  structures.Action(constants.ACTION_FOLD)),

        )

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before actions'):
            self.assertIsNone(self.hand_cycle.betting_round)

        for player in (self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(next_player, player)

        for round_name, lap, player, action in round_and_laps_and_players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
            player.request_action(action)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_river_with_all_players_all_in(self):

        "Tests going up to the river, ending with all players going all-in."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        self.Goma.mark_is_extra_blind()
        self.Hilo.mark_is_extra_blind()

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Iris,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Iris,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.TURN,    1, self.Hilo,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.TURN,    1, self.Iris,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.TURN,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)), # all-in
            (constants.TURN,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 400)), # all-in
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.TURN,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_BET, 300)), # all-in
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.RIVER,   1, self.Fomi,  structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.RIVER,   1, self.Goma,  structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.RIVER,   1, self.Hilo,  structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.RIVER,   1, self.Iris,  structures.Action(constants.ACTION_CALL, 300)), # all-in

        )

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before actions'):
            self.assertIsNone(self.hand_cycle.betting_round)

        for player in (self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(next_player, player)

        for round_name, lap, player, action in round_and_laps_and_players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
            player.request_action(action)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


    def test_up_to_river_with_mixed_final_setups(self):

        "Tests going up to the river, with players ending in mixed situations."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(200)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(500)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(500)

        self.Goma.mark_is_extra_blind()
        self.Hilo.mark_is_extra_blind()

        round_and_laps_and_players_and_actions = (

            (constants.PREFLOP, 1, self.Dino,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Epa,   structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Fomi,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.PREFLOP, 1, self.Iris,  structures.Action(constants.ACTION_FOLD)),
            (constants.PREFLOP, 1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)),
            (constants.PREFLOP, 1, self.Boa,   structures.Action(constants.ACTION_CALL, 50)),
            (constants.PREFLOP, 1, self.Coral, structures.Action(constants.ACTION_CHECK)),

            (constants.FLOP,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Coral, structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Goma,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Hilo,  structures.Action(constants.ACTION_CHECK)),
            (constants.FLOP,    1, self.Andy,  structures.Action(constants.ACTION_CHECK)),

            (constants.TURN,    1, self.Boa,   structures.Action(constants.ACTION_CHECK)),
            (constants.TURN,    1, self.Coral, structures.Action(constants.ACTION_BET, 100)),
            (constants.TURN,    1, self.Dino,  structures.Action(constants.ACTION_RAISE, 300)),
            (constants.TURN,    1, self.Epa,   structures.Action(constants.ACTION_RAISE, 600)),
            (constants.TURN,    1, self.Fomi,  structures.Action(constants.ACTION_CALL, 600)),
            (constants.TURN,    1, self.Goma,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    1, self.Hilo,  structures.Action(constants.ACTION_FOLD)),
            (constants.TURN,    1, self.Andy,  structures.Action(constants.ACTION_CALL, 100)), # all-in
            (constants.TURN,    2, self.Boa,   structures.Action(constants.ACTION_CALL, 400)), # all-in
            (constants.TURN,    2, self.Coral, structures.Action(constants.ACTION_CALL, 300)), # all-in
            (constants.TURN,    2, self.Dino,  structures.Action(constants.ACTION_CALL, 300)),

            (constants.RIVER,   1, self.Dino,  structures.Action(constants.ACTION_CHECK)),
            (constants.RIVER,   1, self.Epa,   structures.Action(constants.ACTION_CHECK)),
            (constants.RIVER,   1, self.Fomi,  structures.Action(constants.ACTION_CHECK)),

        )

        generator = engines.run_hand_cycle_listener(self.hand_cycle)

        with self.subTest('before actions'):
            self.assertIsNone(self.hand_cycle.betting_round)

        for player in (self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(next_player, player)

        for round_name, lap, player, action in round_and_laps_and_players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', round=round_name, lap=lap, player=player.name, action=action):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.hand_cycle.betting_round.lap_counts, lap)
                self.assertEqual(next_player, player)
            player.request_action(action)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)


if __name__ == '__main__':
    main()