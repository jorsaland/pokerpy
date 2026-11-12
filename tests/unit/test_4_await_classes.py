"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, states, structures


class BaseTestCase(TestCase):


    "Base class for test cases that require a shared setup."


    def setUp(self):

        self.player = structures.Player('Andy', 1000)

        self.common_dealing_await = states.CommonDealingAwait(
            count = 2,
            deck = tuple(
                structures.Card(constants.ACES, suit) for suit in constants.sorted_card_suits
            ),
        )

        self.player_action_await = states.PlayerActionAwait(
            player = self.player,
            ranges = {
                constants.ACTION_CHECK: range(0, 1),
                constants.ACTION_FOLD: range(0, 1),
                constants.ACTION_BET: range(10, 1001),
            },
        )

        self.player_blind_await = states.PlayerBlindAwait(player=self.player, amount=10)

        self.player_dealing_await = states.PlayerDealingAwait(
            player = self.player,
            count = 2,
            deck = tuple(
                structures.Card(constants.ACES, suit) for suit in constants.sorted_card_suits
            ),
        )


class TestAwaitStatesParseMethods(BaseTestCase):


    "Runs unit tests on await states methods to parse values."


    def test_input_in_common_dealing_await_parse_method(self):

        "Tests valid and invalid input in the parse method of CommonDealingAwait."

        non_iterables = (1, structures.Card(constants.ACES, constants.SPADES), None)
        not_all_cards = ('As', structures.Card(constants.ACES, constants.SPADES), None)
        all_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
        )

        await_state = self.common_dealing_await

        for value in non_iterables:
            with self.subTest('invalid iterable', value=value):
                with self.assertRaises(TypeError) as context:
                    await_state.deal_cards(value)
                self.assertEqual(context.exception.args[0], messages.msg_not_iterable_object.format(type(value).__name__))

        with self.subTest('invalid cards', value=not_all_cards):
            with self.assertRaises(TypeError) as context:
                await_state.deal_cards(not_all_cards)
            self.assertEqual(context.exception.args[0], messages.msg_not_all_card_instances)

        with self.subTest('valid input', value=all_cards):
            self.assertTupleEqual(await_state.dealt_cards, ())
            await_state.deal_cards(all_cards)
            self.assertTupleEqual(await_state.dealt_cards, all_cards)


    def test_input_in_player_blind_await_parse_method(self):

        "Tests valid and invalid input in the parse method of PlayerBlindAwait."

        await_state = self.player_blind_await

        with self.subTest('state change'):
            self.assertFalse(await_state.placed_blind)
            await_state.place_blind()
            self.assertTrue(await_state.placed_blind)


    def test_input_in_player_action_await_parse_method(self):

        "Tests valid and invalid input in the parse method of PlayerActionAwait."

        non_actions = (1, 'jump', None)
        valid_action = structures.Action(constants.ACTION_CHECK)

        await_state = self.player_action_await

        for value in non_actions:
            with self.subTest('invalid action', value=value):
                with self.assertRaises(TypeError) as context:
                    await_state.request_action(value)
                self.assertEqual(context.exception.args[0], messages.msg_not_action_instance.format(type(value).__name__))

        with self.subTest('valid input', value=valid_action):
            self.assertIsNone(await_state.requested_action)
            await_state.request_action(valid_action)
            self.assertEqual(await_state.requested_action, valid_action)


    def test_input_in_player_dealing_await_parse_method(self):

        "Tests valid and invalid input in the parse method of PlayerDealingAwait."

        non_iterables = (1, structures.Card(constants.ACES, constants.SPADES), None)
        not_all_cards = ('As', structures.Card(constants.ACES, constants.SPADES), None)
        all_cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.HEARTS),
        )

        await_state = self.player_dealing_await

        for value in non_iterables:
            with self.subTest('invalid iterable', value=value):
                with self.assertRaises(TypeError) as context:
                    await_state.deal_cards(value)
                self.assertEqual(context.exception.args[0], messages.msg_not_iterable_object.format(type(value).__name__))

        with self.subTest('invalid cards', value=not_all_cards):
            with self.assertRaises(TypeError) as context:
                await_state.deal_cards(not_all_cards)
            self.assertEqual(context.exception.args[0], messages.msg_not_all_card_instances)

        with self.subTest('valid input', value=all_cards):
            self.assertTupleEqual(await_state.dealt_cards, ())
            await_state.deal_cards(all_cards)
            self.assertTupleEqual(await_state.dealt_cards, all_cards)


class TestAwaitStatesSerializationMethods(BaseTestCase):


    "Runs unit tests on await states methods to serialize attributes."


    def test_input_in_common_dealing_await_serialization_method(self):

        "Tests valid and invalid input in the serialization method of CommonDealingAwait."

        self.assertDictEqual(
            self.common_dealing_await.to_dict(),
            {
                "count": 2,
                "deck": [
                    {"value": constants.ACES, "suit": constants.CLUBS},
                    {"value": constants.ACES, "suit": constants.DIAMONDS},
                    {"value": constants.ACES, "suit": constants.HEARTS},
                    {"value": constants.ACES, "suit": constants.SPADES},
                ]
            },
        )


    def test_input_in_player_action_await_serialization_method(self):

        "Tests valid and invalid input in the serialization method of PlayerActionAwait."

        self.assertDictEqual(
            self.player_action_await.to_dict(),
            {
                "player": {
                    "name": "Andy",
                    "stack": 1000,
                },
                "ranges": {
                    constants.ACTION_CHECK: {
                        "min": 0,
                        "max": 0,
                    },
                    constants.ACTION_FOLD: {
                        "min": 0,
                        "max": 0,
                    },
                    constants.ACTION_BET: {
                        "min": 10,
                        "max": 1000,
                    },
                },
            },
        )


    def test_input_in_player_blind_await_serialization_method(self):

        "Tests valid and invalid input in the serialization method of PlayerBlindAwait."

        self.assertDictEqual(
            self.player_blind_await.to_dict(),
            {
                "player": {
                    "name": "Andy",
                    "stack": 1000,
                },
                "amount": 10,
            },
        )


    def test_input_in_player_dealing_await_serialization_method(self):

        "Tests valid and invalid input in the serialization method of PlayerDealingAwait."

        self.assertDictEqual(
            self.player_dealing_await.to_dict(),
            {
                "player": {
                    "name": "Andy",
                    "stack": 1000,
                },
                "count": 2,
                "deck": [
                    {"value": constants.ACES, "suit": constants.CLUBS},
                    {"value": constants.ACES, "suit": constants.DIAMONDS},
                    {"value": constants.ACES, "suit": constants.HEARTS},
                    {"value": constants.ACES, "suit": constants.SPADES},
                ]
            },
        )


if __name__ == '__main__':
    main()