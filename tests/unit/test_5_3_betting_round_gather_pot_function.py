"""
Defines unit tests on set_action_effects function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import engines, structures


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


class TestBettingRoundGatherPotFunctionWithZeroStartingPot(BaseTestCase):


    "Runs unit tests on gather_pot function where the starting pot is zero."


    def test_no_bettor_players_with_zero_starting_pot(self):

        "Tests pot gathering when no player places money."

        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertEqual(self.Coral.pot_index, 0)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertEqual(self.Coral.pot_index, 0)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (0,))


    def test_one_bettor_player_with_zero_starting_pot(self):

        "Tests pot gathering when only one player places money and the others fold."

        self.Andy.increase_bet_level(100)
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (100,))


    def test_equal_bettor_players_with_zero_starting_pot(self):

        "Tests pot gathering when multiple players place the same amount of money."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(100)

        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 100)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (400,))


    def test_unequal_bettor_players_with_zero_starting_pot(self):

        "Tests pot gathering when multiple players place different amounts of money."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Coral.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 2)
            self.assertTupleEqual(self.table.split_central_pot, (600, 900, 600))


    def test_unequal_bettor_players_lower_folded_with_zero_starting_pot(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the lowest bet level have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Andy.mark_is_folded()
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (1500, 600))


    def test_unequal_bettor_players_middle_folded_with_zero_starting_pot(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the middle bet level have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (600, 1500))


    def test_unequal_bettor_players_first_and_middle_folded_with_zero_starting_pot(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the first and middle bet levels have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Andy.mark_is_folded()
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (2100,))


class TestBettingRoundGatherPotFunctionWithStartingMainPot(BaseTestCase):


    "Runs unit tests on gather_pot function where there is a starting main pot."


    def setUp(self):

        super().setUp()
        self.table.increase_central_pot(1000)


    def test_no_bettor_players_with_starting_main_pot(self):

        "Tests pot gathering when no player places money."

        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertEqual(self.Coral.pot_index, 0)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertEqual(self.Coral.pot_index, 0)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))


    def test_one_bettor_player_with_starting_main_pot(self):

        "Tests pot gathering when only one player places money and the others fold."

        self.Andy.increase_bet_level(100)
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1100,))


    def test_equal_bettor_players_with_starting_main_pot(self):

        "Tests pot gathering when multiple players place the same amount of money."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(100)

        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 100)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1400,))


    def test_unequal_bettor_players_with_starting_main_pot(self):

        "Tests pot gathering when multiple players place different amounts of money."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Coral.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 2)
            self.assertTupleEqual(self.table.split_central_pot, (1600, 900, 600))


    def test_unequal_bettor_players_lower_folded_with_starting_main_pot(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the lowest bet level have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Andy.mark_is_folded()
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (2500, 600))


    def test_unequal_bettor_players_middle_folded_with_starting_main_pot(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the middle bet level have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (1600, 1500))


    def test_unequal_bettor_players_first_and_middle_folded_with_starting_main_pot(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the first and middle bet levels have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Andy.mark_is_folded()
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000,))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (3100,))


class TestBettingRoundGatherPotFunctionWithStartingSidePots(BaseTestCase):


    "Runs unit tests on gather_pot function where there are starting side pots."


    def setUp(self):

        super().setUp()
        self.table.increase_central_pot(1000)
        self.table.add_side_pot()
        self.table.increase_central_pot(500)
        self.table.add_side_pot()
        self.table.increase_central_pot(2000)


    def test_no_bettor_players_with_starting_side_pots(self):

        "Tests pot gathering when no player places money."

        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertEqual(self.Coral.pot_index, 0)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertEqual(self.Coral.pot_index, 0)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))


    def test_one_bettor_player_with_starting_side_pots(self):

        "Tests pot gathering when only one player places money and the others fold."

        self.Andy.increase_bet_level(100)
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertEqual(self.Coral.bet_level, 0)
            self.assertEqual(self.Dino.bet_level, 0)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2100))


    def test_equal_bettor_players_with_starting_side_pots(self):

        "Tests pot gathering when multiple players place the same amount of money."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(100)

        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 100)
            self.assertEqual(self.Epa.bet_level, 0)
            self.assertEqual(self.Fomi.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertIsNone(self.Fomi.pot_index)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2400))


    def test_unequal_bettor_players_with_starting_side_pots(self):

        "Tests pot gathering when multiple players place different amounts of money."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Coral.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 1)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 2)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2600, 900, 600))


    def test_unequal_bettor_players_lower_folded_with_starting_side_pots(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the lowest bet level have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Andy.mark_is_folded()
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertEqual(self.Dino.pot_index, 0)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 3500, 600))


    def test_unequal_bettor_players_middle_folded_with_starting_side_pots(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the middle bet level have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertEqual(self.Andy.pot_index, 0)
            self.assertEqual(self.Boa.pot_index, 0)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2600, 1500))


    def test_unequal_bettor_players_first_and_middle_folded_with_starting_side_pots(self):

        "Tests pot gathering when multiple players place different amounts of money and the ones with the first and middle bet levels have folded."

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(100)
        self.Dino.increase_bet_level(400)
        self.Epa.increase_bet_level(400)
        self.Fomi.increase_bet_level(1000)

        self.Andy.mark_is_folded()
        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()

        with self.subTest('before gather'):
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 400)
            self.assertEqual(self.Epa.bet_level, 400)
            self.assertEqual(self.Fomi.bet_level, 1000)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 2000))

        engines.gather_pot(self.table)

        with self.subTest('after gather'):
            for player in self.setup_players:
                self.assertEqual(player.bet_level, 0)
            self.assertIsNone(self.Andy.pot_index)
            self.assertIsNone(self.Boa.pot_index)
            self.assertIsNone(self.Coral.pot_index)
            self.assertIsNone(self.Dino.pot_index)
            self.assertIsNone(self.Epa.pot_index)
            self.assertEqual(self.Fomi.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (1000, 500, 4100))


if __name__ == '__main__':
    main()