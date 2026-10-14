"""
Defines unit tests on BettingRound class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import engines, structures


class TestHandCycleAnteRoundFunction(TestCase):


    "Runs unit tests on ante_round function."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi = self.setup_players

        self.table = structures.Table(self.setup_players)
        self.table.set_ante(10)


    def test_unset_ante(self):

        "Tests when the ante was not set."

        table = structures.Table(self.setup_players)

        with self.assertRaises(AssertionError):
            engines.ante_round(table)


    def test_no_actionable_players(self):

        "Tests when there are no actionable players on the table."

        for player in self.setup_players:
            player.mark_is_folded()

        with self.subTest('before ante round'):
            for player in self.setup_players:
                self.assertEqual(player.stack, 1000)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.ante_round(self.table)

        with self.subTest('after ante round'):
            for player in self.setup_players:
                self.assertEqual(player.stack, 1000)
            self.assertTupleEqual(self.table.split_central_pot, (0,))


    def test_some_actionable_players_under_ante_stacks(self):

        "Tests when there are some actionable players on the table, all with stacks under ante."

        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(2)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(2)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(5)

        self.Dino.decrease_stack(self.Dino.stack)
        self.Dino.increase_stack(5)

        with self.subTest('before ante round'):
            for player in self.setup_players:
                if player in (self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                elif player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 2)
                else:
                    self.assertEqual(player.stack, 5)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.ante_round(self.table)

        with self.subTest('after ante round'):
            for player in self.setup_players:
                if player in (self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                elif player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (8, 6))


    def test_some_actionable_players_full_stacks(self):

        "Tests when there are some actionable players on the table, all with full stacks."

        for player in (self.Epa, self.Fomi):
            player.mark_is_folded()

        with self.subTest('before ante round'):
            for player in self.setup_players:
                self.assertEqual(player.stack, 1000)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.ante_round(self.table)

        with self.subTest('after ante round'):
            for player in self.setup_players:
                if player in (self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                else:
                    self.assertEqual(player.stack, 990)
                    self.assertEqual(player.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (40,))


    def test_some_actionable_players_under_ante_and_full_stacks(self):

        """
        Tests when there are some actionable players on the table, some with under-ante stacks and
        some with full stacks.
        """

        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(5)

        self.Dino.decrease_stack(self.Dino.stack)
        self.Dino.increase_stack(5)

        with self.subTest('before ante round'):
            for player in self.setup_players:
                if player in (self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                elif player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 1000)
                else:
                    self.assertEqual(player.stack, 5)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.ante_round(self.table)

        with self.subTest('after ante round'):
            for player in self.setup_players:
                if player in (self.Epa, self.Fomi):
                    self.assertEqual(player.stack, 1000)
                elif player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 990)
                    self.assertEqual(player.pot_index, 1)
                else:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (20, 10))


    def test_all_actionable_players_under_ante_stacks(self):

        "Tests when all players on table are actionable and have stacks under ante."

        self.Andy.decrease_stack(self.Andy.stack)
        self.Andy.increase_stack(2)

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(2)

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(5)

        self.Dino.decrease_stack(self.Dino.stack)
        self.Dino.increase_stack(5)

        self.Epa.decrease_stack(self.Epa.stack)
        self.Epa.increase_stack(7)

        self.Fomi.decrease_stack(self.Fomi.stack)
        self.Fomi.increase_stack(7)


        with self.subTest('before ante round'):
            for player in self.setup_players:
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 2)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 5)
                else:
                    self.assertEqual(player.stack, 7)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.ante_round(self.table)

        with self.subTest('after ante round'):
            for player in self.setup_players:
                self.assertEqual(player.stack, 0)
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.pot_index, 0)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.pot_index, 1)
                else:
                    self.assertEqual(player.pot_index, 2)
            self.assertTupleEqual(self.table.split_central_pot, (12, 12, 4))


    def test_all_actionable_players_full_stacks(self):

        "Tests when all players on table are actionable and have full stacks."

        with self.subTest('before ante round'):
            for player in self.setup_players:
                self.assertEqual(player.stack, 1000)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.ante_round(self.table)

        with self.subTest('after ante round'):
            for player in self.setup_players:
                self.assertEqual(player.stack, 990)
                self.assertEqual(player.pot_index, 0)
            self.assertTupleEqual(self.table.split_central_pot, (60,))


    def test_all_actionable_players_under_ante_and_full_stacks(self):

        """
        Tests when all players on table are actionable, some with under-ante stacks and some with
        full stacks.
        """

        self.Coral.decrease_stack(self.Coral.stack)
        self.Coral.increase_stack(2)

        self.Dino.decrease_stack(self.Dino.stack)
        self.Dino.increase_stack(2)

        self.Epa.decrease_stack(self.Epa.stack)
        self.Epa.increase_stack(5)

        self.Fomi.decrease_stack(self.Fomi.stack)
        self.Fomi.increase_stack(5)

        with self.subTest('before ante round'):
            for player in self.setup_players:
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 1000)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 2)
                else:
                    self.assertEqual(player.stack, 5)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        engines.ante_round(self.table)

        with self.subTest('after ante round'):
            for player in self.setup_players:
                if player in (self.Andy, self.Boa):
                    self.assertEqual(player.stack, 990)
                    self.assertEqual(player.pot_index, 2)
                elif player in (self.Coral, self.Dino):
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 0)
                else:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.pot_index, 1)
            self.assertTupleEqual(self.table.split_central_pot, (12, 12, 10))


if __name__ == '__main__':
    main()