"""
Defines unit tests on Hand instantiation.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import messages, structures


class TestHandInstantiation(TestCase):


    """
    Runs unit tests on Hand class instantiation.
    """


    def test_instantiation(self):


        """
        Runs test cases to check if hand instantiation works as expected.
        """


        # Valid inputs

        structures.Hand([ ## list
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ])

        structures.Hand(( ## tuple
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ))

        structures.Hand({ ## set
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        })

        def generator():
            yield structures.Card('A', 's')
            yield structures.Card('K', 's')
            yield structures.Card('Q', 's')
            yield structures.Card('J', 's')
            yield structures.Card('T', 's')
        structures.Hand(generator())


        # Invalid input types

        with self.assertRaises(TypeError) as cm:
            structures.Hand(98765)
        self.assertEqual(cm.exception.args[0], messages.hand_not_iterable_object_cards_message.format(int.__name__))

        with self.assertRaises(TypeError) as cm:
            structures.Hand('98765')
        self.assertEqual(cm.exception.args[0], messages.hand_not_all_card_instances_message.format(str.__name__))

        with self.assertRaises(TypeError) as cm:
            structures.Hand(['Ah', structures.Card('A', 's')])
        self.assertEqual(cm.exception.args[0], messages.hand_not_all_card_instances_message)


if __name__ == '__main__':
    main()