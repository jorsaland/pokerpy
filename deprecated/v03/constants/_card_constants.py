"""
Defines the constants regarding to actions used when playing.
"""


# Values and suits

sorted_card_values: tuple[str] = (
    (DEUCES := '2'),
    (THREES := '3'),
    (FOURS := '4'),
    (FIVES := '5'),
    (SIXES := '6'),
    (SEVENS := '7'),
    (EIGHTS := '8'),
    (NINES := '9'),
    (TENS := 'T'),
    (JACKS := 'J'),
    (QUEENS := 'Q'),
    (KINGS := 'K'),
    (ACES := 'A'),
)

sorted_card_suits: tuple[str] = (
    (CLUBS := 'c'),
    (DIAMONDS := 'd'),
    (HEARTS := 'h'),
    (SPADES := 's'),
)

unicode_code_point_by_card_suit = {
    CLUBS: (CLUBS_UNICODE_CODE_POINT := 9827),
    DIAMONDS: (DIAMONDS_UNICODE_CODE_POINT := 9830), ## black: 9830 / white: 9826
    HEARTS: (HEARTS_UNICODE_CODE_POINT := 9829), ## black: 9829 / white: 9825
    SPADES: (SPADES_UNICODE_CODE_POINT := 9824),
}

full_sorted_values_and_suits: tuple[tuple[str, str], ...] = tuple((value, suit) for value in sorted_card_values for suit in sorted_card_suits)


# Hands

sorted_hand_categories: tuple[str] = (
    (HIGH_CARD := 'high card'),
    (ONE_PAIR := 'pair'),
    (TWO_PAIR := 'two pair'),
    (THREE_OF_A_KIND := 'three of a kind'),
    (STRAIGHT := 'straight'),
    (FLUSH := 'flush'),
    (FULL_HOUSE := 'full house'),
    (FOUR_OF_A_KIND := 'four of a kind'),
    (STRAIGHT_FLUSH := 'straight flush'),
    (ROYAL_FLUSH := 'royal flush'),
)