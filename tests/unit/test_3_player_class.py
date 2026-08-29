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


    def test_action_methods(self):


        """
        Runs test cases on methods related to actions.
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
        Runs test cases on methods related to cards.
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
        Runs test cases on methods related to hands.
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

        Andy.clear_hand()
        self.assertIsNone(Andy.hand)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.assign_hand(structures.Card('J', 's'))
        self.assertEqual(cm.exception.args[0], messages.msg_not_hand_instance.format(structures.Card.__name__))


    def test_amount_methods(self):


        """
        Runs test cases on methods related to the amount.
        """


        Andy = structures.Player('Andy', 1000)


        # Before and after effects

        self.assertEqual(Andy.amount, 0)

        Andy.increase_amount(0)
        Andy.increase_amount(50)
        Andy.increase_amount(100)

        self.assertEqual(Andy.amount, 150)

        Andy.clear_amount()

        self.assertEqual(Andy.amount, 0)

        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.increase_amount('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.increase_amount(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_pot_participation_methods(self):


        """
        Runs test cases on methods related to pot participation.
        """


        Andy = structures.Player('Andy', 1000)


        # Before and after effects

        self.assertEqual(Andy.pot_participation, 0)

        Andy.increase_pot_participation(0)
        Andy.increase_pot_participation(50)
        Andy.increase_pot_participation(100)

        self.assertEqual(Andy.pot_participation, 150)

        Andy.clear_pot_participation()

        self.assertEqual(Andy.pot_participation, 0)

        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.increase_pot_participation('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.increase_pot_participation(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_stack_methods(self):


        """
        Runs test cases on methods related to the stack.
        """


        Andy = structures.Player('Andy', 1000)


        # Before and after effects

        self.assertEqual(Andy.stack, 1000)

        Andy.increase_stack(0)
        Andy.increase_stack(50)
        Andy.increase_stack(100)

        self.assertEqual(Andy.stack, 1150)

        Andy.decrease_stack(0)
        Andy.decrease_stack(50)
        Andy.decrease_stack(100)

        self.assertEqual(Andy.stack, 1000)

        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.increase_stack('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.increase_stack(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))

        with self.assertRaises(TypeError) as cm:
            Andy.decrease_stack('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.decrease_stack(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_boolean_status_methods(self):


        """
        Runs test cases on methods related to boolean status.
        """


        Andy = structures.Player('Andy', 1000)

        self.assertFalse(Andy.is_folded)
        Andy.mark_is_folded()
        self.assertTrue(Andy.is_folded)
        Andy.unmark_is_folded()
        self.assertFalse(Andy.is_folded)

        self.assertFalse(Andy.has_played)
        Andy.mark_has_played()
        self.assertTrue(Andy.has_played)
        Andy.unmark_has_played()
        self.assertFalse(Andy.has_played)


if __name__ == '__main__':
    main()