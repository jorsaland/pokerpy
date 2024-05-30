"""
Defines unit tests on Player class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestPlayerClass(TestCase):


    """
    Runs unit tests on Player class.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation.
        """


        # Valid inputs

        pk.Player('Andy')


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            pk.Player(1933)
        self.assertEqual(cm.exception.args[0], pk.messages.not_str_player_name_message.format(int.__name__))
        
        with self.assertRaises(TypeError) as cm:
            pk.Player(['Andy'])
        self.assertEqual(cm.exception.args[0], pk.messages.not_str_player_name_message.format(list.__name__))


    def test_request_action_method(self):


        """
        Runs test cases on request_action method.
        """


        Andy = pk.Player('Andy')


        # Valid inputs

        Andy.request_action(pk.ACTION_BET)
        Andy.request_action(pk.ACTION_CALL)
        Andy.request_action(pk.ACTION_CHECK)
        Andy.request_action(pk.ACTION_FOLD)
        Andy.request_action(pk.ACTION_RAISE)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            Andy.request_action(1953)
        self.assertEqual(cm.exception.args[0], pk.messages.not_str_action_message.format(int.__name__))


        # Invalid values

        with self.assertRaises(ValueError) as cm:
            Andy.request_action('drink')
        self.assertEqual(cm.exception.args[0], pk.messages.undefined_action_message.format('drink'))


    def test_deliver_card_method(self):


        """
        Runs test cases on deliver_card method.
        """


        Andy = pk.Player('Andy')


        # Valid inputs

        Andy.deliver_card(pk.Card('A', 's'))


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            Andy.deliver_card('As')
        self.assertEqual(cm.exception.args[0], pk.messages.not_card_instance_message.format(str.__name__))


    def test_assign_hand_method(self):


        """
        Runs test cases on assign_hand method.
        """


        Andy = pk.Player('Andy')


        # Valid inputs

        Andy.assign_hand(pk.Hand([
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ]))


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            Andy.assign_hand(pk.Card('J', 's'))
        self.assertEqual(cm.exception.args[0], pk.messages.not_hand_instance_message.format(pk.Card.__name__))


if __name__ == '__main__':
    main()