"""
Defines unit tests on functions related to placing blinds.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import engines, structures


class TestHandCyclePlaceSmallBlindFunction(TestCase):


    "Runs unit tests on place_small_blind function."


    def test_no_stack_small_blind(self):

        "Tests when player has zero stack."

        player = structures.Player('Andy', 0)

        with self.subTest('before small blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 0)

        engines.place_small_blind(50, player)

        with self.subTest('after small blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 0)


    def test_stack_under_small_blind(self):

        "Tests when player has a stack under small blind amount."

        player = structures.Player('Andy', 10)

        with self.subTest('before small blind placing'):
            self.assertEqual(player.stack, 10)
            self.assertEqual(player.bet_level, 0)

        engines.place_small_blind(50, player)

        with self.subTest('after small blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 10)


    def test_stack_equal_small_blind(self):

        "Tests when player has a stack equal to the small blind amount."

        player = structures.Player('Andy', 50)

        with self.subTest('before small blind placing'):
            self.assertEqual(player.stack, 50)
            self.assertEqual(player.bet_level, 0)

        engines.place_small_blind(50, player)

        with self.subTest('after small blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 50)


    def test_stack_over_small_blind(self):

        "Tests when player has a stack larger than the small blind amount."

        player = structures.Player('Andy', 1000)

        with self.subTest('before small blind placing'):
            self.assertEqual(player.stack, 1000)
            self.assertEqual(player.bet_level, 0)

        engines.place_small_blind(50, player)

        with self.subTest('after small blind placing'):
            self.assertEqual(player.stack, 950)
            self.assertEqual(player.bet_level, 50)


class TestHandCyclePlaceBigBlindFunction(TestCase):


    "Runs unit tests on place_big_blind function."


    def test_no_stack_big_blind(self):

        "Tests when player has zero stack."

        player = structures.Player('Andy', 0)

        with self.subTest('before big blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 0)

        with self.subTest('failed big blind placing'):
            with self.assertRaises(AssertionError):
                engines.place_big_blind(100, player)


    def test_stack_under_big_blind(self):

        "Tests when player has a stack under big blind amount."

        player = structures.Player('Andy', 10)

        with self.subTest('before big blind placing'):
            self.assertEqual(player.stack, 10)
            self.assertEqual(player.bet_level, 0)

        engines.place_big_blind(100, player)

        with self.subTest('after big blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 10)


    def test_stack_equal_to_big_blind(self):

        "Tests when player has a stack equal to the big blind amount."

        player = structures.Player('Andy', 100)

        with self.subTest('before big blind placing'):
            self.assertEqual(player.stack, 100)
            self.assertEqual(player.bet_level, 0)

        engines.place_big_blind(100, player)

        with self.subTest('after big blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 100)


    def test_stack_over_big_blind(self):

        "Tests when player has a stack larger than the big blind amount."

        player = structures.Player('Andy', 1000)

        with self.subTest('before big blind placing'):
            self.assertEqual(player.stack, 1000)
            self.assertEqual(player.bet_level, 0)

        engines.place_big_blind(100, player)

        with self.subTest('after big blind placing'):
            self.assertEqual(player.stack, 900)
            self.assertEqual(player.bet_level, 100)


class TestHandCyclePlaceExtraBigBlindsFunction(TestCase):


    "Runs unit tests on place_extra_big_blinds function."


    def test_no_stacks_extra_big_blinds(self):

        "Tests when players have zero stack."

        players = (
            Andy := structures.Player('Andy', 0),
            Boa := structures.Player('Boa', 0),
            Coral := structures.Player('Coral', 0),
            Dino := structures.Player('Dino', 0),
            Epa := structures.Player('Epa', 0),
            Fomi := structures.Player('Fomi', 0),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 0)
                self.assertEqual(player.bet_level, 0)

        for player in generator:
            if player in (Andy, Boa, Coral):
                player.mark_is_extra_blind()

        with self.subTest('after big blind placing'):
            for player in (Andy, Boa, Coral):
                self.assertTrue(player.is_extra_blind)
                self.assertEqual(player.stack, 0)
                self.assertEqual(player.bet_level, 0)
            for player in (Dino, Epa, Fomi):
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 0)
                self.assertEqual(player.bet_level, 0)


    def test_stacks_under_big_blind(self):

        "Tests when players have stacks under big blind amount."

        players = (
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            Epa := structures.Player('Epa', 10),
            Fomi := structures.Player('Fomi', 10),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 10)
                self.assertEqual(player.bet_level, 0)

        for player in generator:
            if player in (Andy, Boa, Coral):
                player.mark_is_extra_blind()

        with self.subTest('after big blind placing'):
            for player in (Andy, Boa, Coral):
                self.assertTrue(player.is_extra_blind)
                self.assertEqual(player.stack, 0)
                self.assertEqual(player.bet_level, 10)
            for player in (Dino, Epa, Fomi):
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 10)
                self.assertEqual(player.bet_level, 0)


    def test_stacks_equal_to_big_blind(self):

        "Tests when players have stacks equal to big blind amount."

        players = (
            Andy := structures.Player('Andy', 100),
            Boa := structures.Player('Boa', 100),
            Coral := structures.Player('Coral', 100),
            Dino := structures.Player('Dino', 100),
            Epa := structures.Player('Epa', 100),
            Fomi := structures.Player('Fomi', 100),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 100)
                self.assertEqual(player.bet_level, 0)

        for player in generator:
            if player in (Andy, Boa, Coral):
                player.mark_is_extra_blind()

        with self.subTest('after big blind placing'):
            for player in (Andy, Boa, Coral):
                self.assertTrue(player.is_extra_blind)
                self.assertEqual(player.stack, 0)
                self.assertEqual(player.bet_level, 100)
            for player in (Dino, Epa, Fomi):
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 100)
                self.assertEqual(player.bet_level, 0)


    def test_stacks_equal_over_big_blind(self):

        "Tests when players have stacks larger than big blind amount."

        players = (
            Andy := structures.Player('Andy', 1000),
            Boa := structures.Player('Boa', 1000),
            Coral := structures.Player('Coral', 1000),
            Dino := structures.Player('Dino', 1000),
            Epa := structures.Player('Epa', 1000),
            Fomi := structures.Player('Fomi', 1000),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 1000)
                self.assertEqual(player.bet_level, 0)

        for player in generator:
            if player in (Andy, Boa, Coral):
                player.mark_is_extra_blind()

        with self.subTest('after big blind placing'):
            for player in (Andy, Boa, Coral):
                self.assertTrue(player.is_extra_blind)
                self.assertEqual(player.stack, 900)
                self.assertEqual(player.bet_level, 100)
            for player in (Dino, Epa, Fomi):
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 1000)
                self.assertEqual(player.bet_level, 0)


    def test_mixed_stack_conditions(self):

        "Tests when players have stacks are set with different amounts, related to the big blind amount."

        players = (
            Andy := structures.Player('Andy', 1000),
            Boa := structures.Player('Boa', 1000),
            Coral := structures.Player('Coral', 1000),
            Dino := structures.Player('Dino', 100),
            Epa := structures.Player('Epa', 10),
            Fomi := structures.Player('Fomi', 0),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):

            for player in (Andy, Boa, Coral):
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 1000)
                self.assertEqual(player.bet_level, 0)

            self.assertFalse(Dino.is_extra_blind)
            self.assertEqual(Dino.stack, 100)
            self.assertEqual(Dino.bet_level, 0)

            self.assertFalse(Epa.is_extra_blind)
            self.assertEqual(Epa.stack, 10)
            self.assertEqual(Epa.bet_level, 0)

            self.assertFalse(Fomi.is_extra_blind)
            self.assertEqual(Fomi.stack, 0)
            self.assertEqual(Fomi.bet_level, 0)


        for player in generator:
            if player in (Coral, Dino, Epa, Fomi):
                player.mark_is_extra_blind()

        with self.subTest('after big blind placing'):

            for player in (Andy, Boa):
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.stack, 1000)
                self.assertEqual(player.bet_level, 0)

            self.assertTrue(Coral.is_extra_blind)
            self.assertEqual(Coral.stack, 900)
            self.assertEqual(Coral.bet_level, 100)

            self.assertTrue(Dino.is_extra_blind)
            self.assertEqual(Dino.stack, 0)
            self.assertEqual(Dino.bet_level, 100)

            self.assertTrue(Epa.is_extra_blind)
            self.assertEqual(Epa.stack, 0)
            self.assertEqual(Epa.bet_level, 10)

            self.assertTrue(Fomi.is_extra_blind)
            self.assertEqual(Fomi.stack, 0)
            self.assertEqual(Fomi.bet_level, 0)


if __name__ == '__main__':
    main()