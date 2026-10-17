"""
Defines unit tests on functions related to placing blinds.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class TestPostFlopFunction(TestCase):


    "Runs unit tests on post_flop function."


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
        self.hand_cycle.deal_cards_to_players(2)


    def test_flop(self):

        "Tests flop."

        self.table.set_button_player(self.Andy)

        players_and_actions = [
            (self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        ]

        generator = engines.post_flop(self.hand_cycle, constants.FLOP)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertEqual(len(self.table.common_cards), 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.FLOP)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(len(self.table.common_cards), 3)
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


    def test_turn(self):

        "Tests turn."

        self.hand_cycle.deal_common_cards(3)
        self.table.set_button_player(self.Andy)

        players_and_actions = [
            (self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        ]

        generator = engines.post_flop(self.hand_cycle, constants.TURN)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertEqual(len(self.table.common_cards), 3)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.TURN)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(len(self.table.common_cards), 4)
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


    def test_river(self):

        "Tests river."

        self.hand_cycle.deal_common_cards(4)
        self.table.set_button_player(self.Andy)

        players_and_actions = [
            (self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        ]

        generator = engines.post_flop(self.hand_cycle, constants.RIVER)

        with self.subTest('before pre-flop'):
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertEqual(len(self.table.common_cards), 4)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        for player, action in players_and_actions:
            next_player = next(generator)
            with self.subTest('action phase', player=player.name):
                self.assertIsNotNone(self.hand_cycle.betting_round)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.RIVER)
                self.assertFalse(self.hand_cycle.betting_round.is_completed)
                self.assertEqual(len(self.table.common_cards), 5)
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