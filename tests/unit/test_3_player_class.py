"""
Defines unit tests on Player class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestPlayerClass(TestCase):


    """
    Runs unit tests on Player class.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation.
        """


        # Valid inputs

        structures.Player('Andy', 1000)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            structures.Player(1933, stack=1000)
        self.assertEqual(cm.exception.args[0], messages.msg_not_str.format(int.__name__))
        
        with self.assertRaises(TypeError) as cm:
            structures.Player('Andy', stack='1000')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))


    def test_request_action_and_reset_action_methods(self):


        """
        Runs test cases on request_action and reset_action methods.
        """


        Andy = structures.Player('Andy', 1000)

        # Valid inputs

        Andy.request_action(structures.Action(constants.ACTION_BET, 100))
        self.assertEqual(Andy.requested_action, structures.Action(constants.ACTION_BET, 100))

        Andy.request_action(structures.Action(constants.ACTION_CALL, 100))
        self.assertEqual(Andy.requested_action, structures.Action(constants.ACTION_CALL, 100))

        Andy.request_action(structures.Action(constants.ACTION_RAISE, 100))
        self.assertEqual(Andy.requested_action, structures.Action(constants.ACTION_RAISE, 100))

        Andy.request_action(structures.Action(constants.ACTION_CHECK))
        self.assertEqual(Andy.requested_action, structures.Action(constants.ACTION_CHECK))

        Andy.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(Andy.requested_action, structures.Action(constants.ACTION_FOLD))

        Andy.reset_action()
        self.assertIsNone(Andy.requested_action)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.request_action(constants.ACTION_BET)
        self.assertEqual(cm.exception.args[0], messages.msg_not_action_instance.format(str.__name__))


    def test_card_methods(self):


        """
        Runs test cases on assign_card and reset_cards methods.
        """


        Andy = structures.Player('Andy', 1000)


        # Valid inputs

        Andy.assign_card(structures.Card('A', 's'))
        self.assertEqual(Andy.cards, (structures.Card('A', 's'),))

        Andy.assign_card(structures.Card('J', 'd'))
        self.assertEqual(Andy.cards, (structures.Card('A', 's'), structures.Card('J', 'd')))

        Andy.reset_cards()
        self.assertEqual(Andy.cards, ())

        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.assign_card('As')
        self.assertEqual(cm.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        Andy.assign_card(structures.Card('A', 's'))
        with self.assertRaises(ValueError) as cm:
            Andy.assign_card(structures.Card('A', 's'))
        self.assertEqual(cm.exception.args[0], messages.msg_repeated_cards)


    def test_hand_methods(self):


        """
        Runs test cases on assign_hand and reset_hand methods.
        """


        Andy = structures.Player('Andy', 1000)


        # Valid inputs

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        self.assertEqual(Andy.hand, structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))

        Andy.assign_hand(structures.Hand([
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
            structures.Card('7', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'c'),
        ]))
        self.assertEqual(Andy.hand, structures.Hand([
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
            structures.Card('7', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'c'),
        ]))

        Andy.reset_hand()
        self.assertIsNone(Andy.hand)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.assign_hand(structures.Card('J', 's'))
        self.assertEqual(cm.exception.args[0], messages.msg_not_hand_instance.format(structures.Card.__name__))


    def test_current_amount_methods(self):


        """
        Runs test cases on add_to_current_amount and reset_current_amount methods.
        """


        Andy = structures.Player('Andy', 1000)


        # Before and after effects

        self.assertEqual(Andy.current_amount, 0)

        Andy.add_to_current_amount(0)
        Andy.add_to_current_amount(50)
        Andy.add_to_current_amount(100)

        self.assertEqual(Andy.current_amount, 150)

        Andy.reset_current_amount()

        self.assertEqual(Andy.current_amount, 0)

        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.add_to_current_amount('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.add_to_current_amount(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_add_to_stack_method(self):


        """
        Runs test cases on add_to_stack_method method.
        """


        Andy = structures.Player('Andy', 1000)


        # Before and after effects

        self.assertEqual(Andy.stack, 1000)

        Andy.add_to_stack(0)
        Andy.add_to_stack(50)
        Andy.add_to_stack(100)

        self.assertEqual(Andy.stack, 1150)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.add_to_stack('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.add_to_stack(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_remove_from_stack_method(self):


        """
        Runs test cases on add_stack_method method.
        """


        Andy = structures.Player('Andy', 1000)


        # Before and after effects

        self.assertEqual(Andy.stack, 1000)

        Andy.remove_from_stack(0)
        Andy.remove_from_stack(50)
        Andy.remove_from_stack(100)

        self.assertEqual(Andy.stack, 850)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.remove_from_stack('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.remove_from_stack(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_fold_methods(self):


        """
        Runs test cases on set_as_folded and unset_as_folded methods.
        """


        Andy = structures.Player('Andy', 1000)

        # Before and after effects

        self.assertFalse(Andy.is_folded)
        Andy.set_as_folded()
        self.assertTrue(Andy.is_folded)
        Andy.unset_as_folded()
        self.assertFalse(Andy.is_folded)


if __name__ == '__main__':
    main()