"""
Defines unit tests on Hand instantiation.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestHandInstantiation(TestCase):


    "Runs unit tests on hand instantiation."


    def test_cards_whole_input_type_error(self):

        "Tests type error detection on the whole input of field cards."

        bad_values = (1, None)

        for bad_value in bad_values:

            with self.subTest(value=bad_value):
                with self.assertRaises(TypeError) as cm:
                    structures.Hand(bad_value)
                self.assertEqual(cm.exception.args[0], messages.msg_not_iterable_object.format(type(bad_value).__name__))


    def test_cards_items_type_error(self):

        "Tests type error detection on one of the items of field cards."

        bad_cards_1 = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.HEARTS),
            'tens',
        )

        bad_cards_2 = (
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.CLUBS),
            None,
        )

        bad_cards_3 = 'strings are iterable'

        bad_cards_4 = [1, 2, 3]

        for bad_card_set in (bad_cards_1, bad_cards_2, bad_cards_3, bad_cards_4):

            with self.subTest(cards=bad_card_set):
                with self.assertRaises(TypeError) as cm:
                    structures.Hand(bad_card_set)
                self.assertEqual(cm.exception.args[0], messages.msg_not_all_card_instances)


    def test_valid_instantiation(self):

        "Tests valid instantiation."

        cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.SPADES),
        )

        for data_type in (tuple, list, set):
            hand = structures.Hand(data_type(cards))
            with self.subTest(data_type.__name__):
                self.assertEqual(hand.cards, cards)
                self.assertEqual(hand.category, constants.ROYAL_FLUSH)


if __name__ == '__main__':
    main()