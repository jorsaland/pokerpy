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

        structures.Player('Andy')


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            structures.Player(1933)
        self.assertEqual(cm.exception.args[0], messages.player_not_str_name_message.format(int.__name__))
        
        with self.assertRaises(TypeError) as cm:
            structures.Player('Andy', smallest_chip='1')
        self.assertEqual(cm.exception.args[0], messages.player_not_int_smallest_chip_message.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            structures.Player('Andy', smallest_chip=0)
        self.assertEqual(cm.exception.args[0], messages.player_not_positive_smalleset_chip_message.format(0))


    def test_request_action_and_reset_action_methods(self):


        """
        Runs test cases on request_action and reset_action methods.
        """


        Andy = structures.Player('Andy')


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
        self.assertEqual(cm.exception.args[0], messages.player_not_action_instance_message.format(str.__name__))


    def test_deal_card_method(self):


        """
        Runs test cases on deal_card method.
        """


        Andy = structures.Player('Andy')


        # Valid inputs

        Andy.deal_card(structures.Card('A', 's'))
        self.assertEqual(Andy.cards, (structures.Card('A', 's'),))

        Andy.deal_card(structures.Card('J', 'd'))
        self.assertEqual(Andy.cards, (structures.Card('A', 's'), structures.Card('J', 'd')))


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.deal_card('As')
        self.assertEqual(cm.exception.args[0], messages.player_not_card_instance_message.format(str.__name__))


    def test_assign_hand_method(self):


        """
        Runs test cases on assign_hand method.
        """


        Andy = structures.Player('Andy')


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


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.assign_hand(structures.Card('J', 's'))
        self.assertEqual(cm.exception.args[0], messages.player_not_hand_instance_message.format(structures.Card.__name__))


    def test_add_to_current_amount_method(self):


        """
        Runs test cases on add_to_current_amount method.
        """


        Andy = structures.Player('Andy', smallest_chip=10)


        # Valid inputs

        Andy.add_to_current_amount(0)
        Andy.add_to_current_amount(50)
        Andy.add_to_current_amount(100)

        self.assertEqual(Andy.current_amount, 150)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            Andy.add_to_current_amount('100')
        self.assertEqual(cm.exception.args[0], messages.player_not_int_current_amount_message.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            Andy.add_to_current_amount(-100)
        self.assertEqual(cm.exception.args[0], messages.player_increase_not_multiple_of_smallest_chip_message.format(10, -100))

        with self.assertRaises(ValueError) as cm:
            Andy.add_to_current_amount(7)
        self.assertEqual(cm.exception.args[0], messages.player_increase_not_multiple_of_smallest_chip_message.format(10, 7))

        with self.assertRaises(ValueError) as cm:
            Andy.add_to_current_amount(77)
        self.assertEqual(cm.exception.args[0], messages.player_increase_not_multiple_of_smallest_chip_message.format(10, 77))


    def test_reset_betting_round_states_method(self):


        """
        Runs test cases on reset_betting_round_states method.
        """


        Andy = structures.Player('Andy')

        Andy.request_action(structures.Action(constants.ACTION_BET, 200))
        Andy.add_to_current_amount(200)

        Andy.reset_betting_round_states()

        self.assertIsNone(Andy.requested_action)
        self.assertEqual(Andy.current_amount, 0)


    def test_reset_cycle_states_method(self):


        """
        Runs test cases on reset_cycle_states method.
        """


        Andy = structures.Player('Andy')

        Andy.request_action(structures.Action(constants.ACTION_BET, 200))
        Andy.add_to_current_amount(200)
        Andy.deal_card(structures.Card('J', 'd'))
        Andy.assign_hand(structures.Hand([
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
            structures.Card('7', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'c'),
        ]))

        Andy.reset_cycle_states()

        self.assertIsNone(Andy.requested_action)
        self.assertEqual(Andy.current_amount, 0)
        self.assertTupleEqual(Andy.cards, ())
        self.assertIsNone(Andy.hand)


if __name__ == '__main__':
    main()