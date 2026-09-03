"""
Defines unit tests on get_category function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, structures


class TestHandGetCategoryWithRoyalFlush(TestCase):


    "Runs unit tests on get_category function with royal flush."


    def test_royal_flush(self):

        "Tests royal flush."

        for suit in constants.sorted_card_suits:
            cards = (
                structures.Card(constants.ACES, suit),
                structures.Card(constants.KINGS, suit),
                structures.Card(constants.QUEENS, suit),
                structures.Card(constants.JACKS, suit),
                structures.Card(constants.TENS, suit),
            )
            with self.subTest(suit=suit):
                self.assertEqual(structures.get_category(cards), constants.ROYAL_FLUSH)


class TestHandGetCategoryWithStraightFlush(TestCase):


    "Runs unit tests on get_category function with straight flush."


    def test_king_high_straight_flush(self):

        "Tests king-high straight flush."

        for suit in constants.sorted_card_suits:
            cards = (
                structures.Card(constants.KINGS, suit),
                structures.Card(constants.QUEENS, suit),
                structures.Card(constants.JACKS, suit),
                structures.Card(constants.TENS, suit),
                structures.Card(constants.NINES, suit),
            )
            with self.subTest(suit=suit):
                self.assertEqual(structures.get_category(cards), constants.STRAIGHT_FLUSH)


    def test_five_high_straight_flush(self):

        "Tests five-high straight flush."

        for suit in constants.sorted_card_suits:
            cards = (
                structures.Card(constants.FIVES, suit),
                structures.Card(constants.FOURS, suit),
                structures.Card(constants.THREES, suit),
                structures.Card(constants.DEUCES, suit),
                structures.Card(constants.ACES, suit),
            )
            with self.subTest(suit=suit):
                self.assertEqual(structures.get_category(cards), constants.STRAIGHT_FLUSH)


    def test_intermediate_straight_flush(self):

        "Tests an intermediate straight flush."

        for suit in constants.sorted_card_suits:
            cards = (
                structures.Card(constants.NINES, suit),
                structures.Card(constants.EIGHTS, suit),
                structures.Card(constants.SEVENS, suit),
                structures.Card(constants.SIXES, suit),
                structures.Card(constants.FIVES, suit),
            )
            with self.subTest(suit=suit):
                self.assertEqual(structures.get_category(cards), constants.STRAIGHT_FLUSH)


class TestHandGetCategoryFunctionWithFourOfAKind(TestCase):


    "Runs unit tests on get_category function with four of a kind."


    def test_four_of_a_kind_higher_than_unpaired_card(self):

        "Tests four of a kind when it is of higher value than the unpaired card."

        cards = (
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.HEARTS),
        )
        self.assertEqual(structures.get_category(cards), constants.FOUR_OF_A_KIND)


    def test_four_of_a_kind_lower_than_unpaired_card(self):

        "Tests four of a kind when it is of lower value than the unpaired card."

        cards = (
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.THREES, constants.CLUBS),
            structures.Card(constants.TENS, constants.CLUBS),
        )
        self.assertEqual(structures.get_category(cards), constants.FOUR_OF_A_KIND)


class TestHandGetCategoryFunctionWithFullHouse(TestCase):


    "Runs unit tests on get_category function with full house."


    def test_full_house_higher_than_pair(self):

        "Tests full house when the three of a kind is of higher value than the pair."

        cards = (
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.FOURS, constants.DIAMONDS),
        )
        self.assertEqual(structures.get_category(cards), constants.FULL_HOUSE)


    def test_full_house_lower_than_pair(self):

        "Tests full house when the three of a kind is of lower value than the pair."

        cards = (
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.HEARTS),
            structures.Card(constants.FIVES, constants.CLUBS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
        )
        self.assertEqual(structures.get_category(cards), constants.FULL_HOUSE)


class TestHandGetCategoryFunctionWithFlush(TestCase):


    "Runs unit tests on get_category function with flush."


    def test_flush_close_to_straight_flush(self):

        "Tests flush when it is close to looking like a straight flush."

        for suit in constants.sorted_card_suits:
            cards = (
                structures.Card(constants.QUEENS, suit),
                structures.Card(constants.JACKS, suit),
                structures.Card(constants.TENS, suit),
                structures.Card(constants.NINES, suit),
                structures.Card(constants.SEVENS, suit),
            )
            with self.subTest(suit=suit):
                self.assertEqual(structures.get_category(cards), constants.FLUSH)


    def test_flush_far_from_straight_flush(self):

        "Tests flush when it is far from looking like a straight flush."

        for suit in constants.sorted_card_suits:
            cards = (
                structures.Card(constants.KINGS, suit),
                structures.Card(constants.NINES, suit),
                structures.Card(constants.SEVENS, suit),
                structures.Card(constants.FOURS, suit),
                structures.Card(constants.DEUCES, suit),
            )
            with self.subTest(suit=suit):
                self.assertEqual(structures.get_category(cards), constants.FLUSH)


class TestHandGetCategoryFunctionWithStraight(TestCase):


    "Runs unit tests on get_category function with straight."


    def test_ace_high_straight(self):

        "Tests ace-high straight."

        cards = (
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.SPADES),
        )
        self.assertEqual(structures.get_category(cards), constants.STRAIGHT)


    def test_five_high_straight(self):

        "Tests five-high straight."

        cards = (
            structures.Card(constants.FIVES, constants.HEARTS),
            structures.Card(constants.FOURS, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )
        self.assertEqual(structures.get_category(cards), constants.STRAIGHT)


    def test_straight_close_to_straight_flush(self):

        "Tests straight when it is close to looking like a straight flush."

        cards = (
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.HEARTS),
            structures.Card(constants.SEVENS, constants.HEARTS),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.FIVES, constants.HEARTS),
        )
        self.assertEqual(structures.get_category(cards), constants.STRAIGHT)


    def test_intermediate_straight(self):

        "Tests straight when it is a normal straight."

        cards = (
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.HEARTS),
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.FIVES, constants.HEARTS),
        )
        self.assertEqual(structures.get_category(cards), constants.STRAIGHT)


class TestHandGetCategoryFunctionWithThreeOfAKind(TestCase):


    "Runs unit tests on get_category function with three of a kind."


    def test_three_of_a_kind_higher_than_unpaired_cards(self):

        "Tests three of a kind when it is of higher value than both unpaired cards."

        cards = (
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.CLUBS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.HEARTS),
        )
        self.assertEqual(structures.get_category(cards), constants.THREE_OF_A_KIND)


    def test_three_of_a_kind_between_unpaired_cards(self):

        "Tests three of a kind value when its value is in between of the values of both unpaired cards."

        cards = (
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.SIXES, constants.HEARTS),
        )
        self.assertEqual(structures.get_category(cards), constants.THREE_OF_A_KIND)


    def test_three_of_a_kind_lower_than_unpaired_cards(self):

        "Tests three of a kind when it is of lower value than both unpaired cards."

        cards = (
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.SPADES),
            structures.Card(constants.SIXES, constants.HEARTS),
        )
        self.assertEqual(structures.get_category(cards), constants.THREE_OF_A_KIND)


class TestHandGetCategoryFunctionWithTwoPair(TestCase):


    "Runs unit tests on get_category function with two pair."


    def test_two_pairs_higher_than_unpaired_card(self):

        "Tests two pair when they are of higher value than the unpaired card."

        cards = (
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.CLUBS),
        )
        self.assertEqual(structures.get_category(cards), constants.TWO_PAIR)


    def test_unpaired_card_between_two_pairs(self):

        "Tests two pair when the unpaired card value is in between of the two pair values."

        cards = (
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.JACKS, constants.SPADES),
        )
        self.assertEqual(structures.get_category(cards), constants.TWO_PAIR)


    def test_two_pairs_lower_than_unpaired_card(self):

        "Tests two pair when they are of lower value than the unpaired card."

        cards = (
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.HEARTS),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
        )
        self.assertEqual(structures.get_category(cards), constants.TWO_PAIR)


class TestHandGetCategoryFunctionWithPair(TestCase):


    "Runs unit tests on get_category function with pair."


    def test_pair_higher_than_unpaired_cards(self):

        "Tests pair when it is of higher value than all the unpaired cards."

        cards = (
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        )
        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


    def test_pair_higher_than_two_unpaired_cards(self):

        "Tests pair when it is of higher value than two unpaired cards and lower than the other."

        cards = (
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.NINES, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        )
        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


    def test_pair_lower_than_two_unpaired_cards(self):

        "Tests pair when it is of lower value than two unpaired cards and higher than the other."

        cards = (
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.SIXES, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.THREES, constants.DIAMONDS),
        )
        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


    def test_pair_lower_than_unpaired_cards(self):

        "Tests pair when it is of lower value than all the unpaired cards."

        cards = (
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.SPADES),
        )
        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


class TestHandGetCategoryFunctionWithHighCard(TestCase):


    "Runs unit tests on get_category function with high card."


    def test_high_card_close_to_flush(self):

        "Tests high card when it is close to looking like a flush."

        cards = (
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
        )
        self.assertEqual(structures.get_category(cards), constants.HIGH_CARD)


    def test_high_card_close_to_straight(self):

        "Tests high card when it is close to looking like a straight."

        cards = (
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.SPADES),
            structures.Card(constants.SIXES, constants.CLUBS),
            structures.Card(constants.FIVES, constants.CLUBS),
            structures.Card(constants.THREES, constants.SPADES),
        )
        self.assertEqual(structures.get_category(cards), constants.HIGH_CARD)


    def test_high_card_making_wrap_around_straight(self):

        "Tests high card when it makes a wrap-around straight (not valid in poker)."

        cards = (
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.DEUCES, constants.CLUBS),
            structures.Card(constants.THREES, constants.SPADES),
        )
        self.assertEqual(structures.get_category(cards), constants.HIGH_CARD)


    def test_plain_high_card(self):

        "Tests high card when it is a normal high card."

        cards = (
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.SEVENS, constants.CLUBS),
            structures.Card(constants.FOURS, constants.CLUBS),
            structures.Card(constants.THREES, constants.SPADES),
        )
        self.assertEqual(structures.get_category(cards), constants.HIGH_CARD)


if __name__ == '__main__':
    main()