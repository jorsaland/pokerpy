"""
Defines unit tests on Action class.
"""


import sys
sys.path.insert(0, '.')


from decimal import Decimal
from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestActionInstantiation(TestCase):


    "Runs unit tests on action instantiation."


    def test_category_type_errors(self):

        "Tests type error detection on field category."

        bad_categories = (1, None)

        for bad_category in bad_categories:

            with self.subTest(category=bad_category):
                with self.assertRaises(TypeError) as cm:
                    structures.Action(category=bad_category, amount=300)
                self.assertEqual(cm.exception.args[0], messages.msg_not_str.format(type(bad_category).__name__))


    def test_amount_type_errors(self):

        "Tests type error detection on field amount."

        bad_amounts = ('300', 300.0, Decimal('300'), None)

        for bad_amount in bad_amounts:

            with self.subTest(amount=bad_amount):
                with self.assertRaises(TypeError) as cm:
                    structures.Action(constants.ACTION_BET, amount=bad_amount)
                self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))


    def test_category_name_value_error(self):

        "Tests value error detection on category name."

        bad_categories = ('drink', '')

        for bad_category in bad_categories:

            with self.subTest(category=bad_category):
                with self.assertRaises(ValueError) as cm:
                    structures.Action(bad_category, 200)
                self.assertEqual(cm.exception.args[0], messages.msg_invalid_action_name.format(', '.join(constants.possible_action_names)))


    def test_fold_amount_value_error(self):

        "Tests value error detection on amount when action is fold."

        bad_amounts = (-100, 100)

        for bad_amount in bad_amounts:

            with self.subTest(amount=bad_amount):
                with self.assertRaises(ValueError) as cm:
                    structures.Action(constants.ACTION_FOLD, bad_amount)
                self.assertEqual(cm.exception.args[0], messages.msg_not_zero_value.format(bad_amount))


    def test_check_amount_value_error(self):

        "Tests value error detection on amount when action is check."

        bad_amounts = (-100, 100)

        for bad_amount in bad_amounts:

            with self.subTest(amount=bad_amount):
                with self.assertRaises(ValueError) as cm:
                    structures.Action(constants.ACTION_CHECK, bad_amount)
                self.assertEqual(cm.exception.args[0], messages.msg_not_zero_value.format(bad_amount))


    def test_call_amount_value_error(self):

        "Tests value error detection on amount when action is call."

        bad_amounts = (-100, 0)

        for bad_amount in bad_amounts:

            with self.subTest(amount=bad_amount):
                with self.assertRaises(ValueError) as cm:
                    structures.Action(constants.ACTION_CALL, bad_amount)
                self.assertEqual(cm.exception.args[0], messages.msg_not_positive_value.format(bad_amount))


    def test_bet_amount_value_error(self):

        "Tests value error detection on amount when action is bet."

        bad_amounts = (-100, 0)

        for bad_amount in bad_amounts:

            with self.subTest(amount=bad_amount):
                with self.assertRaises(ValueError) as cm:
                    structures.Action(constants.ACTION_BET, bad_amount)
                self.assertEqual(cm.exception.args[0], messages.msg_not_positive_value.format(bad_amount))


    def test_raise_amount_value_error(self):

        "Tests value error detection on amount when action is raise."

        bad_amounts = (-100, 0)

        for bad_amount in bad_amounts:

            with self.subTest(amount=bad_amount):
                with self.assertRaises(ValueError) as cm:
                    structures.Action(constants.ACTION_RAISE, bad_amount)
                self.assertEqual(cm.exception.args[0], messages.msg_not_positive_value.format(bad_amount))


    def test_valid_instantiation(self):

        "Tests valid instantiation."

        categories_and_amounts = [
            (constants.ACTION_FOLD, 0),
            (constants.ACTION_CHECK, 0),
            (constants.ACTION_CALL, 100),
            (constants.ACTION_BET, 100),
            (constants.ACTION_RAISE, 100),
        ]

        for category, amount in categories_and_amounts:

            action = structures.Action(category, amount)

            with self.subTest(action=str(action)):
                self.assertEqual(action.category, category)
                self.assertEqual(action.amount, amount)


if __name__ == '__main__':
    main()