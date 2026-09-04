"""
Defines unit tests on action_is_valid function and its helper functions.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines


class TestImpossibleSituations(TestCase):


    """
    Runs unit tests on get_valid_action_names function when parsed input represent impossible situations.
    """


    def test_invalid_negative_inputs(self):

        "Test parsed negative values."

        with self.subTest('negative player stack'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = -1,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 1,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative player amount'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = -1,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 1,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative bet level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = -1,
                    full_bet_level = 0,
                    min_bet = 1,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative full bet level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = -1,
                    min_bet = 1,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative minimum bet'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = -1,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('zero minimum bet'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 0,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative minimum raise increase'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 1,
                    min_raise_increase = -1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('zero minimum raise increase'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 1,
                    min_raise_increase = 0,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )


    def test_composed_invalid_inputs(self):

        "Tests parsed invalid combinations."

        with self.subTest('minimum raise increase smaller than minimum bet'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 2,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('minimum raise expected level not larger than current bet level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 1,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('bet level smaller than full current level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 1,
                    min_bet = 1,
                    min_raise_increase = 1,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                )


class TestNotFacingAnAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is not facing an
    aggression.
    """


    def test_not_facing_aggression_cannot_afford_a_full_bet(self):

        "Tests player not having enough chips to cover a full bet."

        with self.subTest('player has not placed money, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(1, 2),
                },
            )

        with self.subTest('player has not placed money, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(1, 2),
                },
            )

        with self.subTest('player has placed a small blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 2,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(1, 2),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(1, 2),
                },
            )

        with self.subTest('player has placed a big blind, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(1, 2),
                },
            )


    def test_not_facing_aggression_can_afford_a_full_bet_but_no_more(self):

        "Tests players having just enough chips to cover a full bet."

        with self.subTest('player has not placed money, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 5),
                },
            )

        with self.subTest('player has not placed money, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 5),
                },
            )

        with self.subTest('player has placed a small blind and has just enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 2,
                    player_bet_level = 2,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 4,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 5),
                },
            )

        with self.subTest('player has placed a big blind, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 4,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 5),
                },
            )


    def test_not_facing_aggression_can_afford_more_than_a_full_bet(self):

        "Tests cases when the player has more than enough chips to cover a full bet."

        with self.subTest('player has not placed money, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 101),
                },
            )

        with self.subTest('player has not placed money, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 101),
                },
            )

        with self.subTest('player has placed a small blind and has more than enough to call but not enough to make a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 2,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_RAISE: range(4, 5),
                },
            )

        with self.subTest('player has placed a small blind and has just enough money to make a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 2,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has placed a small blind and has more than enough money to make a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 2,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_RAISE: range(6, 101),
                },
            )

        with self.subTest('player has placed a big blind, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 101),
                },
            )

        with self.subTest('player has placed a big blind, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(4, 101),
                },
            )


class TestFacingAnIncompleteAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is facing an
    aggression that is not enough to be considered a full bet or full raise.
    """


    def test_facing_incomplete_aggression_cannot_afford_a_full_call(self):

        "Tests player not having enough chips to cover the call amount."

        with self.subTest('player has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has placed a small blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(1, 2),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 5,
                    bet_level = 7,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 8,
                    bet_level = 10,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 9,
                    bet_level = 11,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )


    def test_facing_incomplete_aggression_can_afford_a_full_call_but_no_more(self):

        "Tests player having just enough chips to cover the call amount."

        with self.subTest('player has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 2,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has placed a small blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 2,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 2,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 2,
                    player_bet_level = 5,
                    bet_level = 7,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 2,
                    player_bet_level = 8,
                    bet_level = 10,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 2,
                    player_bet_level = 9,
                    bet_level = 11,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )


    def test_facing_incomplete_aggression_can_afford_a_full_call_but_not_to_complete_the_aggression(self):

        "Test player having enough chips to make an increment but not to complete the full bet or raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(3, 4),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(5, 6),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(3, 4),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 5,
                    bet_level = 7,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 8,
                    bet_level = 10,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 3,
                    player_bet_level = 9,
                    bet_level = 11,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )


    def test_facing_incomplete_aggression_can_afford_to_complete_the_aggression_but_no_more(self):

        "Tests player having just enough chips to complete the bet or raise, but not to re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 5),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 5),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 5,
                    bet_level = 7,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 8,
                    bet_level = 10,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 9,
                    bet_level = 11,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )


    def test_facing_incomplete_aggression_can_afford_to_complete_the_aggression_but_not_to_make_a_full_reraise(self):

        "Tests player having more than enough chips to complete the bet or raise but not to make a full re-raise"

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 6),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(6, 8),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 6),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 5,
                    bet_level = 7,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 8,
                    bet_level = 10,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 9,
                    bet_level = 11,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )


    def test_facing_incomplete_aggression_can_afford_make_a_full_reraise_but_no_more(self):

        "Tests player having just enough chips to complete a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 9),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(6, 11),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 9),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 5,
                    bet_level = 7,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 8,
                    bet_level = 10,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 9,
                    bet_level = 11,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )


    def test_facing_incomplete_aggression_can_afford_make_a_full_reraise_and_more(self):

        "Tests player having more than enough chips to complete a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 101),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 2,
                    full_bet_level = 0,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(6, 101),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 2,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                    constants.ACTION_BET: range(4, 101),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 6,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 5,
                    bet_level = 7,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 8,
                    bet_level = 10,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 9,
                    bet_level = 11,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(2, 3),
                },
            )


class TestFacingACompleteAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is facing a
    full bet or a full raise but no more than that.
    """


    def test_facing_complete_aggression_cannot_afford_a_full_call(self):

        "Tests player not having enough chips to cover the call amount."

        with self.subTest('player has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has placed a small blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(1, 2),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )


    def test_facing_complete_aggression_can_afford_a_full_call_but_no_more(self):

        "Tests player having just enough chips to cover the call amount."

        with self.subTest('player has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has placed a small blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 4,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )


    def test_facing_complete_aggression_can_afford_to_call_but_not_to_make_a_full_reraise(self):

        "Tests player having more than enough chips to complete the bet or raise but not to make a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(5, 6),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(7, 8),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(5, 6),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called a full bet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full bet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overbet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called an overbet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full raise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full raise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overraise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called an overraise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )


    def test_facing_complete_aggression_can_afford_make_a_full_reraise_but_no_more(self):

        "Tests player having just enough chips to complete a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 9),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(10, 11),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 9),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called a full bet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 9),
                },
            )

        with self.subTest('player has previously opened or called a full bet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overbet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 11),
                },
            )

        with self.subTest('player has previously opened or called an overbet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full raise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 9),
                },
            )

        with self.subTest('player has previously opened or called a full raise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overraise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 11),
                },
            )

        with self.subTest('player has previously opened or called an overraise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )


    def test_facing_complete_aggression_can_afford_make_a_full_reraise_and_more(self):

        "Tests player having more than enough chips to complete a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 101),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 4,
                    full_bet_level = 4,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(10, 101),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 2,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 101),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called a full bet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 101),
                },
            )

        with self.subTest('player has previously opened or called a full bet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 8,
                    full_bet_level = 8,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overbet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 101),
                },
            )

        with self.subTest('player has previously opened or called an overbet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 5,
                    bet_level = 10,
                    full_bet_level = 10,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full raise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                    constants.ACTION_RAISE: range(8, 101),
                },
            )

        with self.subTest('player has previously opened or called a full raise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 8,
                    bet_level = 12,
                    full_bet_level = 12,
                    min_bet = 4,
                    min_raise_increase = 4,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(4, 5),
                },
            )

        with self.subTest('player has previously opened or called an overraise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 101),
                },
            )

        with self.subTest('player has previously opened or called an overraise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 9,
                    bet_level = 14,
                    full_bet_level = 14,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )


class TestFacingAnOverAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is facing an
    overbet or an overraise.
    """


    def test_facing_over_aggression_cannot_afford_a_full_call(self):

        "Tests player not having enough chips to cover the call amount."

        with self.subTest('player has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has placed a small blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(1, 2),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(1, 2),
                },
            )


    def test_facing_over_aggression_can_afford_a_full_call_but_no_more(self):

        "Tests player having just enough chips to cover the call amount."

        with self.subTest('player has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has placed a small blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(7, 8),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 5,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )


    def test_facing_over_aggression_can_afford_to_call_but_not_to_make_a_full_reraise(self):

        "Tests player having more than enough chips to complete the bet or raise but not to make a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(7, 8),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(8, 9),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 8,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(7, 8),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full bet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called a full bet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overbet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_RAISE: range(7, 8),
                },
            )

        with self.subTest('player has previously opened or called an overbet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called a full raise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called a full raise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 6,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overraise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_RAISE: range(7, 8),
                },
            )

        with self.subTest('player has previously opened or called an overraise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 7,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )


    def test_facing_over_aggression_can_afford_make_a_full_reraise_but_no_more(self):

        "Tests player having just enough chips to complete a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 11),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 12,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(7, 8),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(12, 13),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 12,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(7, 8),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 11),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full bet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 11),
                },
            )

        with self.subTest('player has previously opened or called a full bet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overbet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 12,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_RAISE: range(12, 13),
                },
            )

        with self.subTest('player has previously opened or called an overbet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 12,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called a full raise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 11),
                },
            )

        with self.subTest('player has previously opened or called a full raise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 10,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overraise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 12,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_RAISE: range(12, 13),
                },
            )

        with self.subTest('player has previously opened or called an overraise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 12,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = True,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )


    def test_facing_over_aggression_can_afford_make_a_full_reraise_and_more(self):

        "Tests player having more than enough chips to complete a full re-raise."

        with self.subTest('player has not placed money and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 101),
                },
            )

        with self.subTest('player has not placed money and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 5,
                    full_bet_level = 5,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has placed a small blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(7, 8),
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_RAISE: range(12, 101),
                },
            )

        with self.subTest('player has placed a small blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 2,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(7, 8),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('player has placed a big blind and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 101),
                },
            )

        with self.subTest('player has placed a big blind and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called a full bet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 101),
                },
            )

        with self.subTest('player has previously opened or called a full bet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 4,
                    bet_level = 9,
                    full_bet_level = 9,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overbet and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_RAISE: range(12, 101),
                },
            )

        with self.subTest('player has previously opened or called an overbet and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 5,
                    bet_level = 11,
                    full_bet_level = 11,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )

        with self.subTest('player has previously opened or called a full raise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                    constants.ACTION_RAISE: range(10, 101),
                },
            )

        with self.subTest('player has previously opened or called a full raise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 8,
                    bet_level = 13,
                    full_bet_level = 13,
                    min_bet = 4,
                    min_raise_increase = 5,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(5, 6),
                },
            )

        with self.subTest('player has previously opened or called an overraise and there are more active players'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = False,
                    is_last_active_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                    constants.ACTION_RAISE: range(12, 101),
                },
            )

        with self.subTest('player has previously opened or called an overraise and is the last active player'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 9,
                    bet_level = 15,
                    full_bet_level = 15,
                    min_bet = 4,
                    min_raise_increase = 6,
                    player_has_played = False,
                    is_last_active_player = True,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(6, 7),
                },
            )


if __name__ == '__main__':
    main()