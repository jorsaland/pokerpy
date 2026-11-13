"""
Defines unit tests on alternate_players function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, exceptions, engines, messages, states, structures


class TestBettingRoundPromptPlayerFunction(TestCase):


    "Runs unit tests on prompt_player function."


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


    def test_last_remaining_player(self):

        "Tests prompted player cannot parse an action because is the last one remaining in the hand cycle."

        self.table.set_current_player(self.Andy)

        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        generator = engines.prompt_player(self.table, open_fold_allowed=False)

        with self.subTest('initial state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)

        with self.subTest('closure state'):
            with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
                next(generator)
            self.assertEqual(context.exception.cause, messages.signal_last_player_in_hand)

        with self.subTest('final state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)


    def test_no_further_action_possible(self):

        "Tests prompted player cannot parse an action when everyone else is folded or all-in and there is no amount to call."

        self.table.set_current_player(self.Andy)

        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.decrease_stack(self.Dino.stack)
        self.Epa.decrease_stack(self.Epa.stack)
        self.Fomi.decrease_stack(self.Fomi.stack)

        generator = engines.prompt_player(self.table, open_fold_allowed=False)

        with self.subTest('initial state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)

        with self.subTest('closure state'):
            with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
                next(generator)
            self.assertEqual(context.exception.cause, messages.signal_no_further_action_possible)

        with self.subTest('final state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)


    def test_non_closing_folded_player(self):

        "Tests prompted player cannot parse an action because has already folded, given there are more players to listen."

        self.table.set_current_player(self.Andy)
        self.Andy.mark_is_folded()

        generator = engines.prompt_player(self.table, open_fold_allowed=False)

        with self.subTest('initial state'):
            self.assertFalse(self.Andy.has_played)
            self.assertTrue(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)

        with self.subTest('closure state'):
            with self.assertRaises(exceptions.JumpToNextPlayerSignal) as context:
                next(generator)
            self.assertEqual(context.exception.cause, messages.signal_folded_player)

        with self.subTest('final state'):
            self.assertFalse(self.Andy.has_played)
            self.assertTrue(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)


    def test_closing_folded_player(self):

        "Tests prompted player cannot parse an action because has already folded, given there are no more players to listen."

        self.table.set_current_player(self.Andy)
        self.table.set_stopping_player(self.Andy)
        self.Andy.mark_is_folded()

        generator = engines.prompt_player(self.table, open_fold_allowed=False)

        with self.subTest('initial state'):
            self.assertFalse(self.Andy.has_played)
            self.assertTrue(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Andy)

        with self.subTest('closure state'):
            with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
                next(generator)
            self.assertEqual(context.exception.cause, messages.signal_folded_stopping_player)

        with self.subTest('final state'):
            self.assertFalse(self.Andy.has_played)
            self.assertTrue(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Andy)


    def test_non_closing_all_in_player(self):

        "Tests prompted player cannot parse an action because is already all-in, given there are more players to listen."

        self.table.set_current_player(self.Andy)
        self.Andy.decrease_stack(self.Andy.stack)

        generator = engines.prompt_player(self.table, open_fold_allowed=False)

        with self.subTest('initial state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 0)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)

        with self.subTest('closure state'):
            with self.assertRaises(exceptions.JumpToNextPlayerSignal) as context:
                next(generator)
            self.assertEqual(context.exception.cause, messages.signal_all_in_player)

        with self.subTest('final state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 0)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)


    def test_closing_all_in_player(self):

        "Tests prompted player cannot parse an action because is already all-in, given there are no more players to listen."

        self.table.set_current_player(self.Andy)
        self.table.set_stopping_player(self.Andy)
        self.Andy.decrease_stack(self.Andy.stack)

        generator = engines.prompt_player(self.table, open_fold_allowed=False)

        with self.subTest('initial state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 0)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Andy)

        with self.subTest('closure state'):
            with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
                next(generator)
            self.assertEqual(context.exception.cause, messages.signal_all_in_stopping_player)

        with self.subTest('final state'):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 0)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Andy)


    def test_non_closing_passive_player_no_previous_aggression(self):

        """
        Tests prompted player parses a passive action, given there are more players to await and
        none has parsed an aggressive action yet.
        """

        actions = [
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CHECK),
        ]

        expected_action_ranges = {
            constants.ACTION_FOLD: range(0, 1),
            constants.ACTION_CHECK: range(0, 1),
            constants.ACTION_BET: range(100, 1001),
        }

        for action in actions:

            self.setUp()
            self.table.set_current_player(self.Andy)

            generator = engines.prompt_player(self.table, open_fold_allowed=True)

            with self.subTest('initial state', action=action):
                self.assertFalse(self.Andy.has_played)
                self.assertFalse(self.Andy.is_folded)
                self.assertEqual(self.Andy.stack, 1000)
                self.assertEqual(self.Andy.bet_level, 0)
                self.assertEqual(self.table.bet_level, 0)
                self.assertEqual(self.table.full_bet_level, 0)
                self.assertEqual(self.table.min_raise_increase, 100)
                self.assertEqual(self.table.stopping_player, self.Fomi)

            with self.subTest('yield state', action=action):
                await_state = next(generator)
                self.assertIsInstance(await_state, states.PlayerActionAwait)
                self.assertEqual(await_state.player, self.Andy)
                self.assertDictEqual(await_state.ranges, expected_action_ranges)

            await_state.request_action(action)

            with self.subTest('closure state', action=action):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)

            with self.subTest('final state'):
                self.assertTrue(self.Andy.has_played)
                if action.category == constants.ACTION_FOLD:
                    self.assertTrue(self.Andy.is_folded)
                else:
                    self.assertFalse(self.Andy.is_folded)
                self.assertEqual(self.Andy.stack, 1000)
                self.assertEqual(self.Andy.bet_level, 0)
                self.assertEqual(self.table.bet_level, 0)
                self.assertEqual(self.table.full_bet_level, 0)
                self.assertEqual(self.table.min_raise_increase, 100)
                self.assertEqual(self.table.stopping_player, self.Fomi)


    def test_non_closing_passive_player_previous_aggression(self):

        """
        Tests prompted player parses a passive action, given there are more players to await and
        there is a previous aggressive action.
        """

        action = structures.Action(constants.ACTION_CALL, 100)

        expected_action_ranges = {
            constants.ACTION_FOLD: range(0, 1),
            constants.ACTION_CALL: range(100, 101),
            constants.ACTION_RAISE: range(200, 1001),
        }

        self.table.set_current_player(self.Andy)
        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)


        generator = engines.prompt_player(self.table, open_fold_allowed=True)

        with self.subTest('initial state', action=action):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)

        with self.subTest('yield state', action=action):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerActionAwait)
            self.assertEqual(await_state.player, self.Andy)
            self.assertDictEqual(await_state.ranges, expected_action_ranges)

        await_state.request_action(action)

        with self.subTest('closure state', action=action):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final state'):
            self.assertTrue(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)


    def test_closing_passive_player_no_previous_aggression(self):

        """
        Tests prompted player parses a passive action, given there are no more players to await and
        none has parsed an aggressive action yet.
        """

        actions = [
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CHECK),
        ]

        expected_action_ranges = {
            constants.ACTION_FOLD: range(0, 1),
            constants.ACTION_CHECK: range(0, 1),
            constants.ACTION_BET: range(100, 1001),
        }

        for action in actions:

            self.setUp()
            self.table.set_current_player(self.Andy)
            self.table.set_stopping_player(self.Andy)

            generator = engines.prompt_player(self.table, open_fold_allowed=True)

            with self.subTest('initial state', action=action):
                self.assertFalse(self.Andy.has_played)
                self.assertFalse(self.Andy.is_folded)
                self.assertEqual(self.Andy.stack, 1000)
                self.assertEqual(self.Andy.bet_level, 0)
                self.assertEqual(self.table.bet_level, 0)
                self.assertEqual(self.table.full_bet_level, 0)
                self.assertEqual(self.table.min_raise_increase, 100)
                self.assertEqual(self.table.stopping_player, self.Andy)

            with self.subTest('yield state', action=action):
                await_state = next(generator)
                self.assertIsInstance(await_state, states.PlayerActionAwait)
                self.assertEqual(await_state.player, self.Andy)
                self.assertDictEqual(await_state.ranges, expected_action_ranges)

            await_state.request_action(action)

            with self.subTest('closure state', action=action):
                with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
                    next(generator)
                self.assertEqual(context.exception.cause, messages.signal_passive_stopping_player)

            with self.subTest('final state'):
                self.assertTrue(self.Andy.has_played)
                if action.category == constants.ACTION_FOLD:
                    self.assertTrue(self.Andy.is_folded)
                else:
                    self.assertFalse(self.Andy.is_folded)
                self.assertEqual(self.Andy.stack, 1000)
                self.assertEqual(self.Andy.bet_level, 0)
                self.assertEqual(self.table.bet_level, 0)
                self.assertEqual(self.table.full_bet_level, 0)
                self.assertEqual(self.table.min_raise_increase, 100)
                self.assertEqual(self.table.stopping_player, self.Andy)


    def test_closing_passive_player_previous_aggression(self):

        """
        Tests prompted player parses a passive action, given there are no more players to await and
        there is a previous aggressive action.
        """

        action = structures.Action(constants.ACTION_CALL, 100)

        expected_action_ranges = {
            constants.ACTION_FOLD: range(0, 1),
            constants.ACTION_CALL: range(100, 101),
            constants.ACTION_RAISE: range(200, 1001),
        }

        self.table.set_current_player(self.Andy)
        self.table.set_stopping_player(self.Andy)
        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)


        generator = engines.prompt_player(self.table, open_fold_allowed=True)

        with self.subTest('initial state', action=action):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Andy)

        with self.subTest('yield state', action=action):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerActionAwait)
            self.assertEqual(await_state.player, self.Andy)
            self.assertDictEqual(await_state.ranges, expected_action_ranges)

        await_state.request_action(action)

        with self.subTest('closure state', action=action):
            with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
                next(generator)
            self.assertEqual(context.exception.cause, messages.signal_passive_stopping_player)

        with self.subTest('final state'):
            self.assertTrue(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Andy)


    def test_non_closing_agressive_player(self):

        "Tests prompted player parses an aggressive action, given there are more players to listen."

        action = structures.Action(constants.ACTION_BET, 100)

        expected_action_ranges = {
            constants.ACTION_FOLD: range(0, 1),
            constants.ACTION_CHECK: range(0, 1),
            constants.ACTION_BET: range(100, 1001),
        }

        self.table.set_current_player(self.Andy)
        self.table.set_bet_level(0)
        self.table.set_full_bet_level(0)

        generator = engines.prompt_player(self.table, open_fold_allowed=True)

        with self.subTest('initial state', action=action):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)

        with self.subTest('yield state', action=action):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerActionAwait)
            self.assertEqual(await_state.player, self.Andy)
            self.assertDictEqual(await_state.ranges, expected_action_ranges)

        await_state.request_action(action)

        with self.subTest('closure state', action=action):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final state'):
            self.assertTrue(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)


    def test_closing_agressive_player(self):

        "Tests prompted player parses an aggressive action, given there are no more players to listen."

        action = structures.Action(constants.ACTION_BET, 100)

        expected_action_ranges = {
            constants.ACTION_FOLD: range(0, 1),
            constants.ACTION_CHECK: range(0, 1),
            constants.ACTION_BET: range(100, 1001),
        }

        self.table.set_current_player(self.Andy)
        self.table.set_stopping_player(self.Andy)
        self.table.set_bet_level(0)
        self.table.set_full_bet_level(0)

        generator = engines.prompt_player(self.table, open_fold_allowed=True)

        with self.subTest('initial state', action=action):
            self.assertFalse(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 1000)
            self.assertEqual(self.Andy.bet_level, 0)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Andy)

        with self.subTest('yield state', action=action):
            await_state = next(generator)
            self.assertIsInstance(await_state, states.PlayerActionAwait)
            self.assertEqual(await_state.player, self.Andy)
            self.assertDictEqual(await_state.ranges, expected_action_ranges)

        await_state.request_action(action)

        with self.subTest('closure state', action=action):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        with self.subTest('final state'):
            self.assertTrue(self.Andy.has_played)
            self.assertFalse(self.Andy.is_folded)
            self.assertEqual(self.Andy.stack, 900)
            self.assertEqual(self.Andy.bet_level, 100)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.stopping_player, self.Fomi)


if __name__ == '__main__':
    main()