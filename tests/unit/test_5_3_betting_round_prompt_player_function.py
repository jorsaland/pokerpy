"""
Defines unit tests on alternate_players function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, exceptions, engines, messages, structures


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

        self.Andy = self.setup_players[0]
        self.Boa = self.setup_players[1]
        self.Coral = self.setup_players[2]
        self.Dino = self.setup_players[3]
        self.Epa = self.setup_players[4]
        self.Fomi = self.setup_players[5]


    def test_non_closing_folded_player(self):

        "Tests prompted player cannot parse an action because has already folded, given there are more players to listen."

        self.table.set_current_player(self.Andy)

        self.Andy.mark_is_folded()

        generator = engines.prompt_player(
            table = self.table,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.assertRaises(exceptions.JumpToNextPlayerSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_folded_player)


    def test_closing_folded_player(self):

        "Tests prompted player cannot parse an action because has already folded, given there are no more players to listen."

        self.table.set_current_player(self.Andy)
        self.table.set_stopping_player(self.Andy)

        self.Andy.mark_is_folded()

        generator = engines.prompt_player(
            table = self.table,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_folded_stopping_player)


    def test_non_closing_all_in_player(self):

        "Tests prompted player cannot parse an action because is already all-in, given there are more players to listen."

        self.table.set_current_player(self.Andy)

        self.Andy.decrease_stack(self.Andy.stack)

        generator = engines.prompt_player(
            table = self.table,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.assertRaises(exceptions.JumpToNextPlayerSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_all_in_player)


    def test_closing_all_in_player(self):

        "Tests prompted player cannot parse an action because is already all-in, given there are no more players to listen."

        self.table.set_current_player(self.Andy)
        self.table.set_stopping_player(self.Andy)

        self.Andy.decrease_stack(self.Andy.stack)

        generator = engines.prompt_player(
            table = self.table,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_all_in_stopping_player)


    def test_non_closing_passive_player(self):

        "Tests prompted player parses a passive action, given there are more players to listen."

        actions = [
            structures.Action(constants.ACTION_CHECK),
            structures.Action(constants.ACTION_CALL, 100),
            structures.Action(constants.ACTION_FOLD),
        ]

        for action in actions:

            self.setUp()
            self.table.set_current_player(self.Andy)

            if action.category == constants.ACTION_CALL:
                self.table.set_bet_level(100)
                self.table.set_full_bet_level(100)

            generator = engines.prompt_player(
                table = self.table,
                open_fold_allowed = True,
                raise_invalid_actions = True,
            )

            with self.subTest('before prompt', action=action):
                self.assertEqual(next(generator), self.Andy)

            self.Andy.request_action(action)
            with self.subTest('after prompt', action=action):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)


    def test_closing_passive_player(self):

        "Tests prompted player parses a passive action, given there are more players to listen."

        actions = [
            structures.Action(constants.ACTION_CHECK),
            structures.Action(constants.ACTION_CALL, 100),
            structures.Action(constants.ACTION_FOLD),
        ]

        for action in actions:

            self.setUp()
            self.table.set_current_player(self.Andy)
            self.table.set_stopping_player(self.Andy)

            if action.category == constants.ACTION_CALL:
                self.table.set_bet_level(100)
                self.table.set_full_bet_level(100)

            generator = engines.prompt_player(
                table = self.table,
                open_fold_allowed = True,
                raise_invalid_actions = True,
            )

            with self.subTest('before prompt', action=action):
                self.assertEqual(next(generator), self.Andy)

            self.Andy.request_action(action)
            with self.subTest('after prompt', action=action):
                with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
                    next(generator)
                self.assertEqual(context.exception.cause, messages.signal_passive_stopping_player)


    def test_non_closing_agressive_player(self):

        "Tests prompted player parses an aggressive action, given there are more players to listen."

        actions = [
            structures.Action(constants.ACTION_RAISE, 200),
            structures.Action(constants.ACTION_BET, 100),
        ]

        for action in actions:

            self.setUp()
            self.table.set_current_player(self.Andy)

            if action.category == constants.ACTION_RAISE:
                self.table.set_bet_level(100)
                self.table.set_full_bet_level(100)
            else:
                self.table.set_bet_level(0)
                self.table.set_full_bet_level(0)

            generator = engines.prompt_player(
                table = self.table,
                open_fold_allowed = True,
                raise_invalid_actions = True,
            )

            with self.subTest('before prompt', action=action):
                self.assertEqual(next(generator), self.Andy)

            self.Andy.request_action(action)
            with self.subTest('after prompt', action=action):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)


    def test_closing_agressive_player(self):

        "Tests prompted player parses an aggressive action, given there are no more players to listen."

        actions = [
            structures.Action(constants.ACTION_RAISE, 200),
            structures.Action(constants.ACTION_BET, 100),
        ]

        for action in actions:

            self.setUp()
            self.table.set_current_player(self.Andy)
            self.table.set_stopping_player(self.Andy)

            if action.category == constants.ACTION_RAISE:
                self.table.set_bet_level(100)
                self.table.set_full_bet_level(100)
            else:
                self.table.set_bet_level(0)
                self.table.set_full_bet_level(0)

            generator = engines.prompt_player(
                table = self.table,
                open_fold_allowed = True,
                raise_invalid_actions = True,
            )

            with self.subTest('before prompt', action=action):
                self.assertEqual(next(generator), self.Andy)

            self.Andy.request_action(action)
            with self.subTest('after prompt', action=action):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)


    def test_last_remaining_player(self):

        "Tests prompted player cannot parse an action because is the last one remaining in the hand cycle."

        self.table.set_current_player(self.Andy)

        self.Boa.mark_is_folded()
        self.Coral.mark_is_folded()
        self.Dino.mark_is_folded()
        self.Epa.mark_is_folded()
        self.Fomi.mark_is_folded()

        generator = engines.prompt_player(
            table = self.table,
            open_fold_allowed = False,
            raise_invalid_actions = True,
        )

        with self.assertRaises(exceptions.CloseBettingRoundSignal) as context:
            next(generator)
        self.assertEqual(context.exception.cause, messages.signal_last_player_in_hand)


if __name__ == '__main__':
    main()