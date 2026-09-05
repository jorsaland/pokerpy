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
                    player_stack = -1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative player amount'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = -100,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative bet level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = -100,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative full bet level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = -100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative minimum bet'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = -100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('zero minimum bet'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 0,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('negative minimum raise increase'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = -100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('zero minimum raise increase'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 0,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )


    def test_composed_invalid_inputs(self):

        "Tests parsed invalid combinations."

        with self.subTest('minimum raise increase smaller than minimum bet'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 50,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('minimum raise expected level not larger than current bet level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 200,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )

        with self.subTest('bet level smaller than full current level'):
            with self.assertRaises(AssertionError):
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                )


class TestNotFacingAnAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is not facing an
    aggression.
    """


    def test_not_facing_aggression_cannot_afford_a_full_bet(self):

        "Tests player not having enough chips to cover a full bet."

        with self.subTest('has not placed money, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(50, 51),
                },
            )

        with self.subTest('has not placed money, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(50, 51),
                },
            )

        with self.subTest('has placed a big blind, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100, ## *BB*
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(50, 51),
                },
            )

        with self.subTest('has placed a big blind, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100, ## *BB*
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(50, 51),
                },
            )


    def test_not_facing_aggression_can_afford_a_full_bet_but_no_more(self):

        "Tests player having just enough chips to cover a full bet."

        with self.subTest('has not placed money, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 101),
                },
            )

        with self.subTest('has not placed money, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 101),
                },
            )

        with self.subTest('has placed a big blind, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100, ## *BB*
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 101),
                },
            )

        with self.subTest('has placed a big blind, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100, ## *BB*
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 101),
                },
            )


    def test_not_facing_aggression_can_afford_more_than_a_full_bet(self):

        "Tests player having more than enough chips to cover a full bet."

        with self.subTest('has not placed money, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 1001),
                },
            )

        with self.subTest('has not placed money, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 0,
                    bet_level = 0,
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 1001),
                },
            )

        with self.subTest('has placed a big blind, open fold is allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 900,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100, ## *BB*
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = True,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 901),
                },
            )

        with self.subTest('has placed a big blind, open fold is not allowed'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 900,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100, ## *BB*
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(100, 901),
                },
            )


    def test_not_facing_aggression_being_small_blind(self):

        "Tests player being the small blind."

        with self.subTest('small blind, not enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 20,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100, ## BB
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(20, 21),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('small blind, just enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100, ## BB
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(50, 51),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('small blind, not enough to make a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100, ## BB
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                    constants.ACTION_RAISE: range(100, 101),
                },
            )

        with self.subTest('small blind, just enough to make a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100, ## BB
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                    constants.ACTION_RAISE: range(150, 151),
                },
            )

        with self.subTest('small blind, more than enough to make a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 1000,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100, ## BB
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                    constants.ACTION_RAISE: range(150, 1001),
                },
            )


class TestFacingAnIncompleteAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is facing an
    aggression that is not enough to be considered a full bet or full raise.
    """


    def test_facing_incomplete_aggression_cannot_afford_a_full_call(self):

        "Tests player not having enough chips to cover the call amount."

        with self.subTest('has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 20,
                    player_bet_level = 0,
                    bet_level = 50, ## underbet
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(20, 21),
                },
            )

        with self.subTest('has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 20,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100 + 50, ## *BB* + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(20, 21),
                },
            )

        with self.subTest('has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 20,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 50, ## *bet* + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(20, 21),
                },
            )

        with self.subTest('has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 100, ## *overbet* + underraise
                    full_bet_level = 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 20,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 50, ## bet + *raise* + underraise
                    full_bet_level = 200,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(20, 21),
                },
            )

        with self.subTest('has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 100, ## bet + *overraise* + underraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )


    def test_facing_incomplete_aggression_can_afford_a_full_call_but_no_more(self):

        "Tests player having just enough chips to cover the call amount."

        with self.subTest('has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 0,
                    bet_level = 50, ## underbet
                    full_bet_level = 0,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100 + 50, ## *BB* + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 50, ## *bet* + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 100, ## *overbet* + underraise
                    full_bet_level = 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 50, ## bet + *raise* + *underraise*
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 100, ## bet + *overraise* + underraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )


    def test_facing_incomplete_aggression_can_afford_a_full_call_but_not_to_complete_the_aggression(self):

        "Test player having enough chips to make an increment but not to complete the full bet or raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(50, 51),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_BET] = range(70, 71)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 70,
                        player_bet_level = 0,
                        bet_level = 50, ## underbet
                        full_bet_level = 0,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(50, 51),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_BET] = range(70, 71)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 70,
                        player_bet_level = 0,
                        bet_level = 50, ## underbet
                        full_bet_level = 0,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        with self.subTest('has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 70,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 50, ## *bet* + underbet
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 120,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 100, ## *overbet* + underraise
                    full_bet_level = 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 70,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 50, ## bet + *raise* + underraise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 120,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 100, ## bet + *overraise* + underraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )


    def test_facing_incomplete_aggression_can_afford_to_complete_the_aggression_but_no_more(self):

        "Tests player having just enough chips to complete the bet or raise, but not to re-raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(50, 51),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_BET] = range(100, 101)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 100,
                        player_bet_level = 0,
                        bet_level = 50, ## underbet
                        full_bet_level = 0,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(50, 51),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_BET] = range(100, 101)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 100,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 50, ## *BB* + underraise
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        with self.subTest('has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 50, ## *bet* + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 100, ## *overbet* + underraise
                    full_bet_level = 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 50, ## bet + *raise* + underraise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 100, ## bet + *overraise* + underraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )


    def test_facing_incomplete_aggression_can_afford_to_complete_the_aggression_and_more(self):

        "Tests player having more than enough chips to complete the bet or raise but not to make a full re-raise"

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(50, 51),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_BET] = range(100, 1001)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 1000,
                        player_bet_level = 0,
                        bet_level = 50, ## underbet
                        full_bet_level = 0,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(50, 51),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_BET] = range(100, 901)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 900,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 50, ## *BB* + underraise
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        with self.subTest('has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 900,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 50, ## *bet* + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 850,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 100, ## *overbet* + underraise
                    full_bet_level = 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 800,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 50, ## bet + *raise* + underraise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 750,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 100, ## bet + *overraise* + underraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )


    def test_facing_incomplete_aggression_being_small_blind(self):

        "Tests player being the small blind."

        with self.subTest('small blind, not enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100 + 50, ## BB + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(50, 51),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('small blind, just enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100 + 50, ## BB + underraise
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(100, 101),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(120, 121)
            with self.subTest('small blind, not enough to complete the aggression', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 120,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 50, ## BB + underraise
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(150, 151)
            with self.subTest('small blind, just enough to complete the aggression', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 150,
                        player_bet_level = 50, ## *SB*
                        bet_level = 150, ## BB + underraise
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(150, 951)
            with self.subTest('small blind, more than enough to complete the aggression', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 950,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 50, ## BB + underraise
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


class TestFacingACompleteAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is facing a
    full bet or a full raise but no more than that.
    """


    def test_facing_complete_aggression_cannot_afford_a_full_call(self):

        "Tests player not having enough chips to cover the call amount."

        with self.subTest('has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 0,
                    bet_level = 100, ## bet
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100 + 100, ## *BB* + raise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 100, ## *bet* + raise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 150, ## *overbet* + raise
                    full_bet_level = 150 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 50,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 100, ## bet + *raise* + raise
                    full_bet_level = 100 + 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(50, 51),
                },
            )

        with self.subTest('has opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 150, ## bet + *overraise* + raise
                    full_bet_level = 100 + 150 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )


    def test_facing_complete_aggression_can_afford_a_full_call_but_no_more(self):

        "Tests player having just enough chips to cover the call amount."

        with self.subTest('has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 100, ## bet
                    full_bet_level = 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100 + 100, ## *BB* + raise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 100, ## *bet* + raise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 150, ## *overbet* + raise
                    full_bet_level = 150 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )

        with self.subTest('has opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 100, ## bet + *raise* + raise
                    full_bet_level = 100 + 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 150, ## bet + *overraise* + raise
                    full_bet_level = 100 + 150 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )


    def test_facing_complete_aggression_can_afford_to_call_but_not_to_make_a_full_reraise(self):

        "Tests player having more than enough chips to complete the bet or raise but not to make a full re-raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(150, 151)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 150,
                        player_bet_level = 0,
                        bet_level = 100, ## bet
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(150, 151)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 150,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 100, ## *BB* + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(150, 151)
            with self.subTest('has opened or called a full bet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 150,
                        player_bet_level = 100, ## *bet*
                        bet_level = 100 + 100, ## *bet* + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('has opened or called an overbet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 150, ## *overbet*
                        bet_level = 150 + 150, ## *overbet* + raise
                        full_bet_level = 150 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(150, 151)
            with self.subTest('has opened or called a full raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 150,
                        player_bet_level = 100 + 100, ## bet + *raise*
                        bet_level = 100 + 100 + 100, ## bet + *raise* + raise
                        full_bet_level = 100 + 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('has opened or called an overraise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 100 + 150, ## bet + *overraise*
                        bet_level = 100 + 150 + 150, ## bet + *overraise* + raise
                        full_bet_level = 100 + 150 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


    def test_facing_complete_aggression_can_afford_make_a_full_reraise_but_no_more(self):

        "Tests player having just enough chips to complete a full re-raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 201)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 200,
                        player_bet_level = 0,
                        bet_level = 100, ## bet
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 201)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 200,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 100, ## *BB* + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 201)
            with self.subTest('has opened or called a full bet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 200,
                        player_bet_level = 100, ## *bet*
                        bet_level = 100 + 100, ## *bet* + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 301)
            with self.subTest('has opened or called an overbet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 300,
                        player_bet_level = 150, ## *overbet*
                        bet_level = 150 + 150, ## *overbet* + raise
                        full_bet_level = 150 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 201)
            with self.subTest('has opened or called a full raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 200,
                        player_bet_level = 100 + 100, ## bet + *raise*
                        bet_level = 100 + 100 + 100, ## bet + *raise* + raise
                        full_bet_level = 100 + 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 301)
            with self.subTest('has opened or called an overraise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 300,
                        player_bet_level = 100 + 150, ## bet + *overraise*
                        bet_level = 100 + 150 + 150, ## bet + *overraise* + raise
                        full_bet_level = 100 + 150 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


    def test_facing_complete_aggression_can_afford_make_a_full_reraise_and_more(self):

        "Tests player having more than enough chips to complete a full re-raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 1001)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 1000,
                        player_bet_level = 0,
                        bet_level = 100, ## bet
                        full_bet_level = 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 901)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 900,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 100, ## *BB* + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 901)
            with self.subTest('has opened or called a full bet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 900,
                        player_bet_level = 100, ## *bet*
                        bet_level = 100 + 100, ## *bet* + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 851)
            with self.subTest('has opened or called an overbet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 850,
                        player_bet_level = 150, ## *overbet*
                        bet_level = 150 + 150, ## *overbet* + raise
                        full_bet_level = 150 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(100, 101),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 801)
            with self.subTest('has opened or called a full raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 800,
                        player_bet_level = 100 + 100, ## bet + *raise*
                        bet_level = 100 + 100 + 100, ## bet + *raise* + raise
                        full_bet_level = 100 + 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 751)
            with self.subTest('has opened or called an overraise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 750,
                        player_bet_level = 100 + 150, ## bet + *overraise*
                        bet_level = 100 + 150 + 150, ## bet + *overraise* + raise
                        full_bet_level = 100 + 150 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


    def test_facing_complete_aggression_being_small_blind(self):

        "Tests player being the small blind."

        with self.subTest('small blind, not enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100 + 100, ## BB + raise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(100, 101),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('small blind, just enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100 + 100, ## BB + raise
                    full_bet_level = 100 + 100,
                    min_bet = 100,
                    min_raise_increase = 100,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(150, 151),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(200, 201)
            with self.subTest('small blind, not enough to make a full re-raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 200,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 100, ## BB + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('small blind, just enough to make a full re-raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 100, ## BB + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 951)
            with self.subTest('small blind, more than enough to make a full re-raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 950,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 100, ## BB + raise
                        full_bet_level = 100 + 100,
                        min_bet = 100,
                        min_raise_increase = 100,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


class TestFacingAnOverAggression(TestCase):


    """
    Runs unit tests on get_valid_action_names function in cases where the player is facing an
    overbet or an overraise.
    """


    def test_facing_over_aggression_cannot_afford_a_full_call(self):

        "Tests player not having enough chips to cover the call amount."

        with self.subTest('has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 0,
                    bet_level = 150, ## overbet
                    full_bet_level = 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100 + 150, ## *BB* + overraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 150, ## *bet* + overraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 250, ## *overbet* + overraise
                    full_bet_level = 150 + 250,
                    min_bet = 100,
                    min_raise_increase = 250,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )

        with self.subTest('has opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 100,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 150, ## bet + *raise* + overraise
                    full_bet_level = 100 + 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(100, 101),
                },
            )

        with self.subTest('has opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 250, ## bet + *overraise* + overraise
                    full_bet_level = 100 + 150 + 250,
                    min_bet = 100,
                    min_raise_increase = 250,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )


    def test_facing_over_aggression_can_afford_a_full_call_but_no_more(self):

        "Tests player having just enough chips to cover the call amount."

        with self.subTest('player has not placed money'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 0,
                    bet_level = 150, ## overbet
                    full_bet_level = 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )

        with self.subTest('player has placed a big blind'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 100, ## *BB*
                    bet_level = 100 + 150, ## *BB* + overraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )

        with self.subTest('player has previously opened or called a full bet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 100, ## *bet*
                    bet_level = 100 + 150, ## *bet* + overraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )

        with self.subTest('player has previously opened or called an overbet'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 250,
                    player_bet_level = 150, ## *overbet*
                    bet_level = 150 + 250, ## *overbet* + overraise
                    full_bet_level = 150 + 250,
                    min_bet = 100,
                    min_raise_increase = 250,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(250, 251),
                },
            )

        with self.subTest('player has previously opened or called a full raise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 100 + 100, ## bet + *raise*
                    bet_level = 100 + 100 + 150, ## bet + *raise* + overraise
                    full_bet_level = 100 + 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(150, 151),
                },
            )

        with self.subTest('player has previously opened or called an overraise'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 250,
                    player_bet_level = 100 + 150, ## bet + *overraise*
                    bet_level = 100 + 150 + 250, ## bet + *overraise* + overraise
                    full_bet_level = 100 + 150 + 250,
                    min_bet = 100,
                    min_raise_increase = 250,
                    player_has_played = True,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_FOLD: range(0, 1),
                    constants.ACTION_CALL: range(250, 251),
                },
            )


    def test_facing_over_aggression_can_afford_to_call_but_not_to_make_a_full_reraise(self):

        "Tests player having more than enough chips to complete the bet or raise but not to make a full re-raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 0,
                        bet_level = 150, ## overbet
                        full_bet_level = 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 150, ## *BB* + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('has opened or called a full bet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 100, ## *bet*
                        bet_level = 100 + 150, ## *bet* + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(250, 251),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(400, 401)
            with self.subTest('has opened or called an overbet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 400,
                        player_bet_level = 150, ## *overbet*
                        bet_level = 150 + 250, ## *overbet* + overraise
                        full_bet_level = 150 + 250,
                        min_bet = 100,
                        min_raise_increase = 250,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('has opened or called a full raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 100 + 100, ## bet + *raise*
                        bet_level = 100 + 100 + 150, ## bet + *raise* + overraise
                        full_bet_level = 100 + 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(250, 251),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(400, 401)
            with self.subTest('has opened or called an overraise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 400,
                        player_bet_level = 100 + 150, ## bet + *overraise*
                        bet_level = 100 + 150 + 250, ## bet + *overraise* + overraise
                        full_bet_level = 100 + 150 + 250,
                        min_bet = 100,
                        min_raise_increase = 250,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


    def test_facing_over_aggression_can_afford_make_a_full_reraise_but_no_more(self):

        "Tests player having just enough chips to complete a full re-raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 301)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 300,
                        player_bet_level = 0,
                        bet_level = 150, ## overbet
                        full_bet_level = 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 301)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 300,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 150, ## *BB* + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 301)
            with self.subTest('has opened or called a full bet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 300,
                        player_bet_level = 100, ## *bet*
                        bet_level = 100 + 150, ## *bet* + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(250, 251),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(500, 501)
            with self.subTest('has opened or called an overbet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 500,
                        player_bet_level = 150, ## *overbet*
                        bet_level = 150 + 250, ## *overbet* + overraise
                        full_bet_level = 150 + 250,
                        min_bet = 100,
                        min_raise_increase = 250,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 301)
            with self.subTest('has opened or called a full raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 300,
                        player_bet_level = 100 + 100, ## bet + *raise*
                        bet_level = 100 + 100 + 150, ## bet + *raise* + overraise
                        full_bet_level = 100 + 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(250, 251),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(500, 501)
            with self.subTest('has opened or called an overraise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 500,
                        player_bet_level = 100 + 150, ## bet + *overraise*
                        bet_level = 100 + 150 + 250, ## bet + *overraise* + overraise
                        full_bet_level = 100 + 150 + 250,
                        min_bet = 100,
                        min_raise_increase = 250,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


    def test_facing_over_aggression_can_afford_make_a_full_reraise_and_more(self):

        "Tests player having more than enough chips to complete a full re-raise."

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 1001)
            with self.subTest('has not placed money', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 1000,
                        player_bet_level = 0,
                        bet_level = 150, ## overbet
                        full_bet_level = 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 901)
            with self.subTest('has placed a big blind', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 900,
                        player_bet_level = 100, ## *BB*
                        bet_level = 100 + 150, ## *BB* + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 901)
            with self.subTest('has opened or called a full bet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 900,
                        player_bet_level = 100, ## *bet*
                        bet_level = 100 + 150, ## *bet* + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(250, 251),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(500, 851)
            with self.subTest('has opened or called an overbet', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 850,
                        player_bet_level = 150, ## *overbet*
                        bet_level = 150 + 250, ## *overbet* + overraise
                        full_bet_level = 150 + 250,
                        min_bet = 100,
                        min_raise_increase = 250,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(150, 151),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(300, 801)
            with self.subTest('has opened or called a full raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 800,
                        player_bet_level = 100 + 100, ## bet + *raise*
                        bet_level = 100 + 100 + 150, ## bet + *raise* + overraise
                        full_bet_level = 100 + 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(250, 251),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(500, 751)
            with self.subTest('has opened or called an overraise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 750,
                        player_bet_level = 100 + 150, ## bet + *overraise*
                        bet_level = 100 + 150 + 250, ## bet + *overraise* + overraise
                        full_bet_level = 100 + 150 + 250,
                        min_bet = 100,
                        min_raise_increase = 250,
                        player_has_played = True,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


    def test_facing_over_aggression_being_small_blind(self):

        "Tests player being the small blind."

        with self.subTest('small blind, not enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 150,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100 + 150, ## BB + overraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(150, 151),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        with self.subTest('small blind, just enough to call'):
            self.assertDictEqual(
                engines.get_valid_actions(
                    player_stack = 200,
                    player_bet_level = 50, ## *SB*
                    bet_level = 100 + 150, ## BB + overraise
                    full_bet_level = 100 + 150,
                    min_bet = 100,
                    min_raise_increase = 150,
                    player_has_played = False,
                    is_last_actionable_player = False,
                    open_fold_allowed = False,
                ),
                {
                    constants.ACTION_CALL: range(200, 201),
                    constants.ACTION_FOLD: range(0, 1),
                },
            )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(200, 201),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(250, 251)
            with self.subTest('small blind, not enough to make a full re-raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 250,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 150, ## BB + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(200, 201),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(350, 351)
            with self.subTest('small blind, just enough to make a full re-raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 350,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 150, ## BB + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )

        for is_last_actionable_player in (False, True):
            valid_actions = {
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_CALL: range(200, 201),
            }
            if not is_last_actionable_player:
                valid_actions[constants.ACTION_RAISE] = range(350, 951)
            with self.subTest('small blind, more than enough to make a full re-raise', is_last_actionable_player=is_last_actionable_player):
                self.assertDictEqual(
                    engines.get_valid_actions(
                        player_stack = 950,
                        player_bet_level = 50, ## *SB*
                        bet_level = 100 + 150, ## BB + overraise
                        full_bet_level = 100 + 150,
                        min_bet = 100,
                        min_raise_increase = 150,
                        player_has_played = False,
                        is_last_actionable_player = is_last_actionable_player,
                        open_fold_allowed = False,
                    ),
                    valid_actions,
                )


if __name__ == '__main__':
    main()