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
        self.assertEqual(cm.exception.args[0], messages.not_str_player_name_message.format(int.__name__))
        
        with self.assertRaises(TypeError) as cm:
            structures.Player(['Andy'])
        self.assertEqual(cm.exception.args[0], messages.not_str_player_name_message.format(list.__name__))


    def test_request_method(self):


        """
        Runs test cases on request method.
        """


        Andy = structures.Player('Andy')


        # Valid inputs

        Andy.request(constants.ACTION_BET)
        Andy.request(constants.ACTION_CALL)
        Andy.request(constants.ACTION_CHECK)
        Andy.request(constants.ACTION_FOLD)
        Andy.request(constants.ACTION_RAISE)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            Andy.request(1953)
        self.assertEqual(cm.exception.args[0], messages.not_str_action_message.format(int.__name__))


        # Invalid values

        with self.assertRaises(ValueError) as cm:
            Andy.request('drink')
        self.assertEqual(cm.exception.args[0], messages.undefined_action_message.format('drink'))


if __name__ == '__main__':
    main()