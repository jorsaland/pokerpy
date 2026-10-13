"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestTableIterPlayersMethod(TestCase):


    "Runs unit tests on Table method iter_players."


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

        self.setup_full_deck = tuple(structures.Card(value, suit) for value, suit in constants.sorted_card_values_and_suits)


    def test_type_errors(self):

        "Tests type error detection in iterator."

        table = structures.Table(self.setup_players)

        bad_players = (1, 'Andy')

        for bad_player in bad_players:

            with self.subTest(player=bad_player):
                with self.assertRaises(TypeError) as context:
                    table.iter_players(bad_player)
                self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(type(bad_player).__name__))


    def test_value_errors(self):

        "Tests value error detection in iterator."

        table = structures.Table(self.setup_players)

        player_not_in_table = structures.Player('Zero', 1000)

        with self.subTest('player not in table'):
            with self.assertRaises(ValueError) as context:
                table.iter_players(player_not_in_table)
            self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(player_not_in_table.name))


    def test_forward_iteration_with_next_function(self):

        "Tests next function on generator, going forward."

        table = structures.Table(self.setup_players)

        generator = table.iter_players()
        for player in self.setup_players:
            with self.subTest('next on default starting player', expected_next=player.name):
                self.assertEqual(next(generator), player)
        with self.subTest('next on default starting player (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        for i, starting_player in enumerate(self.setup_players):

            generator = table.iter_players(starting_player)
            for player in (*self.setup_players[i:], *self.setup_players[:i]):
                with self.subTest('next', starting=starting_player.name, expected_next=player.name):
                    self.assertEqual(next(generator), player)
            with self.subTest('next (stop iteration)', starting=starting_player):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)


    def test_backward_iteration_with_next_function(self):

        "Tests next function on generator, going backards."

        table = structures.Table(self.setup_players)

        generator = table.iter_players(reverse=True)
        for player in (self.setup_players[0], *self.setup_players[:0:-1]):
            with self.subTest('next on default starting player', expected_next=player.name):
                self.assertEqual(next(generator), player)
        with self.subTest('next on default starting player (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        for i, starting_player in enumerate(self.setup_players):

            generator = table.iter_players(starting_player, reverse=True)
            for player in (*self.setup_players[i::-1], *self.setup_players[:i:-1]):
                with self.subTest('next', starting=starting_player.name, expected_next=player.name):
                    self.assertEqual(next(generator), player)
            with self.subTest('next (stop iteration)', starting=starting_player):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)


    def test_forward_iteration_with_for_loop(self):

        "Tests for loop on generator, going forward."

        table = structures.Table(self.setup_players)

        expected_iterable = self.setup_players
        actual_iterable = table.iter_players()
        for expected_player, actual_player in zip(expected_iterable, actual_iterable):
            with self.subTest('for loop on default starting player', expected_iter=expected_player.name):
                self.assertEqual(expected_player, actual_player)

        for i, starting_player in enumerate(self.setup_players):
            expected_iterable = (*self.setup_players[i:], *self.setup_players[:i])
            actual_iterable = table.iter_players(starting_player)
            for expected_player, actual_player in zip(expected_iterable, actual_iterable):
                with self.subTest('for loop', starting=starting_player.name, expected_iter=expected_player.name):
                    self.assertEqual(expected_player, actual_player)


    def test_backward_iteration_with_for_loop(self):

        "Tests for loop on generator, going backwards."

        table = structures.Table(self.setup_players)

        expected_iterable = (self.setup_players[0], *self.setup_players[:0:-1])
        actual_iterable = table.iter_players(reverse=True)
        for expected_player, actual_player in zip(expected_iterable, actual_iterable):
            with self.subTest('for loop on default starting player', expected_iter=expected_player.name):
                self.assertEqual(expected_player, actual_player)

        for i, starting_player in enumerate(self.setup_players):
            expected_iterable = (*self.setup_players[i::-1], *self.setup_players[:i:-1])
            actual_iterable = table.iter_players(starting_player, reverse=True)
            for expected_player, actual_player in zip(expected_iterable, actual_iterable):
                with self.subTest('for loop', starting=starting_player.name, expected_iter=expected_player.name):
                    self.assertEqual(expected_player, actual_player)


    def test_iteration_edge_cases(self):

        "Tests iterator under edge cases."

        player = structures.Player('Zero', 1000)
        table = structures.Table([player])

        generator = table.iter_players()
        with self.subTest('forward next on single player table', expected_next=player.name):
            self.assertEqual(next(generator), player)
        with self.subTest('forward next on single player table (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        generator = table.iter_players(reverse=True)
        with self.subTest('backard next on single player table', expected_next=player.name):
            self.assertEqual(next(generator), player)
        with self.subTest('backard next on single player table (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        for iterated_player in table.iter_players():
            with self.subTest('forward for loop on single player table', expected_iter=player.name):
                self.assertEqual(iterated_player, player)

        for iterated_player in table.iter_players(reverse=True):
            with self.subTest('backard for loop on single player table', expected_iter=player.name):
                self.assertEqual(iterated_player, player)


if __name__ == '__main__':
    main()