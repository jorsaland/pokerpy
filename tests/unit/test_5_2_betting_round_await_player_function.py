"""
Defines unit tests on await_player function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, messages, structures


class TestBettingRoundAwaitPlayerFunction(TestCase):


    """
    Runs unit tests on await_player function.
    """


    def test_parse_a_valid_action(self):

        """
        Runs test cases where a valid action is parsed.
        """
        
        players = [
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ]

        table = structures.Table(players)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet = 2,
            smallest_raising_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = False,
        )

        # Evaluate states before request

        player = next(generator)
        self.assertIsNone(player.requested_action)

        # Evaluate states after request

        player.request_action(action)
        self.assertEqual(player.requested_action, action)

        # Evaluate next states

        try:
            next(generator)
        except StopIteration as ex:
            generator_ended = True
            return_value = ex.value
        else:
            generator_ended = False
            return_value = None

        self.assertTrue(generator_ended)
        self.assertEqual(return_value, action)
        self.assertIsNone(player.requested_action)


    def test_soft_parse_an_invalid_action(self):

        """
        Runs test cases where an invalid action is parsed, with the generator set to ignore it.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet = 2,
            smallest_raising_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = True,
        )

        # Evaluate states before request

        player = next(generator)
        self.assertIsNone(player.requested_action)

        # Evaluate states after request

        player.request_action(action)
        self.assertEqual(player.requested_action, action)

        # Evaluate next states

        try:
            next(generator)
        except StopIteration:
            generator_ended = True
        else:
            generator_ended = False

        self.assertFalse(generator_ended)
        self.assertEqual(player.requested_action, action)


    def test_hard_parse_an_invalid_action(self):

        """
        Runs test cases where an invalid action is parsed, with the generator set to raise an error.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CHECK)

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet = 2,
            smallest_raising_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = False,
        )

        # Evaluate states before request

        player = next(generator)
        self.assertIsNone(player.requested_action)

        # Evaluate states after request

        player.request_action(action)
        self.assertEqual(player.requested_action, action)

        # Evaluate next states

        with self.assertRaises(RuntimeError) as context:
            next(generator)

        self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
        self.assertEqual(player.requested_action, action)


    def test_soft_parse_multiple_invalid_actions(self):

        """
        Runs test cases where multiple invalid actions are parsed (with the generator set to ignore them).
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        actions = [
            structures.Action(constants.ACTION_CHECK),
            structures.Action(constants.ACTION_CALL, 1),
            structures.Action(constants.ACTION_RAISE, 1),
        ]

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet = 2,
            smallest_raising_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = True,
        )

        # Evaluate states after actions

        for action in actions:
            player = next(generator)
            player.request_action(action)
            self.assertEqual(player.requested_action, action)

        # Evaluate final states

        try:
            next(generator)
        except StopIteration:
            generator_ended = True
        else:
            generator_ended = False

        self.assertFalse(generator_ended)


    def test_soft_parse_multiple_invalid_actions_and_a_valid_action(self):

        """
        Runs test cases where multiple invalid actions are parsed (with the generator set to ignore them) and finally a valid action is parsed.
        """
        
        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])
        table.add_to_current_amount(2)

        actions = [
            structures.Action(constants.ACTION_CHECK),
            structures.Action(constants.ACTION_CALL, 1),
            structures.Action(constants.ACTION_FOLD),
        ]

        generator = managers.await_player(
            player = Andy,
            table_current_amount = table.current_amount,
            smallest_bet = 2,
            smallest_raising_amount = 2,
            open_fold_allowed = False,
            ignore_invalid_actions = True,
        )

        # Evaluate states after actions

        for action in actions:
            player = next(generator)
            player.request_action(action)
            self.assertEqual(player.requested_action, action)

        # Evaluate final states

        try:
            next(generator)
        except StopIteration as ex:
            generator_ended = True
            return_value = ex.value
        else:
            generator_ended = False
            return_value = None

        self.assertTrue(generator_ended)
        self.assertEqual(return_value, actions[-1])
        self.assertIsNone(player.requested_action)


if __name__ == '__main__':
    main()