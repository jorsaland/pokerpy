"""
Defines unit tests on BettingRound class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import engines, structures


class TestBettingRoundAssignHandFunction(TestCase):


    "Runs unit tests on assign_hand function."


    def test_best_hand_in_preflop(self):

        """
        Tests when a hand cannot be assigned, in the pre-flop.
        """

        player = structures.Player('Andy', 1000)

        player_cards = (
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
        )

        common_cards = ()

        for card in player_cards:
            player.assign_card(card)

        with self.subTest('before assignment'):
            self.assertIsNone(player.hand)

        engines.assign_hand(player, common_cards)

        with self.subTest('after assignment'):
            self.assertIsNone(player.hand)


    def test_best_hand_in_flop(self):

        """
        Tests when the best hand is conformed by all of the private cards and all of the common
        cards, in the flop.
        """

        player = structures.Player('Andy', 1000)

        player_cards = (
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
        )

        common_cards = (
            structures.Card('J', 's'),
            structures.Card('J', 'd'),
            structures.Card('9', 'd'),
        )

        for card in player_cards:
            player.assign_card(card)

        with self.subTest('before assignment'):
            self.assertIsNone(player.hand)

        engines.assign_hand(player, common_cards)

        with self.subTest('after assignment'):
            self.assertEqual(player.hand, structures.Hand((*player_cards, *common_cards)))


    def test_best_hand_two_private_three_common_in_turn(self):

        """
        Tests when the best hand is conformed by 2 of the private cards and 3 of the common cards,
        in the turn.
        """

        player = structures.Player('Andy', 1000)

        player_cards = (
            structures.Card('7', 's'),
            structures.Card('9', 'c'),
        )

        common_cards = (
            structures.Card('J', 's'),
            structures.Card('J', 'd'),
            structures.Card('9', 'd'),
            structures.Card('7', 'd'),
        )

        for card in player_cards:
            player.assign_card(card)

        with self.subTest('before assignment'):
            self.assertIsNone(player.hand)

        engines.assign_hand(player, common_cards)

        with self.subTest('after assignment'):
            self.assertEqual(player.hand, structures.Hand((*player_cards[:2], *common_cards[:3])))


    def test_best_hand_one_private_four_common_in_turn(self):

        """
        Tests when the best hand is conformed by 1 of the private cards and 4 of the common cards,
        in the turn.
        """

        player = structures.Player('Andy', 1000)

        player_cards = (
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
        )

        common_cards = (
            structures.Card('J', 's'),
            structures.Card('J', 'd'),
            structures.Card('9', 'd'),
            structures.Card('9', 'c'),
        )

        for card in player_cards:
            player.assign_card(card)

        with self.subTest('before assignment'):
            self.assertIsNone(player.hand)

        engines.assign_hand(player, common_cards)

        with self.subTest('after assignment'):
            self.assertEqual(player.hand, structures.Hand((player_cards[0], *common_cards)))


    def test_best_hand_common_cards_in_river(self):

        "Tests when the best hand is conformed by the common cards in the river."

        player = structures.Player('Andy', 1000)

        player_cards = (
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
        )

        common_cards = (
            structures.Card('J', 's'),
            structures.Card('J', 'd'),
            structures.Card('9', 'd'),
            structures.Card('9', 'c'),
            structures.Card('A', 'd'),
        )

        for card in player_cards:
            player.assign_card(card)

        with self.subTest('before assignment'):
            self.assertIsNone(player.hand)

        engines.assign_hand(player, common_cards)

        with self.subTest('after assignment'):
            self.assertEqual(player.hand, structures.Hand(common_cards))


    def test_best_hand_one_private_four_common_in_river(self):

        """
        Tests when the best hand is conformed by 1 of the private cards and 4 of the common cards,
        in the river.
        """

        player = structures.Player('Andy', 1000)

        player_cards = (
            structures.Card('J', 's'),
            structures.Card('7', 'd'),
        )

        common_cards = (
            structures.Card('9', 'd'),
            structures.Card('9', 'c'),
            structures.Card('A', 'd'),
            structures.Card('J', 'd'),
            structures.Card('7', 's'),
        )

        for card in player_cards:
            player.assign_card(card)

        with self.subTest('before assignment'):
            self.assertIsNone(player.hand)

        engines.assign_hand(player, common_cards)

        with self.subTest('after assignment'):
            self.assertEqual(player.hand, structures.Hand((player_cards[0], *common_cards[:4])))


    def test_best_hand_two_private_three_common_in_river(self):

        """
        Tests when the best hand is conformed by 2 of the private cards and 3 of the common cards,
        in the river.
        """

        player = structures.Player('Andy', 1000)

        player_cards = (
            structures.Card('J', 's'),
            structures.Card('J', 'd'),
        )

        common_cards = (
            structures.Card('9', 'd'),
            structures.Card('9', 'c'),
            structures.Card('A', 'd'),
            structures.Card('7', 'd'),
            structures.Card('7', 's'),
        )

        for card in player_cards:
            player.assign_card(card)

        with self.subTest('before assignment'):
            self.assertIsNone(player.hand)

        engines.assign_hand(player, common_cards)

        with self.subTest('after assignment'):
            self.assertEqual(player.hand, structures.Hand((*player_cards[:2], *common_cards[:3])))


if __name__ == '__main__':
    main()