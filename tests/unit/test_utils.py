"""
Runs unit tests on utils section.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestActionIsValid(TestCase):


    """
    Runs unit tests on function action_is_valid.
    """


    def test_unexpected_action(self):

        with self.assertRaises(ValueError):
            pk.action_is_valid(action='drinks', is_under_bet=True)
        with self.assertRaises(ValueError):
            pk.action_is_valid(action='drinks', is_under_bet=False)


    def test_actions_under_bet(self):

        # Valid actions under bet
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=True))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=True))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=True))

        # Invalid actions under bet
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=True))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=True))


    def test_actions_under_no_bet_folding_forbidden(self):

        pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = True

        # Valid actions under no bet, folding forbidden
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=False))

        # Valid actions under no bet, folding forbidden
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=False))


    def test_actions_under_no_bet_folding_allowed(self):

        pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = False

        # Valid actions under no bet, folding allowed
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=False))

        # Valid actions under no bet, folding allowed
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=False))


if __name__ == '__main__':
    main()