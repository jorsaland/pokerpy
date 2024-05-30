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


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            structures.Player(1933)
        self.assertEqual(cm.exception.args[0], messages.player_not_str_name_message.format(int.__name__))
        
        with self.assertRaises(TypeError) as cm:
            structures.Player(['Andy'])
        self.assertEqual(cm.exception.args[0], messages.player_not_str_name_message.format(list.__name__))


    def test_request_action_method(self):


        """
        Runs test cases on request_action method.
        """


        Andy = structures.Player('Andy')


        # Valid inputs

        Andy.request_action(constants.ACTION_BET)
        Andy.request_action(constants.ACTION_CALL)
        Andy.request_action(constants.ACTION_CHECK)
        Andy.request_action(constants.ACTION_FOLD)
        Andy.request_action(constants.ACTION_RAISE)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            Andy.request_action(1953)
        self.assertEqual(cm.exception.args[0], messages.player_not_str_action_message.format(int.__name__))


        # Invalid values

        with self.assertRaises(ValueError) as cm:
            Andy.request_action('drink')
        self.assertEqual(cm.exception.args[0], messages.betting_round_undefined_action_message.format('drink'))


    def test_deliver_card_method(self):


        """
        Runs test cases on deliver_card method.
        """


        Andy = structures.Player('Andy')


        # Valid inputs

        Andy.deliver_card(structures.Card('A', 's'))


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            Andy.deliver_card('As')
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


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            Andy.assign_hand(structures.Card('J', 's'))
        self.assertEqual(cm.exception.args[0], messages.player_not_hand_instance_message.format(structures.Card.__name__))


if __name__ == '__main__':
    main()