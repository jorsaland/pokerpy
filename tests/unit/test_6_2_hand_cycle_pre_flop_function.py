"""
Defines unit tests on functions related to placing blinds.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, states, structures


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

        self.cards_by_player = {
            self.Andy:  (structures.Card(constants.ACES, constants.SPADES),   (structures.Card(constants.ACES, constants.HEARTS))),
            self.Boa:   (structures.Card(constants.KINGS, constants.SPADES),  (structures.Card(constants.KINGS, constants.HEARTS))),
            self.Coral: (structures.Card(constants.QUEENS, constants.SPADES), (structures.Card(constants.QUEENS, constants.HEARTS))),
            self.Dino:  (structures.Card(constants.JACKS, constants.SPADES),  (structures.Card(constants.JACKS, constants.HEARTS))),
            self.Epa:   (structures.Card(constants.TENS, constants.SPADES),   (structures.Card(constants.TENS, constants.HEARTS))),
            self.Fomi:  (structures.Card(constants.NINES, constants.SPADES),  (structures.Card(constants.NINES, constants.HEARTS))),
        }

        self.hand_cycle = engines.HandCycle('test', self.table, open_fold_allowed=True)


    def run_test(
        self,
        *,
        expected_starting_player: structures.Player,
        optional_blind_choices: list[tuple[structures.Player, bool]],
        players_and_actions: list[tuple[structures.Player, structures.Action]],
    ):

        "Runs the shared validations for the tests without blinds."

        generator = engines.pre_flop(self.hand_cycle)

        applied_deals: list[tuple[structures.Player, tuple[structures.Card, ...]]] = []
        applied_small_blinds: set[structures.Player] = set()
        applied_big_blinds: set[structures.Player] = set()
        def assert_applied_deals():
            for player, cards in applied_deals:
                self.assertTupleEqual(player.cards, cards)
            for player in applied_small_blinds:
                self.assertGreaterEqual(player.bet_level, self.table.small_blind or 0)
            for player in applied_big_blinds:
                self.assertGreaterEqual(player.bet_level, self.table.big_blind or 0)

        with self.subTest('before start-up'):
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertEqual(self.table.starting_player, self.setup_players[0])
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            for player in self.setup_players:
                self.assertTupleEqual(player.cards, ())

        for player, chose_placing_blind in optional_blind_choices:
            with self.subTest('extra blinds phase', player=player.name):
                await_state = next(generator)
                if player == self.table.small_blind_player:
                    applied_small_blinds.add(player)
                if player == self.table.big_blind_player:
                    applied_big_blinds.add(player)
                assert_applied_deals()
                self.assertIsInstance(await_state, states.PlayerBlindAwait)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertEqual(self.table.starting_player, expected_starting_player)
                self.assertEqual(self.table.bet_level, self.table.big_blind or 0)
                self.assertEqual(self.table.full_bet_level, self.table.big_blind or 0)
            if chose_placing_blind:
                await_state.place_blind()
                applied_big_blinds.add(player)

        for player, cards in self.cards_by_player.items():
            with self.subTest('dealing phase', player=player.name):
                await_state = next(generator)
                if player == self.table.small_blind_player:
                    applied_small_blinds.add(player)
                if player == self.table.big_blind_player:
                    applied_big_blinds.add(player)
                assert_applied_deals()
                self.assertIsInstance(await_state, states.PlayerDealingAwait)
                self.assertEqual(await_state.player, player)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertEqual(self.table.starting_player, expected_starting_player)
                self.assertEqual(self.table.bet_level, self.table.big_blind or 0)
                self.assertEqual(self.table.full_bet_level, self.table.big_blind or 0)
            await_state.deal_cards(cards)
            applied_deals.append((player, cards))

        for player, action in players_and_actions:
            with self.subTest('action phase', player=player.name):
                await_state = next(generator)
                assert_applied_deals()
                self.assertIsInstance(await_state, states.PlayerActionAwait)
                self.assertEqual(await_state.player, player)
                self.assertEqual(self.hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertEqual(self.table.starting_player, expected_starting_player)
                self.assertGreaterEqual(self.table.bet_level, 0)
                self.assertGreaterEqual(self.table.full_bet_level, 0)
            await_state.request_action(action)

        with self.subTest('termination'):
            with self.assertRaises(StopIteration):
                next(generator)
            applied_small_blinds.clear()
            applied_big_blinds.clear()
            assert_applied_deals()
            self.assertIsNone(self.hand_cycle.betting_round)
            self.assertEqual(self.table.starting_player, expected_starting_player)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)


    def test_no_blinds(self):

        "Tests when no blinds are placed."

        self.table.set_button_player(self.Andy)

        optional_blind_choices = []

        players_and_actions = [
            (self.Boa, structures.Action(constants.ACTION_BET, 100)),
            (self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
        ]

        self.run_test(
            expected_starting_player = self.Boa,
            optional_blind_choices = optional_blind_choices,
            players_and_actions = players_and_actions,
        )


    def test_big_blind_no_extra_blinds(self):

        "Tests when big blind is placed and none of the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)

        optional_blind_choices = [
            (self.Coral, False),
            (self.Dino, False),
            (self.Epa, False),
            (self.Fomi, False),
            (self.Andy, False),
        ]

        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CALL, 100)),
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test(
            expected_starting_player = self.Coral,
            optional_blind_choices = optional_blind_choices,
            players_and_actions = players_and_actions,
        )


    def test_big_blind_some_extra_blinds(self):

        "Tests when big blind is placed and some of the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)

        optional_blind_choices = [
            (self.Coral, True),
            (self.Dino, True),
            (self.Epa, True),
            (self.Fomi, False),
            (self.Andy, False),
        ]

        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test(
            expected_starting_player = self.Coral,
            optional_blind_choices = optional_blind_choices,
            players_and_actions = players_and_actions,
        )


    def test_big_blind_full_extra_blinds(self):

        "Tests when big blind is placed and all the other players place extra big blinds."

        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_big_blind_player(self.Boa)

        optional_blind_choices = [
            (self.Coral, True),
            (self.Dino, True),
            (self.Epa, True),
            (self.Fomi, True),
            (self.Andy, True),
        ]

        players_and_actions = [
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CHECK)),
            (self.Andy, structures.Action(constants.ACTION_CHECK)),
            (self.Boa, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test(
            expected_starting_player = self.Coral,
            optional_blind_choices = optional_blind_choices,
            players_and_actions = players_and_actions,
        )


    def test_small_and_big_blinds_no_extra_blinds(self):

        "Tests when small and big blind are placed and none of the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        optional_blind_choices = [
            (self.Dino, False),
            (self.Epa, False),
            (self.Fomi, False),
            (self.Andy, False),
        ]

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CALL, 100)),
            (self.Epa, structures.Action(constants.ACTION_CALL, 100)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test(
            expected_starting_player = self.Dino,
            optional_blind_choices = optional_blind_choices,
            players_and_actions = players_and_actions,
        )


    def test_small_and_big_blinds_some_extra_blinds(self):

        "Tests when small and big blind are placed and some of the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        optional_blind_choices = [
            (self.Dino, True),
            (self.Epa, True),
            (self.Fomi, False),
            (self.Andy, False),
        ]

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CALL, 100)),
            (self.Andy, structures.Action(constants.ACTION_CALL, 100)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test(
            expected_starting_player = self.Dino,
            optional_blind_choices = optional_blind_choices,
            players_and_actions = players_and_actions,
        )


    def test_small_and_big_blinds_full_extra_blinds(self):

        "Tests when small and big blind are placed and all the other players place extra big blinds."

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        optional_blind_choices = [
            (self.Dino, True),
            (self.Epa, True),
            (self.Fomi, True),
            (self.Andy, True),
        ]

        players_and_actions = [
            (self.Dino, structures.Action(constants.ACTION_CHECK)),
            (self.Epa, structures.Action(constants.ACTION_CHECK)),
            (self.Fomi, structures.Action(constants.ACTION_CHECK)),
            (self.Andy, structures.Action(constants.ACTION_CHECK)),
            (self.Boa, structures.Action(constants.ACTION_CALL, 50)),
            (self.Coral, structures.Action(constants.ACTION_CHECK)),
        ]

        self.run_test(
            expected_starting_player = self.Dino,
            optional_blind_choices = optional_blind_choices,
            players_and_actions = players_and_actions,
        )


if __name__ == '__main__':
    main()