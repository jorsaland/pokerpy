"""
Defines unit tests on Hand relations.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, structures


class TestRelationsBetweenDifferentCategories(TestCase):


    "Runs test cases to compare hands of different categories."


    hands = [
        royal_flush := structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.SPADES),
        )),
        straight_flush := structures.Hand((
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.ACES, constants.SPADES),
        )),
        four_of_a_kind := structures.Hand((
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.SIXES, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.SPADES),
        )),
        full_house := structures.Hand((
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.HEARTS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.SPADES),
            structures.Card(constants.NINES, constants.DIAMONDS),
        )),
        flush := structures.Hand((
            structures.Card(constants.NINES, constants.HEARTS),
            structures.Card(constants.EIGHTS, constants.HEARTS),
            structures.Card(constants.SEVENS, constants.HEARTS),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.FOURS, constants.HEARTS),
        )),
        straight := structures.Hand((
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.NINES, constants.HEARTS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.SPADES),
            structures.Card(constants.SIXES, constants.DIAMONDS),
        )),
        three_of_a_kind := structures.Hand((
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        )),
        two_pair := structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.DIAMONDS),
        )),
        one_pair := structures.Hand((
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.SPADES),
        )),
        high_card := structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.NINES, constants.HEARTS),
        )),
    ]


    def test_compare_hands_from_different_categories(self):

        "Tests comparison of hands from different categories."

        for i, hand in enumerate(self.hands):
            for lower_hand in self.hands[i+1 :]:
                with self.subTest(higher_hand=str(hand), lower_hand=str(lower_hand)):
                    self.assertGreater(hand, lower_hand)
                    self.assertGreaterEqual(hand, lower_hand)


class TestRoyalFlushRelations(TestCase):


    "Runs test cases to compare royal flush hands."


    def test_royal_flush_comparison(self):

        "Tests comparison between royal flush hands."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.SPADES),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.TENS, constants.CLUBS),
        ))

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestStraightFlushRelations(TestCase):


    "Runs test cases to compare straight flush hands."


    def test_straight_flush_comparison_to_same_high_card(self):

        "Tests comparison of a straight flush hand to another that shares the same high card value."

        hand_1 = structures.Hand((
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.NINES, constants.HEARTS),
            structures.Card(constants.EIGHTS, constants.HEARTS),
            structures.Card(constants.SEVENS, constants.HEARTS),
        ))

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_flush_comparison_to_lower_high_card(self):

        "Tests comparison of a straight flush hand to another that has lower high card."

        hand_1 = structures.Hand((
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.DIAMONDS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_flush_comparison_to_five_high(self):

        "Tests comparison of a straight flush hand to a five-high flush straight."

        hand_1 = structures.Hand((
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.ACES, constants.SPADES),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestFourOfAKindRelations(TestCase):


    "Runs test cases to compare four of a kind hands."


    def test_four_of_a_kind_comparison_to_same_repeated_cards_and_kicker(self):

        "Tests comparison of a four of a kind hand to another with the same repeated cards and kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.SPADES),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.CLUBS),
        ))
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_four_of_a_kind_comparison_to_same_repeated_cards_lower_kicker(self):

        "Tests comparison of a four of a kind hand to another with the same repeated cards, but lower kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.SPADES),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.DEUCES, constants.CLUBS),
        ))
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_four_of_a_kind_comparison_to_lower_repeated_cards_higher_kicker(self):

        "Tests comparison of a four of a kind hand to another with lower repeated cards, but higher kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.SPADES),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.FOURS, constants.HEARTS),
            structures.Card(constants.FOURS, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.CLUBS),
            structures.Card(constants.KINGS, constants.CLUBS),
        ))
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestFullHouseRelations(TestCase):


    "Runs test cases to compare full house hands."


    def test_full_house_comparison_to_same_three_of_a_kind_and_pair(self):

        "Tests comparison of a full house hand to another with the same three of a kind and pair."

        hand_1 = structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.HEARTS),
        ))
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_full_house_comparison_to_same_three_of_a_kind_lower_pair(self):

        "Tests comparison of a full house hand to another with the same three of a kind, but lower pair."

        hand_1 = structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.THREES, constants.CLUBS),
        ))
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_full_house_comparison_to_lower_three_of_a_kind_higher_pair(self):

        "Tests comparison of a full house hand to another with lower three of a kind, but higher pair."

        hand_1 = structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.NINES, constants.SPADES),
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.CLUBS),
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
        ))
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_full_house_comparison_to_lower_three_of_a_kind_and_pair(self):

        "Tests comparison of a full house hand to another with lower three of a kind and pair."

        hand_1 = structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.NINES, constants.SPADES),
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.CLUBS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.THREES, constants.CLUBS),
        ))
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestFlushRelations(TestCase):


    "Runs test cases to compare flush hands."


    def test_flush_comparison_to_same_values(self):

        "Tests comparison of a flush hand to another with the same values."

        hand_1 = structures.Hand((
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.HEARTS),
            structures.Card(constants.SEVENS, constants.HEARTS),
            structures.Card(constants.FOURS, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.HEARTS),
        ))

        hand_2 = structures.Hand((
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_flush_comparison_to_lower_high_card_higher_kickers(self):

        "Tests comparison of a flush hand to another with lower high card but higher kickers."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.SPADES),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.JACKS, constants.CLUBS),
            structures.Card(constants.NINES, constants.CLUBS),
            structures.Card(constants.EIGHTS, constants.CLUBS),
        ))
  
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestStraightRelations(TestCase):


    "Runs test cases to compare straight hands."


    def test_straight_comparison_to_same_high_card(self):

        "Tests comparison of a straight hand to another with the same values."

        hand_1 = structures.Hand((
            structures.Card(constants.SEVENS, constants.SPADES),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.FIVES, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.THREES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.SEVENS, constants.SPADES),
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.FIVES, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.CLUBS),
            structures.Card(constants.THREES, constants.DIAMONDS),
        ))

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_comparison_to_lower_high_card(self):

        "Tests comparison of a straight hand to another with lower high card."

        hand_1 = structures.Hand((
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FOURS, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.SPADES),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FOURS, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_comparison_to_five_high(self):

        "Tests comparison of a straight hands to a five-high straight."

        hand_1 = structures.Hand((
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.EIGHTS, constants.HEARTS),
            structures.Card(constants.SEVENS, constants.DIAMONDS),
            structures.Card(constants.SIXES, constants.SPADES),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.ACES, constants.CLUBS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestThreeOfAKindRelations(TestCase):


    "Runs test cases to compare three of a kind hands."


    def test_three_of_a_kind_comparison_to_same_repeated_cards_and_kickers(self):

        "Tests comparison of a three of a kind hand to another with the same repeated cards and kickers."

        hand_1 = structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.SEVENS, constants.SPADES),
            structures.Card(constants.FOURS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.HEARTS),
            structures.Card(constants.FOURS, constants.CLUBS),
        ))

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_three_of_a_kind_comparison_to_same_repeated_cards_lower_1_kicker_higher_2_kicker(self):

        "Tests comparison of a three of a kind hand to another with the same repeated cards, but lower first kicker and higher second kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.NINES, constants.HEARTS),
            structures.Card(constants.FIVES, constants.CLUBS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_three_of_a_kind_comparison_to_lower_repeated_cards_higher_kickers(self):

        "Tests comparison of a three of a kind hand to another with lower repeated cards, but higher kickers."

        hand_1 = structures.Hand((
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.NINES, constants.CLUBS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestTwoPairRelations(TestCase):


    "Runs test cases to compare two pair hands."


    def test_two_pair_comparison_to_same_pairs_and_kicker(self):

        "Tests comparison of a two pair hand to another with the same pairs and kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.TENS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.CLUBS),
            structures.Card(constants.TENS, constants.DIAMONDS),
        ))

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_two_pair_comparison_to_same_pairs_lower_kicker(self):

        "Tests comparison of a two pair hand to another with the same pairs, but lower kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.CLUBS),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.NINES, constants.HEARTS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_two_pair_comparison_to_same_1_pair_lower_2_pair_higher_kicker(self):

        "Tests comparison of a two pair hand to another with the same first pair, but lower second pair and higher kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.TENS, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.KINGS, constants.HEARTS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_two_pair_comparison_to_lower_1_pair_higher_2_pair_and_kicker(self):

        "Tests comparison of a two pair hand to another with lower first pair, but higher second pair and kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.CLUBS),
            structures.Card(constants.DEUCES, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.CLUBS),
            structures.Card(constants.SIXES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.HEARTS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestPairRelations(TestCase):


    "Runs test cases to compare pair hands."


    def test_pair_comparison_to_same_pair_and_kickers(self):

        "Tests comparison of a pair hand to another with the same pair and kickers."

        hand_1 = structures.Hand((
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.THREES, constants.DIAMONDS),
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.FOURS, constants.CLUBS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_pair_comparison_to_same_pair_and_1_2_kickers_lower_3_kicker(self):

        "Tests comparison of a pair hand to another with the same pair, first kicker and second kicker, but lower third kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.HEARTS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        ))

        hand_2 = structures.Hand((
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.QUEENS, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.HEARTS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_pair_comparison_to_same_pair_and_1_kicker_lower_2_kicker_higher_3_kicker(self):

        "Tests comparison of a pair hand to another with the same pair and first kicker, but lower second kicker and higher third kicker."

        hand_1 = structures.Hand((
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.HEARTS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))

        hand_2 = structures.Hand((
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.FIVES, constants.CLUBS),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.NINES, constants.DIAMONDS),
            structures.Card(constants.SIXES, constants.HEARTS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_pair_comparison_to_same_pair_lower_1_kicker_higher_2_3_kickers(self):

        "Tests comparison of a pair hand to another with the same pair, but lower first kicker and higher second and third kickers."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.HEARTS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_pair_comparison_to_lower_pair_higher_kickers(self):

        "Tests comparison of a pair hand to another with lower pair, but higher kickers."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.FOURS, constants.CLUBS),
            structures.Card(constants.THREES, constants.HEARTS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.QUEENS, constants.HEARTS),
            structures.Card(constants.JACKS, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.HEARTS),
        ))

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


class TestHighCardRelations(TestCase):


    "Runs test cases to compare high card hands."


    def test_high_card_comparison_to_same_values(self):

        "Tests comparison of a high card hand to another with the same values."

        hand_1 = structures.Hand((
            structures.Card(constants.TENS, constants.SPADES),
            structures.Card(constants.EIGHTS, constants.HEARTS),
            structures.Card(constants.FIVES, constants.DIAMONDS),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))

        hand_2 = structures.Hand((
            structures.Card(constants.TENS, constants.HEARTS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.THREES, constants.CLUBS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_high_card_comparison_to_lower_high_card_higher_kickers(self):

        "Tests comparison of a high card hand to another with lower high card but higher kickers."

        hand_1 = structures.Hand((
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.SIXES, constants.DIAMONDS),
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.THREES, constants.CLUBS),
            structures.Card(constants.DEUCES, constants.DIAMONDS),
        ))
        hand_2 = structures.Hand((
            structures.Card(constants.SEVENS, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.EIGHTS, constants.DIAMONDS),
        ))
  
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


if __name__ == '__main__':
    main()