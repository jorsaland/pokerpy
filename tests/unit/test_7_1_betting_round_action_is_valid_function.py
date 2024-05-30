"""
Defines unit tests on action_is_valid function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, switches


class TestBettingRoundActionIsValidFunction(TestCase):


    """
    Runs unit tests on action_is_valid function.
    """


    def test_unexpected_action(self):

        """
        Runs test cases where non-defined actions are parsed.
        """

        with self.assertRaises(ValueError):
            managers.action_is_valid(action='drinks', is_under_bet=True)
        
        with self.assertRaises(ValueError):
            managers.action_is_valid(action='drinks', is_under_bet=False)


    def test_actions_under_bet(self):

        """
        Runs test cases where a betting round is under bet.
        """

        # Valid actions under bet
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_FOLD, is_under_bet=True))
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_CALL, is_under_bet=True))
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_RAISE, is_under_bet=True))

        # Invalid actions under bet
        self.assertFalse(managers.action_is_valid(action=constants.ACTION_CHECK, is_under_bet=True))
        self.assertFalse(managers.action_is_valid(action=constants.ACTION_BET, is_under_bet=True))


    def test_actions_under_no_bet(self):

        """
        Runs test cases where a betting round is not under bet.
        """

        # Switch is ON by default

        # Valid actions under no bet, folding forbidden
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_BET, is_under_bet=False))

        # Valid actions under no bet, folding forbidden

        self.assertFalse(managers.action_is_valid(action=constants.ACTION_FOLD, is_under_bet=False))
        self.assertFalse(managers.action_is_valid(action=constants.ACTION_CALL, is_under_bet=False))
        self.assertFalse(managers.action_is_valid(action=constants.ACTION_RAISE, is_under_bet=False))

        # Turn OFF switch
        switches.ONLY_ALLOW_FOLDING_UNDER_BET = False

        # Valid actions under no bet, folding allowed
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_BET, is_under_bet=False))
        self.assertTrue(managers.action_is_valid(action=constants.ACTION_FOLD, is_under_bet=False))

        # Valid actions under no bet, folding allowed
        self.assertFalse(managers.action_is_valid(action=constants.ACTION_CALL, is_under_bet=False))
        self.assertFalse(managers.action_is_valid(action=constants.ACTION_RAISE, is_under_bet=False))

        # Turn switch back ON
        switches.ONLY_ALLOW_FOLDING_UNDER_BET = True


if __name__ == '__main__':
    main()