"""
Defines unit tests on refund_excess function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import engines, structures


class TestRefundExcessFunction(TestCase):


    "Runs unit tests on refund_excess function."


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


    def test_all_max_level_players_are_alive(self):

        "Tests refund behaviour when all the players with the max bet level are alive."

        self.Andy.decrease_stack(100)
        self.Boa.decrease_stack(100)
        self.Coral.decrease_stack(300)
        self.Dino.decrease_stack(300)
        self.Epa.decrease_stack(500)
        self.Fomi.decrease_stack(500)

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(300)
        self.Dino.increase_bet_level(300)
        self.Epa.increase_bet_level(500)
        self.Fomi.increase_bet_level(500)

        with self.subTest('before refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 500)
            self.assertEqual(self.Fomi.stack, 500)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 500)

        engines.refund_excess(self.table)

        with self.subTest('after refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 500)
            self.assertEqual(self.Fomi.stack, 500)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 500)


    def test_one_max_level_players_is_alive(self):

        "Tests refund behaviour when only one of the players with the max bet level is alive."

        self.Andy.decrease_stack(100)
        self.Boa.decrease_stack(100)
        self.Coral.decrease_stack(300)
        self.Dino.decrease_stack(300)
        self.Epa.decrease_stack(500)
        self.Fomi.decrease_stack(500)

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(300)
        self.Dino.increase_bet_level(300)
        self.Epa.increase_bet_level(500)
        self.Fomi.increase_bet_level(500)

        self.Fomi.mark_is_folded()

        with self.subTest('before refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 500)
            self.assertEqual(self.Fomi.stack, 500)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 500)

        engines.refund_excess(self.table)

        with self.subTest('after refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 500)
            self.assertEqual(self.Fomi.stack, 500)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 500)


    def test_no_max_level_players_are_alive(self):

        "Tests refund behaviour when no players with the max bet level are alive."

        self.Andy.decrease_stack(100)
        self.Boa.decrease_stack(100)
        self.Coral.decrease_stack(300)
        self.Dino.decrease_stack(300)
        self.Epa.decrease_stack(500)
        self.Fomi.decrease_stack(500)

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(300)
        self.Dino.increase_bet_level(300)
        self.Epa.increase_bet_level(500)
        self.Fomi.increase_bet_level(500)

        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 500)
            self.assertEqual(self.Fomi.stack, 500)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 500)

        engines.refund_excess(self.table)

        with self.subTest('after refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 700)
            self.assertEqual(self.Fomi.stack, 700)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 300)
            self.assertEqual(self.Fomi.bet_level, 300)


    def test_no_max_level_players_are_alive_one_next_level_is_alive(self):

        "Tests refund behaviour when no players with the max bet level are alive and there is only one player alive in the next max level."

        self.Andy.decrease_stack(100)
        self.Boa.decrease_stack(100)
        self.Coral.decrease_stack(300)
        self.Dino.decrease_stack(300)
        self.Epa.decrease_stack(500)
        self.Fomi.decrease_stack(500)

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(300)
        self.Dino.increase_bet_level(300)
        self.Epa.increase_bet_level(500)
        self.Fomi.increase_bet_level(500)

        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 500)
            self.assertEqual(self.Fomi.stack, 500)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 500)

        engines.refund_excess(self.table)

        with self.subTest('after refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 700)
            self.assertEqual(self.Fomi.stack, 700)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 300)
            self.assertEqual(self.Fomi.bet_level, 300)


    def test_no_max_level_players_are_alive_no_next_level_is_alive(self):

        "Tests refund behaviour when no players with the max bet level are alive, as well as in the next max bet level."

        self.Andy.decrease_stack(100)
        self.Boa.decrease_stack(100)
        self.Coral.decrease_stack(300)
        self.Dino.decrease_stack(300)
        self.Epa.decrease_stack(500)
        self.Fomi.decrease_stack(500)

        self.Andy.increase_bet_level(100)
        self.Boa.increase_bet_level(100)
        self.Coral.increase_bet_level(300)
        self.Dino.increase_bet_level(300)
        self.Epa.increase_bet_level(500)
        self.Fomi.increase_bet_level(500)

        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        with self.subTest('before refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 700)
            self.assertEqual(self.Dino.stack, 700)
            self.assertEqual(self.Epa.stack, 500)
            self.assertEqual(self.Fomi.stack, 500)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 300)
            self.assertEqual(self.Dino.bet_level, 300)
            self.assertEqual(self.Epa.bet_level, 500)
            self.assertEqual(self.Fomi.bet_level, 500)

        engines.refund_excess(self.table)

        with self.subTest('after refund'):
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Coral.stack, 900)
            self.assertEqual(self.Dino.stack, 900)
            self.assertEqual(self.Epa.stack, 900)
            self.assertEqual(self.Fomi.stack, 900)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertEqual(self.Coral.bet_level, 100)
            self.assertEqual(self.Dino.bet_level, 100)
            self.assertEqual(self.Epa.bet_level, 100)
            self.assertEqual(self.Fomi.bet_level, 100)


if __name__ == '__main__':
    main()