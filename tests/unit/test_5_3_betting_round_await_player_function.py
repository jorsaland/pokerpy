"""
Defines unit tests on await_player function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, messages, states, structures


class TestBettingRoundAwaitPlayerFunction(TestCase):


    "Runs unit tests on await_player function."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]

        self.table = structures.Table(self.setup_players)
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi = self.setup_players

        self.action_ranges = {constants.ACTION_CHECK: range(0, 1), constants.ACTION_BET: range(10, 1001)}


    def test_skip_action(self):

        "Tests skipping action"

        generator = engines.await_player(self.Andy, self.action_ranges)

        with self.subTest('generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertDictEqual(await_state.ranges, self.action_ranges)

        with self.subTest('generator end'):
            with self.assertRaises(RuntimeError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_missing_action)


    def test_parse_invalid_action(self):

        "Tests parsing an invalid action"

        action = structures.Action(constants.ACTION_FOLD)

        generator = engines.await_player(self.Andy, self.action_ranges)

        with self.subTest('generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertDictEqual(await_state.ranges, self.action_ranges)

        await_state.request_action(action)

        with self.subTest('generator end'):
            with self.assertRaises(RuntimeError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)


    def test_parse_valid_action(self):

        "Tests parsing a valid action"

        action = structures.Action(constants.ACTION_CHECK)

        generator = engines.await_player(self.Andy, self.action_ranges)

        with self.subTest('generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertDictEqual(await_state.ranges, self.action_ranges)

        await_state.request_action(action)

        with self.subTest('generator end'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertEqual(context.exception.value, action)


if __name__ == '__main__':
    main()