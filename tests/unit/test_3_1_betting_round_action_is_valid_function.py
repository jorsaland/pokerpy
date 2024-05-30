"""
Defines unit tests on action_is_valid function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRoundActionIsValidFunction(TestCase):


    """
    Runs unit tests on action_is_valid function.
    """


    def test_unexpected_action(self):

        """
        Runs test cases where non-defined actions are parsed.
        """

        with self.assertRaises(ValueError):
            pk.action_is_valid(action='drinks', is_under_bet=True)
        
        with self.assertRaises(ValueError):
            pk.action_is_valid(action='drinks', is_under_bet=False)


    def test_actions_under_bet(self):

        """
        Runs test cases where a betting round is under bet.
        """

        # Valid actions under bet
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=True))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=True))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=True))

        # Invalid actions under bet
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=True))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=True))


    def test_actions_under_no_bet(self):

        """
        Runs test cases where a betting round is not under bet.
        """

        # Switch is ON by default

        # Valid actions under no bet, folding forbidden
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=False))

        # Valid actions under no bet, folding forbidden

        self.assertFalse(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=False))

        # Turn OFF switch
        pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = False

        # Valid actions under no bet, folding allowed
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=False))

        # Valid actions under no bet, folding allowed
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=False))

        # Turn switch back ON
        pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = True


if __name__ == '__main__':
    main()