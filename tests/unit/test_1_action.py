"""
Defines unit tests on Action class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, managers


class TestAction(TestCase):


    """
    Runs unit tests on Action class.
    """


    def test_instantiation(self):


        """
        Runs test cases to check if action stantiation works as expected.
        """


        # Invalid input types

        with self.assertRaises(TypeError) as cm:
            managers.Action(0, 300)
        self.assertEqual(cm.exception.args[0], messages.action_not_str_name_message.format(int.__name__))

        with self.assertRaises(TypeError) as cm:
            managers.Action(constants.ACTION_BET, '300')
        self.assertEqual(cm.exception.args[0], messages.action_not_int_amount_message.format(str.__name__))


        # Invalid action name

        with self.assertRaises(ValueError) as cm:
            managers.Action('drink', 200)
        self.assertEqual(cm.exception.args[0], messages.action_invalid_name_message.format('drink', ', '.join(constants.possible_action_names)))


        # Action fold amounts

        # Negative amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_FOLD, -100)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_zero_message.format(constants.ACTION_FOLD, -100))

        # Zero amount
        managers.Action(constants.ACTION_FOLD)
        managers.Action(constants.ACTION_FOLD, 0)

        # Non-zero amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_FOLD, 100)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_zero_message.format(constants.ACTION_FOLD, 100))


        # Action check amounts

        # Negative amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_CHECK, -100)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_zero_message.format(constants.ACTION_CHECK, -100))

        # Zero amount
        managers.Action(constants.ACTION_CHECK)
        managers.Action(constants.ACTION_CHECK, 0)

        # Non-zero amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_CHECK, 100)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_zero_message.format(constants.ACTION_CHECK, 100))


        # Action bet amounts

        # Negative amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_BET, -100)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_BET, -100))

        # Zero amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_BET)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_BET, 0))
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_BET, 0)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_BET, 0))

        # Non-zero amount
        managers.Action(constants.ACTION_BET, 100)


        # Action call amounts

        # Negative amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_CALL, -100)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_CALL, -100))

        # Zero amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_CALL)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_CALL, 0))
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_CALL, 0)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_CALL, 0))

        # Non-zero amount
        managers.Action(constants.ACTION_CALL, 100)


        # Action raise amounts

        # Negative amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_RAISE, -100)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_RAISE, -100))

        # Zero amount
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_RAISE)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_RAISE, 0))
        with self.assertRaises(ValueError) as cm:
            managers.Action(constants.ACTION_RAISE, 0)
        self.assertEqual(cm.exception.args[0], messages.action_amount_not_more_than_zero_message.format(constants.ACTION_RAISE, 0))

        # Non-zero amount
        managers.Action(constants.ACTION_RAISE, 100)


if __name__ == '__main__':
    main()