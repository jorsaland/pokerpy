"""
Defines unit tests on functions related to placing blinds.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class TestPreFlopFunction(TestCase):


    "Runs unit tests on pre_flop function."


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

        self.hand_cycle = engines.HandCycle(
            'test',
            self.table,
            raise_invalid_actions = True,
            open_fold_allowed = True,
        )


    def test_no_blinds(self):

        "Tests when no blinds are placed."

        self.table.set_button_player(self.Andy)

        players_and_actions = [
            (self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        ]

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 2)
            player.request_action(action)

        with self.subTest('before closing', player=player.name):
            self.assertIsNotNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        assert (betting_round := self.hand_cycle.betting_round)
        with self.subTest('after closing'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (600,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 0)


    def test_big_blind_no_extra_blinds(self):

        "Tests when big blind is placed and none of the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)


        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for player in (self.Coral, self.Dino, self.Epa, self.Fomi, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds phase', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 0)

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 2)
            player.request_action(action)

        with self.subTest('before closing', player=player.name):
            self.assertIsNotNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        assert (betting_round := self.hand_cycle.betting_round)
        with self.subTest('after closing'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (600,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 0)


    def test_big_blind_some_extra_blinds(self):

        "Tests when big blind is placed and some of the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)


        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for player in (self.Coral, self.Dino, self.Epa, self.Fomi, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds phase', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 0)
            if player in (self.Coral, self.Dino, self.Epa):
                player.mark_is_extra_blind()

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 2)
            player.request_action(action)

        with self.subTest('before closing', player=player.name):
            self.assertIsNotNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        assert (betting_round := self.hand_cycle.betting_round)
        with self.subTest('after closing'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (600,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 0)


    def test_big_blind_full_extra_blinds(self):

        "Tests when big blind is placed and all the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)

        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CHECK)),
            (self.Andy, structures.Action(constants.ACTION_CHECK)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for player in (self.Coral, self.Dino, self.Epa, self.Fomi, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds phase', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 0)
            player.mark_is_extra_blind()

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 2)
            player.request_action(action)

        with self.subTest('before closing', player=player.name):
            self.assertIsNotNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        assert (betting_round := self.hand_cycle.betting_round)
        with self.subTest('after closing'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (600,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 0)


    def test_small_and_big_blinds_no_extra_blinds(self):

        "Tests when small and big blind are placed and none of the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for player in (self.Dino, self.Epa, self.Fomi, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds phase', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 0)

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 2)
            player.request_action(action)

        with self.subTest('before closing', player=player.name):
            self.assertIsNotNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        assert (betting_round := self.hand_cycle.betting_round)
        with self.subTest('after closing'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (600,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 0)


    def test_small_and_big_blinds_some_extra_blinds(self):

        "Tests when small and big blind are placed and some of the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for player in (self.Dino, self.Epa, self.Fomi, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds phase', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 0)
            if player in (self.Dino, self.Epa):
                player.mark_is_extra_blind()

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 2)
            player.request_action(action)

        with self.subTest('before closing', player=player.name):
            self.assertIsNotNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        assert (betting_round := self.hand_cycle.betting_round)
        with self.subTest('after closing'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (600,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 0)


    def test_small_and_big_blinds_full_extra_blinds(self):

        "Tests when small and big blind are placed and all the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CHECK)),
            (self.Andy, structures.Action(constants.ACTION_CHECK)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for player in (self.Dino, self.Epa, self.Fomi, self.Andy):
            next_player = next(generator)
            with self.subTest('extra blinds phase', player=player.name):
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 0)
            player.mark_is_extra_blind()

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 2)
            player.request_action(action)

        with self.subTest('before closing', player=player.name):
            self.assertIsNotNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        assert (betting_round := self.hand_cycle.betting_round)
        with self.subTest('after closing'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTupleEqual(self.table.split_central_pot, (600,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 0)


if __name__ == '__main__':
    main()