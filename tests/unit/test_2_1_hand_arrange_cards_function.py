"""
Defines unit tests on arrange_cards function.
"""


import sys
sys.path.insert(0, '.')


from itertools import permutations
from unittest import main, TestCase


from pokerpy import constants, messages, structures


class PermutationTestCase(TestCase):


    "Base class to for test cases that require permutation on cards."


    def run_permutations_subtests(self, expected_arrangement: tuple[structures.Card, ...]):

        "Runs the subtests that require permutations on cards."

        for permutation in permutations(expected_arrangement):

            arranged_cards = structures.arrange_cards(permutation)

            with self.subTest(
                permutation = ''.join(str(c) for c in permutation),
                result = ''.join(str(c) for c in arranged_cards),
                expected = ''.join(str(c) for c in expected_arrangement),
            ):
                self.assertEqual(arranged_cards, expected_arrangement)


class TestHandArrangeCardsFunctionInput(TestCase):


    "Runs unit tests on arrange_cards function input."


    def test_value_error(self):

        "Tests value error detection."

        no_cards = ()

        less_than_5_cards = (
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.CLUBS),
            structures.Card(constants.SIXES, constants.SPADES),
        )

        more_than_5_cards = (
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.SEVENS, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.TENS, constants.CLUBS),
        )

        repeated_cards = (
            structures.Card(constants.DEUCES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.CLUBS),
        )

        for card_set in (no_cards, less_than_5_cards, more_than_5_cards):

            with self.subTest('not five cards', cards_count=len(card_set)):
                with self.assertRaises(ValueError) as cm:
                    structures.arrange_cards(card_set)
                self.assertEqual(cm.exception.args[0], messages.msg_not_five_cards_hand)

        with self.subTest('repeated cards', cards_count=len(repeated_cards)):
            with self.assertRaises(ValueError) as cm:
                structures.arrange_cards(repeated_cards)
            self.assertEqual(cm.exception.args[0], messages.msg_repeated_cards)


    def test_valid_input(self):

        "Tests valid input."

        cards = (
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.FOURS, constants.CLUBS),
        )

        structures.arrange_cards(cards)


class TestHandArrangeCardsFunctionWithFourOfAKind(PermutationTestCase):


    "Runs unit tests on arrange_cards function with four of a kind."


    def test_four_of_a_kind_higher_than_unpaired_card(self):

        "Tests arrangement when the four of a kind is of higher value than the unpaired card."

        expected_arrangement = (
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.HEARTS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_four_of_a_kind_lower_than_unpaired_card(self):

        "Tests arrangement when the four of a kind is of lower value than the unpaired card."

        expected_arrangement = (
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.THREES, constants.CLUBS),
            structures.Card(constants.TENS, constants.CLUBS),
        )
        self.run_permutations_subtests(expected_arrangement)


class TestHandArrangeCardsFunctionWithThreeOfAKind(PermutationTestCase):


    "Runs unit tests on arrange_cards function with three of a kind."


    def test_three_of_a_kind_higher_than_pair(self):

        "Tests arrangement when the three of a kind is of higher value than a pair."

        expected_arrangement = (
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.FOURS, constants.DIAMONDS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_three_of_a_kind_lower_than_pair(self):

        "Tests arrangement when the three of a kind is of lower value than a pair."

        expected_arrangement = (
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.HEARTS),
            structures.Card(constants.FIVES, constants.CLUBS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_three_of_a_kind_higher_than_unpaired_cards(self):

        "Tests arrangement when the three of a kind is of higher value than both unpaired cards."

        expected_arrangement = (
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.CLUBS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.HEARTS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_three_of_a_kind_between_unpaired_cards(self):

        "Tests arrangement when the three of a kind value is in between of the values of both unpaired cards."

        expected_arrangement = (
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.SIXES, constants.HEARTS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_three_of_a_kind_lower_than_unpaired_cards(self):

        "Tests arrangement when the three of a kind is of lower value than both unpaired cards."

        expected_arrangement = (
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.SPADES),
            structures.Card(constants.SIXES, constants.HEARTS),
        )
        self.run_permutations_subtests(expected_arrangement)


class TestHandArrangeCardsFunctionWithPairs(PermutationTestCase):


    "Runs unit tests on arrange_cards function with pairs."


    def test_two_pairs_higher_than_unpaired_card(self):

        "Tests arrangement when two pairs are of higher value than the unpaired card."

        expected_arrangement = (
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.CLUBS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_unpaired_card_between_two_pairs(self):

        "Tests arrangement when an unpaired card value is in between the values of two pairs."

        expected_arrangement = (
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.JACKS, constants.SPADES),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_two_pairs_lower_than_unpaired_card(self):

        "Tests arrangement when two pairs are of lower value than the unpaired card."

        expected_arrangement = (
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.HEARTS),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_pair_higher_than_unpaired_cards(self):

        "Tests arrangement when a pair is of higher value than all the unpaired cards."

        expected_arrangement = (
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_pair_higher_than_two_unpaired_cards(self):

        "Tests arrangement when a pair is of higher value than two unpaired cards and lower than the other."

        expected_arrangement = (
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.NINES, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_pair_lower_than_two_unpaired_cards(self):

        "Tests arrangement when a pair is of lower value than two unpaired cards and higher than the other."

        expected_arrangement = (
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.SIXES, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.THREES, constants.DIAMONDS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_pair_lower_than_unpaired_cards(self):

        "Tests arrangement when a pair is of lower value than all the unpaired cards."

        expected_arrangement = (
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.SPADES),
        )
        self.run_permutations_subtests(expected_arrangement)


class TestHandArrangeCardsFunctionWithUnpairedCards(PermutationTestCase):


    "Runs unit tests on arrange_cards function with unpaired cards."


    def test_ace_high_straight(self):

        "Tests arrangement when there is an ace-high straight."

        expected_arrangement = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.TENS, constants.SPADES),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_five_high_straight(self):

        "Tests arrangement when there is a five-high straight."

        expected_arrangement = (
            structures.Card(constants.FIVES, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.CLUBS),
            structures.Card(constants.ACES, constants.CLUBS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_intermediate_straight(self):

        "Tests arrangement when there is a straight at an intermediate point."

        expected_arrangement = (
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.DIAMONDS),
        )
        self.run_permutations_subtests(expected_arrangement)


    def test_no_straight(self):

        "Tests arrangement when cards do not match a straight."

        expected_arrangement = (
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.CLUBS),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.THREES, constants.SPADES),
        )
        self.run_permutations_subtests(expected_arrangement)


if __name__ == '__main__':
    main()