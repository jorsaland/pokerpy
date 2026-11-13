"""
Defines unit tests on functions related to placing blinds.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, messages, structures


class BaseTestCase(TestCase):


    "Base class for test cases that require a shared setup."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
        ]

        self.table = structures.Table(self.setup_players, min_bet=100)
        self.Andy, self.Boa, self.Coral = self.setup_players
        self.full_deck = tuple(structures.Card(value, suit) for value, suit in constants.sorted_card_values_and_suits)


class TestHandCycleDealCommonCardsFunction(BaseTestCase):


    "Runs unit tests on deal_common_cards function."


    def test_common_cards_skip_dealing(self):

        "Tests skipping dealing."

        generator = engines.deal_common_cards(self.table, 3)

        with self.subTest('generator await'):
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)
            next(generator)

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_not_exact_amount_of_cards.format(3))
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)


    def test_common_cards_parse_invalid_cards_amount(self):

        "Tests parsing an invalid amount of cards"

        cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        generator = engines.deal_common_cards(self.table, 3)

        with self.subTest('generator await'):
            await_state = next(generator)
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(cards)

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_not_exact_amount_of_cards.format(3))
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)


    def test_common_cards_parse_repeated_cards(self):

        "Tests parsing a repeated cards"

        cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        generator = engines.deal_common_cards(self.table, 3)

        with self.subTest('generator await'):
            await_state = next(generator)
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(cards)

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_repeated_cards)
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)


    def test_common_cards_parse_missing_cards(self):

        "Tests parsing cards that are not in the deck"

        cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.SPADES),
        )

        missing_card = structures.Card(constants.ACES, constants.SPADES)
        self.table.remove_card_from_deck(missing_card)

        generator = engines.deal_common_cards(self.table, 3)

        with self.subTest('generator await'):
            await_state = next(generator)
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card != missing_card),
            )

        await_state.deal_cards(cards)

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_card_not_in_deck)
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card != missing_card),
            )


    def test_common_cards_parse_valid_cards(self):

        "Tests parsing a repeated cards"

        common_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.TENS, constants.SPADES),
        )

        generator = engines.deal_common_cards(self.table, 3)

        with self.subTest('generator await'):
            await_state = next(generator)
            self.assertTupleEqual(self.table.common_cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(common_cards)

        with self.subTest('generator end'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertTupleEqual(self.table.common_cards, common_cards)
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in common_cards),
            )


class TestHandCycleDealCardsToPlayersFunction(BaseTestCase):


    "Runs unit tests on deal_cards_to_players function."


    def test_player_cards_skip_dealing(self):

        "Tests skipping dealing."

        generator = engines.deal_cards_to_players(self.table, 2)

        Andy_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        with self.subTest('first generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertTupleEqual(self.Andy.cards, ())
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(Andy_cards)

        with self.subTest('second generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Boa)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_not_exact_amount_of_cards.format(2))
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )


    def test_player_cards_parse_invalid_cards_amount(self):

        "Tests parsing an invalid amount of cards"

        generator = engines.deal_cards_to_players(self.table, 2)

        Andy_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        Boa_cards = (
            structures.Card(constants.TENS, constants.CLUBS),
        )

        with self.subTest('first generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertTupleEqual(self.Andy.cards, ())
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(Andy_cards)

        with self.subTest('second generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Boa)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )

        await_state.deal_cards(Boa_cards)

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_not_exact_amount_of_cards.format(2))
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )


    def test_player_cards_parse_repeated_cards(self):

        "Tests parsing a repeated cards"

        generator = engines.deal_cards_to_players(self.table, 2)

        Andy_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        Boa_cards = (
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.TENS, constants.CLUBS),
        )

        with self.subTest('first generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertTupleEqual(self.Andy.cards, ())
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(Andy_cards)

        with self.subTest('second generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Boa)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )

        await_state.deal_cards(Boa_cards)

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_repeated_cards)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )


    def test_player_cards_parse_missing_cards(self):

        "Tests parsing cards that are not in the deck"

        generator = engines.deal_cards_to_players(self.table, 2)

        Andy_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        Boa_cards = (
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.ACES, constants.SPADES),
        )

        with self.subTest('first generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertTupleEqual(self.Andy.cards, ())
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(Andy_cards)

        with self.subTest('second generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Boa)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )

        await_state.deal_cards(Boa_cards)

        with self.subTest('generator end'):
            with self.assertRaises(ValueError) as context:
                next(generator)
            self.assertEqual(context.exception.args[0], messages.msg_card_not_in_deck)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )


    def test_player_cards_parse_valid_cards(self):

        "Tests parsing a repeated cards"

        generator = engines.deal_cards_to_players(self.table, 2)

        Andy_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        Boa_cards = (
            structures.Card(constants.TENS, constants.CLUBS),
            structures.Card(constants.TENS, constants.HEARTS),
        )

        Coral_cards = (
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.CLUBS),
        )

        with self.subTest('first generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Andy)
            self.assertTupleEqual(self.Andy.cards, ())
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(self.table.deck, self.full_deck)

        await_state.deal_cards(Andy_cards)

        with self.subTest('second generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Boa)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, ())
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in Andy_cards),
            )

        await_state.deal_cards(Boa_cards)

        with self.subTest('third generator await'):
            await_state = next(generator)
            self.assertEqual(await_state.player, self.Coral)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, Boa_cards)
            self.assertTupleEqual(self.Coral.cards, ())
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in (*Andy_cards, *Boa_cards)),
            )

        await_state.deal_cards(Coral_cards)

        with self.subTest('generator end'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)
            self.assertTupleEqual(self.Andy.cards, Andy_cards)
            self.assertTupleEqual(self.Boa.cards, Boa_cards)
            self.assertTupleEqual(self.Coral.cards, Coral_cards)
            self.assertTupleEqual(
                self.table.deck,
                tuple(card for card in self.full_deck if card not in (*Andy_cards, *Boa_cards, *Coral_cards)),
            )


if __name__ == '__main__':
    main()