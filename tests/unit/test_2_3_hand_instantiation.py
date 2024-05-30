"""
Defines unit tests on Hand instantiation.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestHandInstantiation(TestCase):


    """
    Runs unit tests on Hand class instantiation.
    """


    def test_instantiation(self):


        """
        Runs test cases to check if hand instantiation works as expected.
        """


        # Valid inputs

        pk.Hand([ ## list
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ])

        pk.Hand(( ## tuple
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ))

        pk.Hand({ ## set
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        })

        def generator():
            yield pk.Card('A', 's')
            yield pk.Card('K', 's')
            yield pk.Card('Q', 's')
            yield pk.Card('J', 's')
            yield pk.Card('T', 's')
        pk.Hand(generator())


        # Invalid input types

        with self.assertRaises(TypeError) as cm:
            pk.Hand(98765)
        self.assertEqual(cm.exception.args[0], pk.messages.hand_not_iterable_object_cards_message.format(int.__name__))

        with self.assertRaises(TypeError) as cm:
            pk.Hand('98765')
        self.assertEqual(cm.exception.args[0], pk.messages.hand_not_all_card_instances_message.format(str.__name__))

        with self.assertRaises(TypeError) as cm:
            pk.Hand(['Ah', pk.Card('A', 's')])
        self.assertEqual(cm.exception.args[0], pk.messages.hand_not_all_card_instances_message)


if __name__ == '__main__':
    main()