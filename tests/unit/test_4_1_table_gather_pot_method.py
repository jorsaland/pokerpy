"""
Defines unit tests on Table method gather_pot.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import structures


class TestGatherPotMethodWithNoStartingPot(TestCase):


    "Runs unit tests on Table method gather_pot where the starting pot is zero."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 500),
            structures.Player('Epa', 500),
            structures.Player('Fomi', 500),
            structures.Player('Goma', 200),
            structures.Player('Hilo', 200),
            structures.Player('Iris', 200),
        ]

        self.table = structures.Table(self.setup_players, min_bet=100)
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris = self.setup_players

        for player in (self.Coral, self.Fomi, self.Iris):
            player.mark_is_folded()


    def test_no_bettor_players_with_no_starting_pot(self):

        "Tests pot gathering when no player places money."

        # Coral starts folded

        # Fomi starts folded

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertEqual(self.Epa.pot_index, 0)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertEqual(self.Epa.pot_index, 0)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))


    def test_one_bettor_with_no_starting_pot(self):

        "Tests pot gathering when only one player places money and the others fold."

        self.Andy.decrease_stack(100)
        self.Andy.increase_bet_level(100)

        self.Boa.mark_is_folded()

        # Coral starts folded

        self.Dino.mark_is_folded()

        self.Epa.mark_is_folded()

        # Fomi starts folded

        self.Goma.mark_is_folded()

        self.Hilo.mark_is_folded()

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (100,))


    def test_one_all_in_bettor_with_no_starting_pot(self):

        "Tests pot gathering when only one player goes all-in and the others fold."

        self.Andy.decrease_stack(1000) # all-in
        self.Andy.increase_bet_level(1000)

        self.Boa.mark_is_folded()

        # Coral starts folded

        self.Dino.mark_is_folded()

        self.Epa.mark_is_folded()

        # Fomi starts folded

        self.Goma.mark_is_folded()

        self.Hilo.mark_is_folded()

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1000,))


    def test_equal_bettors_with_no_starting_pot(self):

        "Tests pot gathering when multiple players place the same amount of money."

        self.Andy.decrease_stack(200)
        self.Andy.increase_bet_level(200)

        self.Boa.decrease_stack(200)
        self.Boa.increase_bet_level(200)

        # Coral starts folded

        self.Dino.mark_is_folded()

        self.Epa.mark_is_folded()

        # Fomi starts folded

        self.Goma.mark_is_folded()

        self.Hilo.mark_is_folded()

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 200)
            self.assertEqual(self.Boa.bet_level, 200)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (400,))


    def test_equal_some_all_in_bettors_with_no_starting_pot(self):

        "Tests pot gathering when multiple players place the same amount of money, some going all-in."

        self.Andy.decrease_stack(200)
        self.Andy.increase_bet_level(200)

        self.Boa.decrease_stack(200)
        self.Boa.increase_bet_level(200)

        # Coral starts folded

        self.Dino.decrease_stack(200)
        self.Dino.increase_bet_level(200)

        self.Epa.decrease_stack(200)
        self.Epa.increase_bet_level(200)

        # Fomi starts folded

        self.Goma.decrease_stack(200) # all-in
        self.Goma.increase_bet_level(200)

        self.Hilo.decrease_stack(200) # all-in
        self.Hilo.increase_bet_level(200)

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 200)
            self.assertEqual(self.Boa.bet_level, 200)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 200)
            self.assertEqual(self.Epa.bet_level, 200)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 200)
            self.assertEqual(self.Hilo.bet_level, 200)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertEqual(self.Epa.pot_index, 0)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 0))


    def test_unequal_bettors_with_no_starting_pot(self):

        "Tests pot gathering when multiple players place different amounts of money."

        self.Andy.decrease_stack(800)
        self.Andy.increase_bet_level(800)

        self.Boa.decrease_stack(800)
        self.Boa.increase_bet_level(800)

        # Coral starts folded

        self.Dino.decrease_stack(500) # all-in
        self.Dino.increase_bet_level(500)

        self.Epa.decrease_stack(500) # all-in
        self.Epa.increase_bet_level(500)

        # Fomi starts folded

        self.Goma.decrease_stack(200) # all-in
        self.Goma.increase_bet_level(200)

        self.Hilo.decrease_stack(200) # all-in
        self.Hilo.increase_bet_level(200)

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 800)
            self.assertEqual(self.Boa.bet_level, 800)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 500)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 200)
            self.assertEqual(self.Hilo.bet_level, 200)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertEqual(self.Epa.pot_index, 0)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 2)
            self.assertEqual(self.Boa.pot_index, 2)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1200, 600))


    def test_unequal_all_in_bettors_with_no_starting_pot(self):

        """
        Tests pot gathering when all remaining players go all-in by placing different amounts of
        money.
        """

        self.Andy.decrease_stack(1000) # all-in
        self.Andy.increase_bet_level(1000)

        self.Boa.decrease_stack(1000) # all-in
        self.Boa.increase_bet_level(1000)

        # Coral starts folded

        self.Dino.decrease_stack(500) # all-in
        self.Dino.increase_bet_level(500)

        self.Epa.decrease_stack(500) # all-in
        self.Epa.increase_bet_level(500)

        # Fomi starts folded

        self.Goma.decrease_stack(200) # all-in
        self.Goma.increase_bet_level(200)

        self.Hilo.decrease_stack(200) # all-in
        self.Hilo.increase_bet_level(200)

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 1000)
            self.assertEqual(self.Boa.bet_level, 1000)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 500)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 200)
            self.assertEqual(self.Hilo.bet_level, 200)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertEqual(self.Epa.pot_index, 0)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 2)
            self.assertEqual(self.Boa.pot_index, 2)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1200, 1000))


    def test_unequal_bettors_one_level_folded_with_no_starting_pot(self):

        """
        Tests pot gathering when multiple players place different amounts of money and one of the
        bet levels only contains folded players.
        """

        self.Andy.decrease_stack(800)
        self.Andy.increase_bet_level(800)

        self.Boa.decrease_stack(800)
        self.Boa.increase_bet_level(800)

        # Coral starts folded

        self.Dino.decrease_stack(400)
        self.Dino.increase_bet_level(400)
        self.Dino.mark_is_folded()

        self.Epa.decrease_stack(400)
        self.Epa.increase_bet_level(400)
        self.Epa.mark_is_folded()

        # Fomi starts folded

        self.Goma.decrease_stack(200) # all-in
        self.Goma.increase_bet_level(200)

        self.Hilo.decrease_stack(200) # all-in
        self.Hilo.increase_bet_level(200)

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 800)
            self.assertEqual(self.Boa.bet_level, 800)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 200)
            self.assertEqual(self.Hilo.bet_level, 200)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1600))


    def test_unequal_all_in_bettors_one_level_folded_with_no_starting_pot(self):

        """
        Tests pot gathering when all remaining players go all-in by placing different amounts of
        money and one of the bet levels only contains folded players.
        """

        self.Andy.decrease_stack(1000)
        self.Andy.increase_bet_level(1000)

        self.Boa.decrease_stack(1000)
        self.Boa.increase_bet_level(1000)

        # Coral starts folded

        self.Dino.decrease_stack(400)
        self.Dino.increase_bet_level(400)
        self.Dino.mark_is_folded()

        self.Epa.decrease_stack(400)
        self.Epa.increase_bet_level(400)
        self.Epa.mark_is_folded()

        # Fomi starts folded

        self.Goma.decrease_stack(200) # all-in
        self.Goma.increase_bet_level(200)

        self.Hilo.decrease_stack(200) # all-in
        self.Hilo.increase_bet_level(200)

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 1000)
            self.assertEqual(self.Boa.bet_level, 1000)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 200)
            self.assertEqual(self.Hilo.bet_level, 200)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 2000))


    def test_unequal_bettors_multiple_level_folded_with_no_starting_pot(self):

        """
        Tests pot gathering when multiple players place different amounts of money and one of the
        bet levels only contains folded players.
        """

        self.Andy.decrease_stack(800)
        self.Andy.increase_bet_level(800)

        self.Boa.decrease_stack(800)
        self.Boa.increase_bet_level(800)

        # Coral starts folded

        self.Dino.decrease_stack(400)
        self.Dino.increase_bet_level(400)
        self.Dino.mark_is_folded()

        self.Epa.decrease_stack(400)
        self.Epa.increase_bet_level(400)
        self.Epa.mark_is_folded()

        # Fomi starts folded

        self.Goma.decrease_stack(100)
        self.Goma.increase_bet_level(100)
        self.Goma.mark_is_folded()

        self.Hilo.decrease_stack(100)
        self.Hilo.increase_bet_level(100)
        self.Hilo.mark_is_folded()

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 800)
            self.assertEqual(self.Boa.bet_level, 800)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 100)
            self.assertEqual(self.Hilo.bet_level, 100)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (2600,))


    def test_unequal_all_in_bettors_multiple_level_folded_with_no_starting_pot(self):

        """
        Tests pot gathering when all remaining players place different amounts of money and one of
        the bet levels only contains folded players.
        """

        self.Andy.decrease_stack(1000) # all-in
        self.Andy.increase_bet_level(1000)

        self.Boa.decrease_stack(1000) # all-in
        self.Boa.increase_bet_level(1000)

        # Coral starts folded

        self.Dino.decrease_stack(400)
        self.Dino.increase_bet_level(400)
        self.Dino.mark_is_folded()

        self.Epa.decrease_stack(400)
        self.Epa.increase_bet_level(400)
        self.Epa.mark_is_folded()

        # Fomi starts folded

        self.Goma.decrease_stack(100)
        self.Goma.increase_bet_level(100)
        self.Goma.mark_is_folded()

        self.Hilo.decrease_stack(100)
        self.Hilo.increase_bet_level(100)
        self.Hilo.mark_is_folded()

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 1000)
            self.assertEqual(self.Boa.bet_level, 1000)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 100)
            self.assertEqual(self.Hilo.bet_level, 100)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertIsNone(self.Goma.pot_index)
            self.assertIsNone(self.Hilo.pot_index)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (3000,))


class TestGatherPotMethodWithStartingPot(TestCase):


    "Runs unit tests on Table method gather_pot where there is a starting main pot."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 500),
            structures.Player('Epa', 500),
            structures.Player('Fomi', 500),
            structures.Player('Goma', 200),
            structures.Player('Hilo', 200),
            structures.Player('Iris', 200),
        ]

        self.table = structures.Table(self.setup_players, min_bet=100)
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi, self.Goma, self.Hilo, self.Iris = self.setup_players

        for player in (self.Coral, self.Fomi, self.Iris):
            player.mark_is_folded()

        for player in (self.Andy, self.Boa, self.Dino, self.Epa, self.Goma, self.Hilo):
            player.decrease_stack(200)
            self.table.increase_central_pot(200)

        self.table.add_side_pot()

        for player in (self.Andy, self.Boa, self.Dino, self.Epa):
            player.increase_pot_index()
            player.decrease_stack(200)
            self.table.increase_central_pot(200)


    def test_no_bettor_players_with_starting_pot(self):

        "Tests pot gathering when no player places money."

        # Coral starts folded

        # Fomi starts folded

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))


    def test_one_bettor_with_starting_pot(self):

        "Tests pot gathering when only one player places money and the others fold."

        self.Andy.decrease_stack(100)
        self.Andy.increase_bet_level(100)

        self.Boa.mark_is_folded()

        # Coral starts folded

        self.Dino.mark_is_folded()

        self.Epa.mark_is_folded()

        # Fomi starts folded

        # Goma is all-in

        # Hilo is all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 900))


    def test_one_all_in_bettor_with_starting_pot(self):

        "Tests pot gathering when only one player goes all-in and the others fold."

        self.Andy.decrease_stack(600) # all-in
        self.Andy.increase_bet_level(600)

        self.Boa.mark_is_folded()

        # Coral starts folded

        self.Dino.mark_is_folded()

        self.Epa.mark_is_folded()

        # Fomi starts folded

        # Goma starts all-in

        # Hilo starts all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 600)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1400))


    def test_equal_bettors_with_starting_pot(self):

        "Tests pot gathering when multiple players place the same amount of money."

        self.Andy.decrease_stack(100)
        self.Andy.increase_bet_level(100)

        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        # Coral starts folded

        self.Dino.mark_is_folded()

        self.Epa.mark_is_folded()

        # Fomi starts folded

        # Goma starts all-in

        # Hilo starts all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1000))


    def test_equal_some_all_in_bettors_with_starting_pot(self):

        "Tests pot gathering when multiple players place the same amount of money, some going all-in."

        self.Andy.decrease_stack(100)
        self.Andy.increase_bet_level(100)

        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        # Coral starts folded

        self.Dino.decrease_stack(100) # all-in
        self.Dino.increase_bet_level(100)

        self.Epa.decrease_stack(100) # all-in
        self.Epa.increase_bet_level(100)

        # Fomi starts folded

        # Goma starts all-in

        # Hilo starts all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 100)
            self.assertEqual(self.Epa.bet_level, 100)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 2)
            self.assertEqual(self.Boa.pot_index, 2)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1200, 0))


    def test_unequal_bettors_with_starting_pot(self):

        "Tests pot gathering when multiple players place different amounts of money."

        self.Andy.decrease_stack(300)
        self.Andy.increase_bet_level(300)

        self.Boa.decrease_stack(300)
        self.Boa.increase_bet_level(300)

        # Coral starts folded

        self.Dino.decrease_stack(100) # all-in
        self.Dino.increase_bet_level(100)

        self.Epa.decrease_stack(100) # all-in
        self.Epa.increase_bet_level(100)

        # Fomi starts folded

        # Goma starts all-in

        # Hilo starts all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 300)
            self.assertEqual(self.Boa.bet_level, 300)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 100)
            self.assertEqual(self.Epa.bet_level, 100)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 2)
            self.assertEqual(self.Boa.pot_index, 2)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1200, 400))


    def test_unequal_all_in_bettors_with_starting_pot(self):

        """
        Tests pot gathering when all remaining players go all-in by placing different amounts of
        money.
        """

        self.Andy.decrease_stack(600) # all-in
        self.Andy.increase_bet_level(600)

        self.Boa.decrease_stack(600) # all-in
        self.Boa.increase_bet_level(600)

        # Coral starts folded

        self.Dino.decrease_stack(100) # all-in
        self.Dino.increase_bet_level(100)

        self.Epa.decrease_stack(100) # all-in
        self.Epa.increase_bet_level(100)

        # Fomi starts folded

        # Goma starts all-in

        # Hilo starts all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 600)
            self.assertEqual(self.Boa.bet_level, 600)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 100)
            self.assertEqual(self.Epa.bet_level, 100)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 2)
            self.assertEqual(self.Boa.pot_index, 2)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertEqual(self.Epa.pot_index, 1)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1200, 1000))


    def test_unequal_bettors_one_level_folded_with_starting_pot(self):

        """
        Tests pot gathering when multiple players place different amounts of money and one of the
        bet levels only contains folded players.
        """

        self.Andy.decrease_stack(300)
        self.Andy.increase_bet_level(300)

        self.Boa.decrease_stack(300)
        self.Boa.increase_bet_level(300)

        # Coral starts folded

        self.Dino.decrease_stack(50)
        self.Dino.increase_bet_level(50)
        self.Dino.mark_is_folded()

        self.Epa.decrease_stack(50)
        self.Epa.increase_bet_level(50)
        self.Epa.mark_is_folded()

        # Fomi starts folded

        # Goma starts all-in

        # Hilo starts all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 300)
            self.assertEqual(self.Boa.bet_level, 300)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 50)
            self.assertEqual(self.Epa.bet_level, 50)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 1500))


    def test_unequal_all_in_bettors_one_level_folded_with_no_starting_pot(self):

        """
        Tests pot gathering when all remaining players go all-in by placing different amounts of
        money and one of the bet levels only contains folded players.
        """

        self.Andy.decrease_stack(600)
        self.Andy.increase_bet_level(600)

        self.Boa.decrease_stack(600)
        self.Boa.increase_bet_level(600)

        # Coral starts folded

        self.Dino.decrease_stack(50)
        self.Dino.increase_bet_level(50)
        self.Dino.mark_is_folded()

        self.Epa.decrease_stack(50)
        self.Epa.increase_bet_level(50)
        self.Epa.mark_is_folded()

        # Fomi starts folded

        # Goma starts all-in

        # Hilo starts all-in

        # Iris starts folded

        with self.subTest('before gather'):

            self.assertEqual(self.Andy.bet_level, 600)
            self.assertEqual(self.Boa.bet_level, 600)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 50)
            self.assertEqual(self.Epa.bet_level, 50)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 800))

        self.table.gather_pot()

        with self.subTest('after gather'):

            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Goma.bet_level, 0)
            self.assertEqual(self.Hilo.bet_level, 0)
            self.assertEqual(self.Iris.bet_level, 0)

            self.assertEqual(self.Andy.pot_index, 1)
            self.assertEqual(self.Boa.pot_index, 1)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertEqual(self.Goma.pot_index, 0)
            self.assertEqual(self.Hilo.pot_index, 0)
            self.assertIsNone(self.Iris.pot_index)

            self.assertTupleEqual(self.table.split_central_pot, (1200, 2100))


if __name__ == '__main__':
    main()