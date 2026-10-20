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


    def run_test_without_blinds(
        self,
        *,
        expected_starting_player: structures.Player,
        players_and_actions: tuple[
            tuple[structures.Player, structures.Action],
            ...
        ],
    ):

        "Runs the shared validations for the tests without blinds."

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before generator start-up'):
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, self.setup_players[0])
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        with self.subTest('after listener start-up'):
            next_player = next(generator)
            self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        for i, (player, action) in enumerate(players_and_actions, 1):
            with self.subTest('action phase', player=player.name):
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.table.starting_player, expected_starting_player)
                self.assertGreaterEqual(self.table.bet_level, 0)
                self.assertGreaterEqual(self.table.full_bet_level, 0)
                self.assertEqual(player, next_player)
                self.assertEqual(len(player.cards), 2)
                player.request_action(action)
                if i < len(players_and_actions):
                    next_player = next(generator)

        with self.subTest('before listener termination'):
            self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertGreaterEqual(self.table.bet_level, 0)
            self.assertGreaterEqual(self.table.full_bet_level, 0)
            self.assertEqual(players_and_actions[-1][0], next_player)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        with self.subTest('after listener termination'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)


    def run_test_with_blinds(
        self,
        *,
        big_blind: int|None = None,
        expected_starting_player: structures.Player,
        players_and_actions: tuple[
            tuple[structures.Player, structures.Action],
            ...
        ],
        extra_blind_candidates: tuple[structures.Player, ...] | None = None,
    ):

        "Runs the shared validations for the tests with blinds."

        generator = engines.pre_flop(self.hand_cycle)

        with self.subTest('before generator start-up'):
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, self.setup_players[0])
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        with self.subTest('after listener start-up'):
            next_player = next(generator)
            self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
            self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(self.table.bet_level, big_blind)
            self.assertEqual(self.table.full_bet_level, big_blind)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        for i, player in enumerate(extra_blind_candidates, 1):
            with self.subTest('extra blinds phase', player=player.name):
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.table.starting_player, expected_starting_player)
                self.assertEqual(self.table.bet_level, big_blind)
                self.assertEqual(self.table.full_bet_level, big_blind)
                self.assertEqual(next_player, player)
                self.assertEqual(len(player.cards), 0)
                if i < len(extra_blind_candidates):
                    next_player = next(generator)

        with self.subTest('before transition to action phase'):
            self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
            self.assertTrue(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(self.table.bet_level, big_blind)
            self.assertEqual(self.table.full_bet_level, big_blind)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        with self.subTest('after transition to action phase'):
            next_player = next(generator)
            self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(self.table.bet_level, big_blind)
            self.assertEqual(self.table.full_bet_level, big_blind)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        for i, (player, action) in enumerate(players_and_actions, 1):
            with self.subTest('action phase', player=player.name):
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
                self.assertEqual(self.table.starting_player, expected_starting_player)
                self.assertGreaterEqual(self.table.bet_level, big_blind)
                self.assertGreaterEqual(self.table.full_bet_level, big_blind)
                self.assertEqual(player, next_player)
                self.assertEqual(len(player.cards), 2)
                player.request_action(action)
                if i < len(players_and_actions):
                    next_player = next(generator)

        with self.subTest('before listener termination'):
            self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertGreaterEqual(self.table.bet_level, big_blind)
            self.assertGreaterEqual(self.table.full_bet_level, big_blind)
            self.assertEqual(players_and_actions[-1][0], next_player)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        with self.subTest('after listener termination'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertFalse(self.hand_cycle.in_extra_big_blinds_phase)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)


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

        self.run_test_without_blinds(
            expected_starting_player = self.Boa,
            players_and_actions = players_and_actions,
        )


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

        self.run_test_with_blinds(
            big_blind = 100,
            expected_starting_player = self.Coral,
            players_and_actions = players_and_actions,
            extra_blind_candidates = (self.Coral, self.Dino, self.Epa, self.Fomi, self.Andy),
        )


    def test_big_blind_some_extra_blinds(self):

        "Tests when big blind is placed and some of the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)

        for player in (self.Coral, self.Dino, self.Epa):
            player.mark_is_extra_blind()

        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test_with_blinds(
            big_blind = 100,
            expected_starting_player = self.Coral,
            players_and_actions = players_and_actions,
            extra_blind_candidates = (self.Coral, self.Dino, self.Epa, self.Fomi, self.Andy),
        )


    def test_big_blind_full_extra_blinds(self):

        "Tests when big blind is placed and all the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)

        for player in (self.Coral, self.Dino, self.Epa, self.Fomi, self.Andy):
            player.mark_is_extra_blind()

        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CHECK)),
            (self.Andy, structures.Action(constants.ACTION_CHECK)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test_with_blinds(
            big_blind = 100,
            expected_starting_player = self.Coral,
            players_and_actions = players_and_actions,
            extra_blind_candidates = (self.Coral, self.Dino, self.Epa, self.Fomi, self.Andy),
        )


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

        self.run_test_with_blinds(
            big_blind = 100,
            expected_starting_player = self.Dino,
            players_and_actions = players_and_actions,
            extra_blind_candidates = (self.Dino, self.Epa, self.Fomi, self.Andy),
        )


    def test_small_and_big_blinds_some_extra_blinds(self):

        "Tests when small and big blind are placed and some of the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        for player in (self.Dino, self.Epa):
            player.mark_is_extra_blind()

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test_with_blinds(
            big_blind = 100,
            expected_starting_player = self.Dino,
            players_and_actions = players_and_actions,
            extra_blind_candidates = (self.Dino, self.Epa, self.Fomi, self.Andy),
        )


    def test_small_and_big_blinds_full_extra_blinds(self):

        "Tests when small and big blind are placed and all the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        for player in (self.Dino, self.Epa, self.Fomi, self.Andy):
            player.mark_is_extra_blind()

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CHECK)),
            (self.Andy, structures.Action(constants.ACTION_CHECK)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test_with_blinds(
            big_blind = 100,
            expected_starting_player = self.Dino,
            players_and_actions = players_and_actions,
            extra_blind_candidates = (self.Dino, self.Epa, self.Fomi, self.Andy),
        )


if __name__ == '__main__':
    main()