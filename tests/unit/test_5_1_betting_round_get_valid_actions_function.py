"""
Defines unit tests on action_is_valid function and its helper functions.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class TestImpossibleSituations(TestCase):


    """
    Runs unit tests on get_valid_action_names function when parsed values represent impossible situations.
    """


    def test_negative_inputs(self):

        """
        Runs test cases where negative values are parsed.
        """

        # Negative player stack
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = -1,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 1,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )

        # Negative player current amount
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = -1,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 1,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )

        # Negative current level
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 0,
                player_has_played = False,
                current_level = -1,
                complete_current_level = 0,
                full_bet = 1,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )

        # Negative complete current level
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = -1,
                full_bet = 1,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )

        # Non-positive full bet
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 0,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )

        # Non-positive full raise increase
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 1,
                full_raise_increase = 0,
                open_fold_allowed = False,
            )


    def test_composed_invalid_inputs(self):

        """
        Runs test cases where invalid value combinations are parsed.
        """

        # Full raise increase smaller than full bet
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 2,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )

        # Full raise amount not larger than current level
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 1,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )

        # Current level smaller than complete current level
        with self.assertRaises(AssertionError):
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 1,
                full_bet = 1,
                full_raise_increase = 1,
                open_fold_allowed = False,
            )


class TestGetValidActionNamesFuctionNotFacingAnAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is not facing an
    aggression.
    """


    def test_cannot_afford_a_full_bet(self):

        """
        Runs test cases when the player does not have enough chips to cover a full bet.
        """

        # player has not put money, open fold is not allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(1, 2),
            },
        )

        # player has not put money, open fold is allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = True,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(1, 2),
            },
        )

        # player has placed a big blind, open fold is not allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(1, 2),
            },
        )


        # player has placed a big blind, open fold is allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = True,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(1, 2),
            },
        )


        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(1, 2),
                constants.ACTION_FOLD: range(0, 1),
            },
        )


    def test_can_afford_a_full_bet_but_no_more(self):

        """
        Runs test cases when the player has just enough chips to cover a full bet.
        """

        # player has not put money, open fold is not allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 5),
            },
        )

        # player has not put money, open fold is allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = True,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 5),
            },
        )

        # player has placed a big blind, open fold is not allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 5),
            },
        )

        # player has placed a big blind, open fold is allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = True,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 5),
            },
        )


        # player has placed a small blind and has just enough to call
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 2,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_FOLD: range(0, 1),
            },
        )


    def test_can_afford_more_than_a_full_bet(self):

        """
        Runs test cases when the player has more than enough chips to cover a full bet.
        """

        # player has not put money, open fold is not allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 6,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 7),
            },
        )

        # player has not put money, open fold is allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 6,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 0,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = True,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 7),
            },
        )

        # player has placed a big blind, open fold is not allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 6,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 7),
            },
        )

        # player has placed a big blind, open fold is allowed
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 6,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = True,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_BET: range(4, 7),
            },
        )


        # player has placed a small blind and has more than enough to call but not enough to make a full raise
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_RAISE: range(4, 5),
            },
        )


        # player has placed a small blind and has just enough money to make a full raise
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 6,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_RAISE: range(6, 7),
            },
        )


        # player has placed a small blind and has more than enough money to make a full raise
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 8,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 4,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_RAISE: range(6, 9),
            },
        )


class TestGetValidActionNamesFuctionFacingAnIncompleteAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is facing an
    aggression that is not enough to be considered a full bet or full raise.
    """


    def test_cannot_afford_a_full_call(self):

        """
        Runs test cases when the player does not have enough chips to cover the call amount.
        """

        # player has not put money
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(1, 2),
            },
        )

        # player has placed a big blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(1, 2),
            },
        )

        # player has previously bet or called
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 4,
                player_has_played = True,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(1, 2),
            },
        )

        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 1,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(1, 2),
                constants.ACTION_FOLD: range(0, 1),
            },
        )


    def test_can_afford_a_full_call_but_no_more(self):

        """
        Runs test cases when the player has just enough chips to cover the call amount.
        """

        # player has not put money
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 2,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has placed a big blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 2,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has previously bet or called
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 2,
                player_current_amount = 4,
                player_has_played = True,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(4, 5),
                constants.ACTION_FOLD: range(0, 1),
            },
        )


    def test_can_afford_a_full_call_but_not_to_complete_the_aggression(self):

        """
        Runs test cases when the player has enough chips to make an increment but not to complete
        the full bet or raise.
        """
        
        # player has not put money
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 3,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(3, 4),
            },
        )

        # player has placed a big blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 3,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(3, 4),
            },
        )

        # player has previously bet or called
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 3,
                player_current_amount = 4,
                player_has_played = True,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 5,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(4, 5),
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_RAISE: range(5, 6),
            },
        )


    def test_can_afford_to_complete_the_aggression_but_no_more(self):

        """
        Runs test cases when the player has just enough chips to complete the bet or raise, but not
        to re-raise.
        """

        # player has not put money
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 5),
            },
        )

        # player has placed a big blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 5),
            },
        )

        # player has previously bet or called
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 4,
                player_current_amount = 4,
                player_has_played = True,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 6,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(4, 5),
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_RAISE: range(6, 7),
            },
        )


    def test_can_afford_to_complete_the_aggression_but_not_to_make_a_full_reraise(self):

        """
        Runs test cases when the player has more than enough chips to complete the bet or raise but
        not to make a full re-raise
        """

        # player has not put money
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 5,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 6),
            },
        )

        # player has placed a big blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 5,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 6),
            },
        )

        # player has previously bet or called
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 5,
                player_current_amount = 4,
                player_has_played = True,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 7,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(4, 5),
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_RAISE: range(6, 8),
            },
        )


    def test_can_afford_make_a_full_reraise_but_no_more(self):

        """
        Runs test cases when the player has just enough chips to complete a full re-raise.
        """

        # player has not put money
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 8,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 9),
            },
        )

        # player has placed a big blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 8,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 9),
            },
        )

        # player has previously bet or called
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 8,
                player_current_amount = 4,
                player_has_played = True,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 10,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(4, 5),
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_RAISE: range(6, 11),
            },
        )


    def test_can_afford_make_a_full_reraise_and_more(self):

        """
        Runs test cases when the player has more than enough chips to complete a full re-raise.
        """

        # player has not put money
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 100,
                player_current_amount = 0,
                player_has_played = False,
                current_level = 2,
                complete_current_level = 0,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 101),
            },
        )

        # player has placed a big blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 100,
                player_current_amount = 4,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
                constants.ACTION_BET: range(4, 101),
            },
        )

        # player has previously bet or called
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 100,
                player_current_amount = 4,
                player_has_played = True,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(2, 3),
            },
        )

        # player has placed a small blind
        self.assertDictEqual(
            engines.get_valid_actions(
                player_stack = 100,
                player_current_amount = 2,
                player_has_played = False,
                current_level = 6,
                complete_current_level = 4,
                full_bet = 4,
                full_raise_increase = 4,
                open_fold_allowed = False,
            ),
            {
                constants.ACTION_CALL: range(4, 5),
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_RAISE: range(6, 100),
            },
        )


if __name__ == '__main__':
    main()