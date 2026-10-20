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


    def run_test(
        self,
        *,
        round_name: str,
        expected_starting_player: structures.Player,
        players_and_actions: tuple[
            tuple[structures.Player, structures.Action],
            ...
        ],
    ):

        "Runs the shared validations for the tests without blinds."

        if round_name == constants.FLOP:
            cards_count_before = 0
            cards_count_after = 3
        elif round_name == constants.TURN:
            cards_count_before = 3
            cards_count_after = 4
        elif round_name == constants.RIVER:
            cards_count_before = 4
            cards_count_after = 5
        else:
            raise AssertionError

        generator = engines.post_flop(self.hand_cycle, round_name)

        with self.subTest('before generator start-up'):
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertEqual(self.table.starting_player, self.setup_players[0])
            self.assertEqual(len(self.table.common_cards), cards_count_before)

        with self.subTest('after listener start-up'):
            next_player = next(generator)
            self.assertEqual(self.hand_cycle.betting_round.name, round_name)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(len(self.table.common_cards), cards_count_after)

        for i, (player, action) in enumerate(players_and_actions, 1):
            with self.subTest('action phase', player=player.name):
                self.assertEqual(self.hand_cycle.betting_round.name, round_name)
                self.assertEqual(self.table.starting_player, expected_starting_player)
                self.assertEqual(len(self.table.common_cards), cards_count_after)
                self.assertEqual(player, next_player)
                player.request_action(action)
                if i < len(players_and_actions):
                    next_player = next(generator)

        with self.subTest('before listener termination'):
            self.assertEqual(self.hand_cycle.betting_round.name, round_name)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(len(self.table.common_cards), cards_count_after)
            self.assertEqual(players_and_actions[-1][0], next_player)

        with self.subTest('after listener termination'):
            with self.assertRaises(StopIteration):
                next(generator)
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(len(self.table.common_cards), cards_count_after)


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

        self.run_test(
            round_name = constants.FLOP,
            players_and_actions = players_and_actions,
            expected_starting_player = self.Boa,
        )


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

        self.run_test(
            round_name = constants.TURN,
            players_and_actions = players_and_actions,
            expected_starting_player = self.Boa,
        )


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

        self.run_test(
            round_name = constants.RIVER,
            players_and_actions = players_and_actions,
            expected_starting_player = self.Boa,
        )


if __name__ == '__main__':
    main()