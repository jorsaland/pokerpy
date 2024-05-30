"""
Defines unit tests on arrange_cards function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import messages, structures


class TestHandArrangeCardsFunction(TestCase):


    """
    Runs unit tests on arrange_cards method.
    """


    def test_input(self):


        """
        Runs test cases to check input is valid.
        """


        # More cards than expected

        cards = [
            structures.Card('K', 'h'),
            structures.Card('7', 'h'),
            structures.Card('2', 'd'),
            structures.Card('5', 's'),
            structures.Card('K', 'c'),
            structures.Card('A', 'c'),
            structures.Card('T', 'c'),
        ]

        with self.assertRaises(ValueError) as cm:
            structures.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_not_five_cards_message)

        
        # Less cards than expected

        cards = [
            structures.Card('J', 'h'),
            structures.Card('2', 'c'),
            structures.Card('6', 's'),
        ]

        with self.assertRaises(ValueError) as cm:
            structures.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_not_five_cards_message)


        # No cards

        cards = []

        with self.assertRaises(ValueError) as cm:
            structures.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_not_five_cards_message)


        # Exactly five cards but some repeated

        cards = [
            structures.Card('2', 'd'),
            structures.Card('5', 's'),
            structures.Card('2', 'd'),
            structures.Card('5', 's'),
            structures.Card('T', 'c'),
        ]

        with self.assertRaises(ValueError) as cm:
            structures.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_repeated_cards_message)


    def test_four_of_a_kind_arrangements(self):


        """
        Runs test cases to check sets with four of a kind are arranged as expected.
        """


        # Four of a kind with higher value than unpaired card

        cards = [
            structures.Card('K', 'h'),
            structures.Card('7', 'h'),
            structures.Card('K', 'd'),
            structures.Card('K', 's'),
            structures.Card('K', 'c'),
        ]

        expected_arrangement = (
            structures.Card('K', 's'),
            structures.Card('K', 'h'),
            structures.Card('K', 'd'),
            structures.Card('K', 'c'),
            structures.Card('7', 'h'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Four of a kind with lower value than unpaired card

        cards = [
            structures.Card('3', 's'),
            structures.Card('T', 'h'),
            structures.Card('3', 'h'),
            structures.Card('3', 'c'),
            structures.Card('3', 'd'),
        ]

        expected_arrangement = (
            structures.Card('3', 's'),
            structures.Card('3', 'h'),
            structures.Card('3', 'd'),
            structures.Card('3', 'c'),
            structures.Card('T', 'h'),
        )
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


    def test_three_of_a_kind_arrangements(self):


        """
        Runs test cases to check sets with three of a kind are arranged as expected.
        """


        # Three of a kind with higher value than pair

        cards = [
            structures.Card('4', 's'),
            structures.Card('T', 'c'),
            structures.Card('T', 'd'),
            structures.Card('4', 'd'),
            structures.Card('T', 's'),
        ]

        expected_arrangement = (
            structures.Card('T', 's'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('4', 's'),
            structures.Card('4', 'd'),
        )

        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Three kind with lower value than pair

        cards = [
            structures.Card('5', 'h'),
            structures.Card('A', 'c'),
            structures.Card('5', 's'),
            structures.Card('A', 'd'),
            structures.Card('5', 'c'),
        ]

        expected_arrangement = (
            structures.Card('5', 's'),
            structures.Card('5', 'h'),
            structures.Card('5', 'c'),
            structures.Card('A', 'd'),
            structures.Card('A', 'c'),
        )

        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Three of a kind with higher value than unpaired cards

        cards = [
            structures.Card('5', 'c'),
            structures.Card('2', 'h'),
            structures.Card('5', 's'),
            structures.Card('3', 'd'),
            structures.Card('5', 'd'),
        ]

        expected_arrangement = (
            structures.Card('5', 's'),
            structures.Card('5', 'd'),
            structures.Card('5', 'c'),
            structures.Card('3', 'd'),
            structures.Card('2', 'h'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Three of a kind with value between single unpaired card values

        cards = [
            structures.Card('6', 'h'),
            structures.Card('J', 'c'),
            structures.Card('J', 's'),
            structures.Card('K', 'h'),
            structures.Card('J', 'h'),
        ]

        expected_arrangement = (
            structures.Card('J', 's'),
            structures.Card('J', 'h'),
            structures.Card('J', 'c'),
            structures.Card('K', 'h'),
            structures.Card('6', 'h'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Three of a kind with lower value than unpaired cards

        cards = [
            structures.Card('6', 'h'),
            structures.Card('2', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'h'),
            structures.Card('7', 's'),
        ]

        expected_arrangement = (
            structures.Card('2', 's'),
            structures.Card('2', 'h'),
            structures.Card('2', 'c'),
            structures.Card('7', 's'),
            structures.Card('6', 'h'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


    def test_pair_arrangements(self):


        """
        Runs test cases to check sets with pairs are arranged as expected.
        """


        # Two pairs with higher values than unpaired card

        cards = [
            structures.Card('7', 'c'),
            structures.Card('A', 'h'),
            structures.Card('8', 'c'),
            structures.Card('8', 's'),
            structures.Card('A', 'd'),
        ]

        expected_arrangement = (
            structures.Card('A', 'h'),
            structures.Card('A', 'd'),
            structures.Card('8', 's'),
            structures.Card('8', 'c'),
            structures.Card('7', 'c'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Single card with value between two pairs values

        cards = [
            structures.Card('J', 's'),
            structures.Card('Q', 's'),
            structures.Card('T', 's'),
            structures.Card('Q', 'c'),
            structures.Card('T', 'c'),
        ]

        expected_arrangement = (
            structures.Card('Q', 's'),
            structures.Card('Q', 'c'),
            structures.Card('T', 's'),
            structures.Card('T', 'c'),
            structures.Card('J', 's'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Two pairs with lower values than single card

        cards = [
            structures.Card('K', 'd'),
            structures.Card('5', 'h'),
            structures.Card('5', 's'),
            structures.Card('3', 'h'),
            structures.Card('3', 's'),
        ]

        expected_arrangement = (
            structures.Card('5', 's'),
            structures.Card('5', 'h'),
            structures.Card('3', 's'),
            structures.Card('3', 'h'),
            structures.Card('K', 'd'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Pair with higher values than unpaired cards

        cards = [
            structures.Card('7', 'd'),
            structures.Card('2', 'd'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('3', 'd'),
        ]

        expected_arrangement = (
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('7', 'd'),
            structures.Card('3', 'd'),
            structures.Card('2', 'd'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Pair with higher value than two unpaired cards and lower than a single unpaired card

        cards = [
            structures.Card('J', 'h'),
            structures.Card('J', 'c'),
            structures.Card('9', 's'),
            structures.Card('8', 'd'),
            structures.Card('A', 's'),
        ]

        expected_arrangement = (
            structures.Card('J', 'h'),
            structures.Card('J', 'c'),
            structures.Card('A', 's'),
            structures.Card('9', 's'),
            structures.Card('8', 'd'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Pair with higher value than a single unpaired card and lower than two unpaired cards

        cards = [
            structures.Card('Q', 'd'),
            structures.Card('J', 'c'),
            structures.Card('6', 'c'),
            structures.Card('3', 'd'),
            structures.Card('6', 's'),
        ]

        expected_arrangement = (
            structures.Card('6', 's'),
            structures.Card('6', 'c'),
            structures.Card('Q', 'd'),
            structures.Card('J', 'c'),
            structures.Card('3', 'd'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Pair with lower values than unpaired cards

        cards = [
            structures.Card('J', 's'),
            structures.Card('A', 'd'),
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('Q', 'h'),
        ]

        expected_arrangement = (
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('A', 'd'),
            structures.Card('Q', 'h'),
            structures.Card('J', 's'),
        )
        
        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


    def test_unpaired_arrangements(self):


        """
        Runs test cases to check sets with unpaired cards are arranged as expected.
        """


        # Straight flush

        cards = [
            structures.Card('6', 'h'),
            structures.Card('T', 'h'),
            structures.Card('7', 'h'),
            structures.Card('8', 'h'),
            structures.Card('9', 'h'),
        ]

        expected_arrangement = (
            structures.Card('T', 'h'),
            structures.Card('9', 'h'),
            structures.Card('8', 'h'),
            structures.Card('7', 'h'),
            structures.Card('6', 'h'),
        )

        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Special case: five to ace straight flush

        cards = [
            structures.Card('3', 'd'),
            structures.Card('4', 'd'),
            structures.Card('A', 'd'),
            structures.Card('5', 'd'),
            structures.Card('2', 'c'),
        ]

        expected_arrangement = (
            structures.Card('5', 'd'),
            structures.Card('4', 'd'),
            structures.Card('3', 'd'),
            structures.Card('2', 'd'),
            structures.Card('A', 'd'),
        )


        # Straight without flush

        cards = [
            structures.Card('K', 's'),
            structures.Card('A', 's'),
            structures.Card('J', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('T', 's'),
        ]

        expected_arrangement = (
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 'd'),
            structures.Card('J', 'h'),
            structures.Card('T', 's'),
        )

        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Special case: five to ace straight without flush

        cards = [
            structures.Card('3', 'd'),
            structures.Card('5', 'd'),
            structures.Card('A', 'c'),
            structures.Card('4', 's'),
            structures.Card('2', 'c'),
        ]

        expected_arrangement = (
            structures.Card('5', 'd'),
            structures.Card('4', 's'),
            structures.Card('3', 'd'),
            structures.Card('2', 'c'),
            structures.Card('A', 'c'),
        )

        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # Flush without straight

        cards = [
            structures.Card('K', 's'),
            structures.Card('9', 's'),
            structures.Card('2', 's'),
            structures.Card('7', 's'),
            structures.Card('6', 's'),
        ]

        expected_arrangement = (
            structures.Card('K', 's'),
            structures.Card('9', 's'),
            structures.Card('7', 's'),
            structures.Card('6', 's'),
            structures.Card('2', 's'),
        )

        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


        # No straight and no flush

        cards = [
            structures.Card('8', 'd'),
            structures.Card('3', 's'),
            structures.Card('J', 'c'),
            structures.Card('7', 'c'),
            structures.Card('4', 's'),
        ]

        expected_arrangement = (
            structures.Card('J', 'c'),
            structures.Card('8', 'd'),
            structures.Card('7', 'c'),
            structures.Card('4', 's'),
            structures.Card('3', 's'),
        )

        self.assertEqual(structures.arrange_cards(cards), expected_arrangement)


if __name__ == '__main__':
    main()