"""
Defines unit tests on functions related to placing blinds.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import engines, states, structures


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

        engines.place_big_blind(100, player)

        with self.subTest('after big blind placing'):
            self.assertEqual(player.stack, 0)
            self.assertEqual(player.bet_level, 0)


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
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('initial states'):
            for player in players:
                self.assertEqual(player.stack, 0)
                self.assertEqual(player.bet_level, 0)

        with self.subTest('closure state'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final states'):
            for player in players:
                self.assertEqual(player.stack, 0)
                self.assertEqual(player.bet_level, 0)


    def test_stacks_under_big_blind(self):

        "Tests when players have stacks under big blind amount."

        players = (
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertEqual(player.stack, 10)
                self.assertEqual(player.bet_level, 0)

        with self.subTest('first yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Andy)
            self.assertEqual(await_state.amount, 10)
            await_state.place_blind()

        with self.subTest('second yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Boa)
            self.assertEqual(await_state.amount, 10)
            await_state.place_blind()

        with self.subTest('third yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Coral)
            self.assertEqual(await_state.amount, 10)

        with self.subTest('fourth yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Dino)
            self.assertEqual(await_state.amount, 10)

        with self.subTest('closure state'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final states'):
            for player in players:
                if player in (Andy, Boa):
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.bet_level, 10)
                else:
                    self.assertEqual(player.stack, 10)
                    self.assertEqual(player.bet_level, 0)


    def test_stacks_equal_to_big_blind(self):

        "Tests when players have stacks equal to big blind amount."

        players = (
            Andy := structures.Player('Andy', 100),
            Boa := structures.Player('Boa', 100),
            Coral := structures.Player('Coral', 100),
            Dino := structures.Player('Dino', 100),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertEqual(player.stack, 100)
                self.assertEqual(player.bet_level, 0)

        with self.subTest('first yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Andy)
            self.assertEqual(await_state.amount, 100)
            await_state.place_blind()

        with self.subTest('second yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Boa)
            self.assertEqual(await_state.amount, 100)
            await_state.place_blind()

        with self.subTest('third yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Coral)
            self.assertEqual(await_state.amount, 100)

        with self.subTest('fourth yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Dino)
            self.assertEqual(await_state.amount, 100)

        with self.subTest('closure state'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final states'):
            for player in players:
                if player in (Andy, Boa):
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.bet_level, 100)
                else:
                    self.assertEqual(player.stack, 100)
                    self.assertEqual(player.bet_level, 0)


    def test_stacks_equal_over_big_blind(self):

        "Tests when players have stacks larger than big blind amount."

        players = (
            Andy := structures.Player('Andy', 1000),
            Boa := structures.Player('Boa', 1000),
            Coral := structures.Player('Coral', 1000),
            Dino := structures.Player('Dino', 1000),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertEqual(player.stack, 1000)
                self.assertEqual(player.bet_level, 0)

        with self.subTest('first yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Andy)
            self.assertEqual(await_state.amount, 100)
            await_state.place_blind()

        with self.subTest('second yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Boa)
            self.assertEqual(await_state.amount, 100)
            await_state.place_blind()

        with self.subTest('third yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Coral)
            self.assertEqual(await_state.amount, 100)

        with self.subTest('fourth yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Dino)
            self.assertEqual(await_state.amount, 100)

        with self.subTest('closure state'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final states'):
            for player in players:
                if player in (Andy, Boa):
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.bet_level, 100)
                else:
                    self.assertEqual(player.stack, 1000)
                    self.assertEqual(player.bet_level, 0)


    def test_mixed_stack_conditions(self):

        "Tests when players have stacks are set with different amounts, related to the big blind amount."

        players = (
            Andy := structures.Player('Andy', 1000),
            Boa := structures.Player('Boa', 100),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 0),
        )

        generator = engines.place_extra_big_blinds(100, players)

        with self.subTest('before big blind placing'):
            for player in players:
                self.assertEqual(player.bet_level, 0)
                if player == Andy:
                    self.assertEqual(player.stack, 1000)
                elif player == Boa:
                    self.assertEqual(player.stack, 100)
                elif player == Coral:
                    self.assertEqual(player.stack, 10)
                elif player == Dino:
                    self.assertEqual(player.stack, 0)
                else:
                    raise AssertionError()

        with self.subTest('first yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Andy)
            self.assertEqual(await_state.amount, 100)
            await_state.place_blind()

        with self.subTest('second yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Boa)
            self.assertEqual(await_state.amount, 100)
            await_state.place_blind()

        with self.subTest('third yield state'):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerBlindAwait)
            self.assertEqual(await_state.player, Coral)
            self.assertEqual(await_state.amount, 10)
            await_state.place_blind()

        with self.subTest('closure state'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final states'):
            for player in players:
                if player == Andy:
                    self.assertEqual(player.stack, 900)
                    self.assertEqual(player.bet_level, 100)
                elif player == Boa:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.bet_level, 100)
                elif player == Coral:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.bet_level, 10)
                elif player == Dino:
                    self.assertEqual(player.stack, 0)
                    self.assertEqual(player.bet_level, 0)
                else:
                    raise AssertionError()


if __name__ == '__main__':
    main()