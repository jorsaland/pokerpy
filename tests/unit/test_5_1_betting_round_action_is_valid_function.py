"""
Defines unit tests on action_is_valid function and its helper functions.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class TestBettingRoundGetValidActionNamesFuction(TestCase):


    """
    Runs unit tests on get_valid_action_names function.
    """


    def test_not_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is not facing a bet or a raise.
        """

        # Open fold is allowed
        self.assertListEqual(
            sorted(engines.get_valid_action_names(amount_to_call=0, stack=10, open_fold_allowed=True)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CHECK, constants.ACTION_BET])
        )

        # Open fold is not allowed
        self.assertListEqual(
            sorted(engines.get_valid_action_names(amount_to_call=0, stack=10, open_fold_allowed=False)),
            sorted([constants.ACTION_CHECK, constants.ACTION_BET])
        )


    def test_not_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is facing a bet or a raise.
        """

        # Player has enough chips and open fold is allowed
        self.assertListEqual(
            sorted(engines.get_valid_action_names(amount_to_call=1, stack=10, open_fold_allowed=True)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CALL, constants.ACTION_RAISE])
        )

        # Player has enough chips and open fold is not allowed
        self.assertListEqual(
            sorted(engines.get_valid_action_names(amount_to_call=1, stack=10, open_fold_allowed=False)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CALL, constants.ACTION_RAISE])
        )

        # Player does not have enough chips and open fold is allowed
        self.assertListEqual(
            sorted(engines.get_valid_action_names(amount_to_call=20, stack=10, open_fold_allowed=True)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CALL])
        )

        # Player does not have enough chips and open fold is not allowed
        self.assertListEqual(
            sorted(engines.get_valid_action_names(amount_to_call=20, stack=10, open_fold_allowed=False)),
            sorted([constants.ACTION_FOLD, constants.ACTION_CALL])
        )    


class TestBettingRoundActionIsValidFunctionWhenActionIsFold(TestCase):


    """
    Runs unit tests on function action_is_valid when the requested action is fold.
    """


    def test_not_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is not facing a bet or a raise.
        """

        # Open fold (allowed) not facing a bet
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_FOLD),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = True
        ))

        # Open fold (allowed) not facing a bet, but having previously placed a blind bet
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_FOLD),
            table_current_amount = 1,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = True
        ))

        # Open fold (forbidden) not facing a bet
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_FOLD),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))

        # Open fold (forbidden) not facing a bet, but having previously placed a blind bet
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_FOLD),
            table_current_amount = 1,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))


    def test_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is facing a bet or a raise.
        """

        # Facing a bet
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_FOLD),
            table_current_amount = 1,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))

        # Facing a raise
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_FOLD),
            table_current_amount = 2,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))


class TestBettingRoundActionIsValidFunctionWhenActionIsCheck(TestCase):


    """
    Runs unit tests on function action_is_valid when the requested action is check.
    """


    def test_not_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is not facing a bet or a raise.
        """

        # Not facing a bet
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CHECK),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))

        # Not facing a raise, having previously placed a blind bet
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CHECK),
            table_current_amount = 1,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))


    def test_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is facing a bet or a raise.
        """

        # Facing a bet
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CHECK),
            table_current_amount = 1,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))

        # Facing a raise
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CHECK),
            table_current_amount = 2,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))


class TestBettingRoundActionIsValidFunctionWhenActionIsCall(TestCase):


    """
    Runs unit tests on function action_is_valid when the requested action is call.
    """


    def test_not_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is not facing a bet or a raise.
        """

        # Not facing a bet
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 1),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))

        # Not facing a raise
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 1),
            table_current_amount = 3,
            player_current_amount = 3,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))


    def test_facing_a_bet_with_enough_chips_to_call(self):

        """
        Runs test cases when the player is facing a bet and has enough chips to call.
        """

        # Attempting to call less than the call amount (2)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 1),
            table_current_amount = 2,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Calling the call amount (2)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 2),
            table_current_amount = 2,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Attempting to call more than call amount (2)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 3),
            table_current_amount = 2,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))


    def test_facing_a_bet_without_enough_chips_to_call(self):

        """
        Runs test cases when the player is facing a bet and does not have enough chips to call.
        """

        # Attempting to call less than the all-in amount (10)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 9),
            table_current_amount = 12,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Going all-in (10) (PENDING IMPLEMENTATION)
        # self.assertTrue(engines.action_is_valid(
        #     action = structures.Action(constants.ACTION_CALL, 10),
        #     table_current_amount = 12,
        #     player_current_amount = 0,
        #     player_stack = 10,
        #     smallest_bet_amount = 1,
        #     smallest_raise_amount = 12,
        #     open_fold_allowed = False
        # ))

        # Attempting to call more than the all-in amount (10) and less than the call amount (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 11),
            table_current_amount = 12,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to call the call amount (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 12),
            table_current_amount = 12,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to call more than the call amount (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 13),
            table_current_amount = 12,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))


    def test_facing_a_raise_with_enough_chips_to_call(self):

        """
        Runs test cases when the player is facing a raise and has enough chips to call.
        """

        # Attempting to call less than call amount (2)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 1),
            table_current_amount = 3,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Calling the call amount (2)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 2),
            table_current_amount = 3,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Attempting to call more than call amount (2)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 3),
            table_current_amount = 3,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))


    def test_facing_a_raise_without_enough_chips_to_call(self):

        """
        Runs test cases when the player is facing a raise and does not have enough chips to call.
        """

        # Attempting to call less than the all-in amount (10)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 9),
            table_current_amount = 13,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Going all-in (10) (PENDING IMPLEMENTATION)
        # self.assertTrue(engines.action_is_valid(
        #     action = structures.Action(constants.ACTION_CALL, 10),
        #     table_current_amount = 13,
        #     player_current_amount = 1,
        #     player_stack = 10,
        #     smallest_bet_amount = 1,
        #     smallest_raise_amount = 12,
        #     open_fold_allowed = False
        # ))

        # Attempting to call more than the all-in amount (10) and less than the call amount (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 11),
            table_current_amount = 13,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to call the call amount (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 12),
            table_current_amount = 13,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to call more than the call amount (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_CALL, 13),
            table_current_amount = 13,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))


class TestBettingRoundActionIsValidFunctionWhenActionIsBet(TestCase):


    """
    Runs unit tests on function action_is_valid when the requested action is bet.
    """


    def test_not_facing_a_bet_with_enough_chips_to_bet(self):

        """
        Runs test cases when the player is not facing a bet and has enough chips to make a full
        bet.
        """

        # Attempting to bet less than a full bet (2)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 1),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Betting a full bet (2)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 2),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Betting more than a full bet (2)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 3),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))


    def test_not_facing_a_bet_without_enough_chips_to_bet(self):

        """
        Runs test cases when the player is not facing a bet or a raise and does not have enough
        chips to make a full bet.
        """

        # Attempting to bet less than the all-in amount (10)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 9),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Going all-in (10)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 10),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to bet more than the all-in amount (10) and less than a full bet (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 11),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to bet a full bet (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 12),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to bet more than a full bet (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 13),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))


    def test_not_facing_a_raise_with_enough_chips_to_bet(self):

        """
        Runs test cases when the player made a blind bet, is not facing a raise and has enough chips to make a full
        bet, having placed a blind bet before.
        """

        # Attempting to bet less than a full bet (2)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 1),
            table_current_amount = 2,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Betting a full bet (2)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 2),
            table_current_amount = 2,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))

        # Betting more than a full bet (2)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 3),
            table_current_amount = 2,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 2,
            open_fold_allowed = False
        ))


    def test_not_facing_a_raise_without_enough_chips_to_bet(self):

        """
        Runs test cases when the player made a blind bet, is not facing a raise and does not have enough
        chips to make a full bet.
        """

        # Attempting to bet less than the all-in amount (10)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 9),
            table_current_amount = 12,
            player_current_amount = 12,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Going all-in (10)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 10),
            table_current_amount = 12,
            player_current_amount = 12,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to bet more than the all-in amount (10) and less than a full bet (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 11),
            table_current_amount = 12,
            player_current_amount = 12,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to bet a full bet (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 12),
            table_current_amount = 12,
            player_current_amount = 12,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))

        # Attempting to bet more than a full bet (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 13),
            table_current_amount = 12,
            player_current_amount = 12,
            player_stack = 10,
            smallest_bet_amount = 12,
            smallest_raise_amount = 12,
            open_fold_allowed = False
        ))


    def test_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is facing a bet or a raise.
        """

        # Facing a bet
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 1),
            table_current_amount = 1,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))

        # Facing a raise
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_BET, 1),
            table_current_amount = 2,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))


class TestBettingRoundActionIsValidFunctionWhenActionIsRaise(TestCase):


    """
    Runs unit tests on function action_is_valid when the requested action is raise.
    """


    def test_not_facing_a_bet_or_raise(self):

        """
        Runs test cases when the player is not facing a bet or a raise.
        """

        # Not facing a bet
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 1),
            table_current_amount = 0,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))

        # Not facing a raise
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 1),
            table_current_amount = 1,
            player_current_amount = 1,
            player_stack = 10,
            smallest_bet_amount = 1,
            smallest_raise_amount = 1,
            open_fold_allowed = False
        ))


    def test_facing_a_bet_with_enough_chips_to_raise(self):

        """
        Runs test cases when the player is facing a bet and has enough chips to make a full raise.
        """

        # Attempting to raise less than a full raise (+3)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 7),
            table_current_amount = 5,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 3,
            open_fold_allowed = False
        ))

        # Raising a full raise (+3)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 8),
            table_current_amount = 5,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 3,
            open_fold_allowed = False
        ))

        # Raising more than a full raise (+3)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 9),
            table_current_amount = 5,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 3,
            open_fold_allowed = False
        ))


    def test_facing_a_bet_without_enough_chips_to_raise(self):

        """
        Runs test cases when the player is facing a bet and does not have enough chips to make a
        full raise.
        """

        # Attempting to raise less than the all-in amount (10)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 9),
            table_current_amount = 6,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Going all-in (10)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 10),
            table_current_amount = 6,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Attempting to raise more than the all-in amount (10) and less than a full raise (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 11),
            table_current_amount = 6,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Attempting a full raise (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 12),
            table_current_amount = 6,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Attempting to raise more than a full raise (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 13),
            table_current_amount = 6,
            player_current_amount = 0,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))


    def test_facing_a_raise_with_enough_chips_to_raise(self):

        """
        Runs test cases when the player is facing a bet and has enough chips to make a full raise.
        """

        # Attempting to raise less than a full raise (+3)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 5),
            table_current_amount = 5,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 3,
            open_fold_allowed = False
        ))

        # Raising a full raise (+3)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 6),
            table_current_amount = 5,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 3,
            open_fold_allowed = False
        ))

        # Raising more than a full raise (+3)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 7),
            table_current_amount = 5,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 3,
            open_fold_allowed = False
        ))


    def test_facing_a_raise_without_enough_chips_to_raise(self):

        """
        Runs test cases when the player is facing a raise and does not have enough chips to make a
        full raise.
        """

        # Attempting to raise less than the all-in amount (10)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 9),
            table_current_amount = 8,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Going all-in (10)
        self.assertTrue(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 10),
            table_current_amount = 8,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Attempting to raise more than the all-in amount (10) and less than a full raise (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 11),
            table_current_amount = 8,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Attempting a full raise (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 12),
            table_current_amount = 8,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))

        # Attempting to raise more than a full raise (12)
        self.assertFalse(engines.action_is_valid(
            action = structures.Action(constants.ACTION_RAISE, 13),
            table_current_amount = 8,
            player_current_amount = 2,
            player_stack = 10,
            smallest_bet_amount = 2,
            smallest_raise_amount = 6,
            open_fold_allowed = False
        ))


if __name__ == '__main__':
    main()