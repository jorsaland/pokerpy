"""
Defines the constants regarding to actions used when playing.
"""


# Values and suits

sorted_card_values = [
    (DEUCE := '2'),
    (THREE := '3'),
    (FOUR := '4'),
    (FIVE := '5'),
    (SIX := '6'),
    (SEVEN := '7'),
    (EIGHT := '8'),
    (NINE := '9'),
    (TEN := 'T'),
    (JACK := 'J'),
    (QUEEN := 'Q'),
    (KING := 'K'),
    (ACE := 'A'),
]

sorted_card_suits = [
    (CLUBS := 'c'),
    (DIAMONDS := 'd'),
    (HEARTS := 'h'),
    (SPADES := 's'),
]

unicode_code_point_by_card_suit = {
    CLUBS: (CLUBS_UNICODE_CODE_POINT := 9827),
    DIAMONDS: (DIAMONDS_UNICODE_CODE_POINT := 9830), ## black: 9830 / white: 9826
    HEARTS: (HEARTS_UNICODE_CODE_POINT := 9829), ## black: 9829 / white: 9825
    SPADES: (SPADES_UNICODE_CODE_POINT := 9824),
}


# Hands

sorted_hand_names = [
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
]