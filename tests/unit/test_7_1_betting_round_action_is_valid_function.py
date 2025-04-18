"""
Defines unit tests on action_is_valid function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, structures


class TestBettingRoundActionIsValidFunction(TestCase):


    """
    Runs unit tests on get_valid_action_names and action_is_valid functions.
    """


    def test_get_valid_action_names(self):

        """
        Runs test cases on function get_valid_action_names.
        """

        self.assertListEqual(
            sorted(managers.get_valid_action_names(amount_to_call=0, open_fold_allowed=True)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CHECK, constants.ACTION_BET])
        )

        self.assertListEqual(
            sorted(managers.get_valid_action_names(amount_to_call=0, open_fold_allowed=False)),
            sorted([constants.ACTION_CHECK, constants.ACTION_BET])
        )

        self.assertListEqual(
            sorted(managers.get_valid_action_names(amount_to_call=10, open_fold_allowed=True)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CALL, constants.ACTION_RAISE])
        )

        self.assertListEqual(
            sorted(managers.get_valid_action_names(amount_to_call=10, open_fold_allowed=False)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CALL, constants.ACTION_RAISE])
        )


    def test_actions_if_nobody_has_bet_and_folding_is_allowed(self):

        """
        Runs test cases where nobody has bet and folding is allowed.
        """

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]

        table = structures.Table(
            all_players,
            smallest_chip = 10,
            smallest_bet = 50,
            open_fold_allowed = True
        )

        # Valid actions

        action = structures.Action(constants.ACTION_FOLD)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_CHECK)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_BET, 100)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their names

        action = structures.Action(constants.ACTION_CALL, 100)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_RAISE, 100)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their amounts

        # Betting amount smaller than the smallest chip
        action = structures.Action(constants.ACTION_BET, 5)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Betting amount smaller than the smallest bet
        action = structures.Action(constants.ACTION_BET, 40)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


    def test_actions_if_nobody_has_bet_and_folding_is_forbidden(self):

        """
        Runs test cases where nobody has bet and folding is forbidden.
        """

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]

        table = structures.Table(
            all_players,
            smallest_chip = 10,
            smallest_bet = 50,
            open_fold_allowed = False
        )


        # Valid actions

        action = structures.Action(constants.ACTION_CHECK)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_BET, 50)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_BET, 60)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their names

        action = structures.Action(constants.ACTION_FOLD)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_CALL, 100)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_RAISE, 100)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their amounts

        # Betting more than the smallest bet but not a multiple of the smallest chip
        action = structures.Action(constants.ACTION_BET, 55)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Betting an amount smaller than the smallest bet
        action = structures.Action(constants.ACTION_BET, 40)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


    def test_actions_to_answer_a_bet(self):

        """
        Runs test cases where you have checked or not played yet, one player bets afterwards, and now you have to play again.
        """

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]

        table = structures.Table(
            all_players,
            smallest_chip = 10,
            smallest_bet = 50,
            open_fold_allowed = False
        )

        table.add_to_current_amount(60) # Someone bets 60
        table.overwrite_smallest_rising_amount(60) # The bet of +60


        # Valid actions

        action = structures.Action(constants.ACTION_FOLD)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_CALL, 60) # Andy has not put money yet
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_RAISE, 120) # Smallest valid raise (60 to call plus 60 to raise)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_RAISE, 130) # Larger raise
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their names

        action = structures.Action(constants.ACTION_CHECK)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_BET, 50)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their amounts

        # Calling less than calling amount
        action = structures.Action(constants.ACTION_CALL, 50)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Calling more than calling amount
        action = structures.Action(constants.ACTION_CALL, 70)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising less than calling amount
        action = structures.Action(constants.ACTION_RAISE, 50)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising the calling amount
        action = structures.Action(constants.ACTION_RAISE, 60)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising more than the calling amount but less than the smallest rising amount
        action = structures.Action(constants.ACTION_RAISE, 110)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising more than the smallest rising amount but not a multiple of the smallest chip
        action = structures.Action(constants.ACTION_RAISE, 125)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


    def test_actions_to_answer_a_single_raise(self):

        """
        Runs test cases where you have bet or called, one player has raised afterwards, and now you have to play again.
        """

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]

        table = structures.Table(
            all_players,
            smallest_chip = 10,
            smallest_bet = 50,
            open_fold_allowed = False
        )

        Andy.add_to_current_amount(60) # Andy bets or calls 60
        table.add_to_current_amount(130) # Someone raises to 130 (+70)
        table.overwrite_smallest_rising_amount(70) # The raise of +70


        # Valid actions

        action = structures.Action(constants.ACTION_FOLD)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_CALL, 70) # Andy already put an amount of 60
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_RAISE, 140) # Smallest valid raise (70 to call plus 70 to raise)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_RAISE, 150) # Larger raise
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their names

        action = structures.Action(constants.ACTION_CHECK)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_BET, 50)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their amounts

        # Calling less than calling amount
        action = structures.Action(constants.ACTION_CALL, 60)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Calling more than calling amount
        action = structures.Action(constants.ACTION_CALL, 80)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising less than calling amount
        action = structures.Action(constants.ACTION_RAISE, 60)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising the calling amount
        action = structures.Action(constants.ACTION_RAISE, 70)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising more than the calling amount but less than the smallest rising amount
        action = structures.Action(constants.ACTION_RAISE, 130)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising more than the smallest rising amount but not a multiple of the smallest chip
        action = structures.Action(constants.ACTION_RAISE, 145)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


    def test_actions_to_answer_multiple_raises(self):

        """
        Runs test cases where you have bet or called, multiple players have raised afterwards, and now you have to play again.
        """

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]

        table = structures.Table(
            all_players,
            smallest_chip = 10,
            smallest_bet = 50,
            open_fold_allowed = False
        )

        Andy.add_to_current_amount(60) # Andy bets or calls 60
        table.add_to_current_amount(200) # Someone raises to 120 (+60), and someone else to 200 (+80)
        table.overwrite_smallest_rising_amount(80) # The second raise of +80


        # Valid actions

        action = structures.Action(constants.ACTION_FOLD)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_CALL, 140) # Andy already put an amount of 60
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))
        
        action = structures.Action(constants.ACTION_RAISE, 220) # Smallest valid raise (140 to call plus 80 to raise)
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_RAISE, 230) # Larger raise
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their names

        action = structures.Action(constants.ACTION_CHECK)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        action = structures.Action(constants.ACTION_BET, 50)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


        # Invalid actions because of their amounts

        # Calling less than calling amount
        action = structures.Action(constants.ACTION_CALL, 130)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Calling more than calling amount
        action = structures.Action(constants.ACTION_CALL, 150)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising less than calling amount
        action = structures.Action(constants.ACTION_RAISE, 130)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising the calling amount
        action = structures.Action(constants.ACTION_RAISE, 140)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising more than the calling amount but less than the smallest rising amount
        action = structures.Action(constants.ACTION_RAISE, 210)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))

        # Raising more than the smallest rising amount but not a multiple of the smallest chip
        action = structures.Action(constants.ACTION_RAISE, 225)
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=action))


if __name__ == '__main__':
    main()