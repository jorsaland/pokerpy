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

        # Define actions

        fold = structures.Action(constants.ACTION_FOLD)
        check = structures.Action(constants.ACTION_CHECK)
        call = structures.Action(constants.ACTION_CALL, 100)
        bet = structures.Action(constants.ACTION_BET, 100)
        raise_ = structures.Action(constants.ACTION_RAISE, 100)

        # Define table and current player

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]
        table = structures.Table(all_players, open_fold_allowed=True)

        # Valid actions
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=fold))
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=check))
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=bet))

        # Invalid actions
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=call))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=raise_))


    def test_actions_if_nobody_has_bet_and_folding_is_forbidden(self):

        """
        Runs test cases where nobody has bet and folding is forbidden.
        """

        # Define actions

        fold = structures.Action(constants.ACTION_FOLD)
        check = structures.Action(constants.ACTION_CHECK)
        call = structures.Action(constants.ACTION_CALL, 100)
        bet = structures.Action(constants.ACTION_BET, 100)
        raise_ = structures.Action(constants.ACTION_RAISE, 100)

        # Define table and current player

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]
        table = structures.Table(all_players, open_fold_allowed=False)

        # Valid actions
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=check))
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=bet))

        # Invalid actions
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=fold))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=call))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=raise_))


    def test_actions_to_answer_a_bet(self):

        """
        Runs test cases where someone else has bet and you have to answer.
        """

        # Define actions

        fold = structures.Action(constants.ACTION_FOLD)
        check = structures.Action(constants.ACTION_CHECK)
        call = structures.Action(constants.ACTION_CALL, 100)
        bet = structures.Action(constants.ACTION_BET, 100)
        raise_ = structures.Action(constants.ACTION_RAISE, 200)
        bad_raise_zero = structures.Action(constants.ACTION_RAISE, 100)
        bad_raise_negative = structures.Action(constants.ACTION_RAISE, 50)

        # Define table and current player

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]
        table = structures.Table(all_players)

        # Make the table to have an amount to be answered
        table.add_to_current_amount(100)

        # Valid actions
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=fold))
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=call))
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=raise_))

        # Invalid actions
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=check))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=bet))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=bad_raise_zero))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=bad_raise_negative))


    def test_actions_to_answer_a_raise(self):

        """
        Runs test cases where someone else raised a bet that you previously made or called, and now you have to answer.
        """

        # Define actions

        fold = structures.Action(constants.ACTION_FOLD)
        check = structures.Action(constants.ACTION_CHECK)
        call = structures.Action(constants.ACTION_CALL, 100)
        bet = structures.Action(constants.ACTION_BET, 100)
        raise_ = structures.Action(constants.ACTION_RAISE, 200)
        bad_raise_zero = structures.Action(constants.ACTION_RAISE, 100)
        bad_raise_negative = structures.Action(constants.ACTION_RAISE, 50)

        # Define table and current player

        all_players = [
            (Andy := structures.Player('Andy')),
            structures.Player('Boa'),
            structures.Player('Coral'),
            structures.Player('Dino'),
        ]
        table = structures.Table(all_players)

        # Make the table to have an amount to be answered, higher than player's amount
        table.add_to_current_amount(200)
        Andy.add_to_current_amount(100)

        # Valid actions
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=fold))
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=call))
        self.assertTrue(managers.action_is_valid(table=table, player=Andy, action=raise_))

        # Invalid actions
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=check))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=bet))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=bad_raise_zero))
        self.assertFalse(managers.action_is_valid(table=table, player=Andy, action=bad_raise_negative))


if __name__ == '__main__':
    main()