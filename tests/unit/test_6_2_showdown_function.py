"""
Defines unit tests on functions related to placing blinds.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class BaseTestCase(TestCase):


    "Base class for test cases that require a shared setup."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 0),
            structures.Player('Boa', 0),
            structures.Player('Coral', 0),
            structures.Player('Dino', 0),
            structures.Player('Epa', 0),
            structures.Player('Fomi', 0),
            structures.Player('Goma', 0),
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


class TestShowdownFunctionWithoutSidePots(BaseTestCase):


    "Runs unit tests on showdown function without side pots."


    def test_main_pot_with_single_remaining_player(self):

        "Tests when there is a single remaining player."

        pot = 1000

        self.table.increase_central_pot(pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player != self.Andy:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (1000,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Coral.stack, 0)
            self.assertEqual(self.Dino.stack, 0)
            self.assertEqual(self.Epa.stack, 0)
            self.assertEqual(self.Fomi.stack, 0)
            self.assertEqual(self.Goma.stack, 0)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


    def test_main_pot_with_single_winner(self):

        "Tests when there is a single winner."

        pot = 1000
        pot_players = (self.Andy, self.Boa, self.Coral, self.Dino, self.Epa)

        winner_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))
        losers_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.TENS, constants.HEARTS),
        ))

        self.table.increase_central_pot(pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player == self.Andy:
                player.assign_hand(winner_hand)
            elif player in pot_players:
                player.assign_hand(losers_hand)
            else:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (1000,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Coral.stack, 0)
            self.assertEqual(self.Dino.stack, 0)
            self.assertEqual(self.Epa.stack, 0)
            self.assertEqual(self.Fomi.stack, 0)
            self.assertEqual(self.Goma.stack, 0)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


    def test_even_main_pot_with_ties(self):

        "Tests when there players tie and the pot is even."

        pot = 1000
        pot_players = (self.Andy, self.Boa, self.Coral, self.Dino, self.Epa)
        tie_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))

        self.table.increase_central_pot(pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player in pot_players:
                player.assign_hand(tie_hand)
            else:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (1000,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Boa.stack, 200)
            self.assertEqual(self.Coral.stack, 200)
            self.assertEqual(self.Dino.stack, 200)
            self.assertEqual(self.Epa.stack, 200)
            self.assertEqual(self.Andy.stack, 200)
            self.assertEqual(self.Fomi.stack, 0)
            self.assertEqual(self.Goma.stack, 0)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


    def test_uneven_main_pot_with_ties_and_single_extra_chips(self):

        "Tests when there players tie and the pot is uneven with a single extra chip."

        pot = 1001
        pot_players = (self.Andy, self.Boa, self.Coral, self.Dino, self.Epa)
        tie_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))

        self.table.increase_central_pot(pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player in pot_players:
                player.assign_hand(tie_hand)
            else:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (1001,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Boa.stack, 201)
            self.assertEqual(self.Coral.stack, 200)
            self.assertEqual(self.Dino.stack, 200)
            self.assertEqual(self.Epa.stack, 200)
            self.assertEqual(self.Andy.stack, 200)
            self.assertEqual(self.Fomi.stack, 0)
            self.assertEqual(self.Goma.stack, 0)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


    def test_uneven_main_pot_with_ties_and_multiple_extra_chips(self):

        "Tests when there players tie and the pot is uneven with multiple extra chips."

        pot = 1003
        pot_players = (self.Andy, self.Boa, self.Coral, self.Dino, self.Epa)
        tie_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))

        self.table.increase_central_pot(pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player in pot_players:
                player.assign_hand(tie_hand)
            else:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (1003,))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Boa.stack, 201)
            self.assertEqual(self.Coral.stack, 201)
            self.assertEqual(self.Dino.stack, 201)
            self.assertEqual(self.Epa.stack, 200)
            self.assertEqual(self.Andy.stack, 200)
            self.assertEqual(self.Fomi.stack, 0)
            self.assertEqual(self.Goma.stack, 0)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


class TestShowdownFunctionWithSidePots(BaseTestCase):


    "Runs unit tests on showdown function with side pots."


    def test_side_pots_with_single_winner(self):

        "Tests when there is a single winner."

        winner_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))
        losers_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.TENS, constants.HEARTS),
        ))

        main_pot = 800
        main_pot_players = (self.Boa, self.Coral, self.Dino)

        side_pot = 300
        side_pot_players = (self.Andy, self.Epa, self.Fomi, self.Goma)

        self.table.increase_central_pot(main_pot)
        self.table.add_side_pot()
        self.table.increase_central_pot(side_pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:

            if player == self.Andy:
                player.assign_hand(winner_hand)
            else:
                player.assign_hand(losers_hand)

            if player in side_pot_players:
                player.increase_pot_index()
            elif player not in main_pot_players:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (800, 300))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Andy.stack, 1100)
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Coral.stack, 0)
            self.assertEqual(self.Dino.stack, 0)
            self.assertEqual(self.Epa.stack, 0)
            self.assertEqual(self.Fomi.stack, 0)
            self.assertEqual(self.Goma.stack, 0)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


    def test_even_side_pots_with_ties(self):

        "Tests when there players tie and the pot is split into even side pots."

        main_pot = 800
        main_pot_players = (self.Andy, self.Boa, self.Coral, self.Dino)
        main_pot_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))

        side_pot = 300
        side_pot_players = (self.Epa, self.Fomi, self.Goma)
        side_pot_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.TENS, constants.HEARTS),
        ))

        self.table.increase_central_pot(main_pot)
        self.table.add_side_pot()
        self.table.increase_central_pot(side_pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player in main_pot_players:
                player.assign_hand(main_pot_hand)
            elif player in side_pot_players:
                player.increase_pot_index()
                player.assign_hand(side_pot_hand)
            else:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (800, 300))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Boa.stack, 200)
            self.assertEqual(self.Coral.stack, 200)
            self.assertEqual(self.Dino.stack, 200)
            self.assertEqual(self.Andy.stack, 200)
            self.assertEqual(self.Epa.stack, 100)
            self.assertEqual(self.Fomi.stack, 100)
            self.assertEqual(self.Goma.stack, 100)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


    def test_uneven_side_pots_with_ties_and_single_extra_chips(self):

        "Tests when there players tie and the pot is split into uneven side pots with a single extra chip."

        main_pot = 801
        main_pot_players = (self.Andy, self.Boa, self.Coral, self.Dino)
        main_pot_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))

        side_pot = 301
        side_pot_players = (self.Epa, self.Fomi, self.Goma)
        side_pot_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.TENS, constants.HEARTS),
        ))

        self.table.increase_central_pot(main_pot)
        self.table.add_side_pot()
        self.table.increase_central_pot(side_pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player in main_pot_players:
                player.assign_hand(main_pot_hand)
            elif player in side_pot_players:
                player.increase_pot_index()
                player.assign_hand(side_pot_hand)
            else:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (801, 301))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Boa.stack, 201)
            self.assertEqual(self.Coral.stack, 200)
            self.assertEqual(self.Dino.stack, 200)
            self.assertEqual(self.Andy.stack, 200)
            self.assertEqual(self.Epa.stack, 101)
            self.assertEqual(self.Fomi.stack, 100)
            self.assertEqual(self.Goma.stack, 100)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


    def test_uneven_side_pots_with_ties_and_multiple_extra_chips(self):

        "Tests when there players tie and the pot is split into uneven side pots with multiple extra chips."

        main_pot = 802
        main_pot_players = (self.Andy, self.Boa, self.Coral, self.Dino)
        main_pot_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.SPADES),
        ))

        side_pot = 302
        side_pot_players = (self.Epa, self.Fomi, self.Goma)
        side_pot_hand = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.TENS, constants.HEARTS),
        ))

        self.table.increase_central_pot(main_pot)
        self.table.add_side_pot()
        self.table.increase_central_pot(side_pot)
        self.table.set_button_player(self.Andy)

        for player in self.setup_players:
            if player in main_pot_players:
                player.assign_hand(main_pot_hand)
            elif player in side_pot_players:
                player.increase_pot_index()
                player.assign_hand(side_pot_hand)
            else:
                player.mark_is_folded()

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (802, 302))
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)

        engines.showdown(self.table)

        with self.subTest('before showdown'):
            self.assertTupleEqual(self.table.split_central_pot, (0,))
            self.assertEqual(self.Boa.stack, 201)
            self.assertEqual(self.Coral.stack, 201)
            self.assertEqual(self.Dino.stack, 200)
            self.assertEqual(self.Andy.stack, 200)
            self.assertEqual(self.Epa.stack, 101)
            self.assertEqual(self.Fomi.stack, 101)
            self.assertEqual(self.Goma.stack, 100)
            self.assertEqual(self.Hilo.stack, 0)
            self.assertEqual(self.Iris.stack, 0)


if __name__ == '__main__':
    main()