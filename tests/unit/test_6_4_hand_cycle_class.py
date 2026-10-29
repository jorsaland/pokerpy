"""
Defines unit tests on BettingRound class.
"""


import sys
sys.path.insert(0, '.')


from decimal import Decimal
from unittest import main, TestCase


from pokerpy import constants, engines, messages, structures


class BaseTestCase(TestCase):


    "Base class for test cases that require a shared setup."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi = self.setup_players

        self.table = structures.Table(self.setup_players)


class TestHandCycleInstantiation(BaseTestCase):


    "Runs unit tests on hand cycle instantiation."


    def test_name_type_error(self):

        "Tests type error detection on the field name."

        bad_names = (1, None)

        for bad_name in bad_names:

            with self.subTest(name=bad_name):
                with self.assertRaises(TypeError) as context:
                    engines.HandCycle(name=bad_name, table=self.table)
                self.assertEqual(context.exception.args[0], messages.msg_not_str.format(type(bad_name).__name__))


    def test_table_type_error(self):

        "Tests type error detection on the field name."

        bad_tables = (1, 'pivot_table', None)

        for bad_table in bad_tables:

            with self.subTest(table=bad_table):
                with self.assertRaises(TypeError) as context:
                    engines.HandCycle(name='test', table=bad_table)
                self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(type(bad_table).__name__))


    def test_valid_input(self):

        "Tests valid input."

        hand_cycle = engines.HandCycle('test', self.table)
        with self.subTest('simple instantiation'):
            self.assertEqual(hand_cycle.name, 'test')
            self.assertEqual(hand_cycle.table, self.table)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.open_fold_allowed)
            self.assertFalse(hand_cycle.raise_invalid_actions)

        hand_cycle = engines.HandCycle(
            'test',
            self.table,
            open_fold_allowed = True,
            raise_invalid_actions = True,
        )
        with self.subTest('complex instantiation'):
            self.assertEqual(hand_cycle.name, 'test')
            self.assertEqual(hand_cycle.table, self.table)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.open_fold_allowed)
            self.assertTrue(hand_cycle.raise_invalid_actions)


class TestHandCycleMethods(BaseTestCase):


    "Runs unit tests on hand cycle methods."


    def test_type_errors_in_dealing_related_methods(self):

        "Tests type error detection in methods related to dealing."

        hand_cycle = engines.HandCycle('test', self.table)

        methods = (
            hand_cycle.deal_cards_to_players,
            hand_cycle.deal_common_cards,
        )

        bad_amounts = ('300', 300.0, Decimal('300'))

        for method in methods:

            for bad_amount in bad_amounts:

                with self.subTest(method=method.__name__, amount=bad_amount):
                    with self.assertRaises(TypeError) as context:
                        method(bad_amount)
                    self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))


    def test_type_errors_in_reset_method(self):

        "Tests type error detection in the reset method."

        bad_tables = (1, 'pivot_table', None)

        for bad_table in bad_tables:

            with self.subTest(table=bad_table):
                with self.assertRaises(TypeError) as context:
                    engines.HandCycle.reset_hand_cycle_states(bad_table)
                self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(type(bad_table).__name__))


    def test_value_errors_in_dealing_related_methods(self):

        "Tests type error detection in methods related to dealing."

        hand_cycle = engines.HandCycle('test', self.table)

        methods = (
            hand_cycle.deal_cards_to_players,
            hand_cycle.deal_common_cards,
        )

        for method in methods:

            bad_min_bet = 0
            with self.subTest('zero minimum bet', method=method.__name__):
                with self.assertRaises(ValueError) as context:
                    method(bad_min_bet)
                self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_min_bet))

            bad_min_bet = -10
            with self.subTest('negative minimum bet', method=method.__name__):
                with self.assertRaises(ValueError) as context:
                    method(bad_min_bet)
                self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_min_bet))


    def test_valid_input_in_dealing_methods(self):

        "Tests valid input in methods related to dealing."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before card deal'):
            self.assertEqual(len(self.table.deck), 52)
            self.assertEqual(len(self.table.common_cards), 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        hand_cycle.deal_cards_to_players(2)

        with self.subTest('after card deal to players'):
            self.assertEqual(len(self.table.deck), 40)
            self.assertEqual(len(self.table.common_cards), 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        hand_cycle.deal_common_cards(5)

        with self.subTest('after card deal to table'):
            self.assertEqual(len(self.table.deck), 35)
            self.assertEqual(len(self.table.common_cards), 5)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)


    def test_valid_input_in_reset_method(self):

        "Tests valid input detection in the reset method."

        player_cards = [
            structures.Card(constants.DEUCES, constants.SPADES),
            structures.Card(constants.THREES, constants.SPADES),
            structures.Card(constants.FOURS, constants.SPADES),
            structures.Card(constants.FIVES, constants.SPADES),
            structures.Card(constants.SIXES, constants.SPADES),
            structures.Card(constants.SEVENS, constants.SPADES),
        ]

        common_cards = [
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
        ]

        hand = structures.Hand((
            structures.Card(constants.ACES, constants.HEARTS),
            structures.Card(constants.ACES, constants.DIAMONDS),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
        ))

        folded_players = (
            self.Andy,
            self.Boa,
            self.Coral
        )

        with self.subTest('initial states'):
            self.assertEqual(self.table.min_raise_increase, 1)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            for player in self.table.players:
                self.assertFalse(player.has_played)
                self.assertIsNone(player.requested_action)
                self.assertEqual(len(player.cards), 0)
                self.assertIsNone(player.hand)
                self.assertFalse(player.is_folded)
                self.assertFalse(player.is_extra_blind)
                self.assertEqual(player.pot_index, 0)
            self.assertEqual(len(self.table.deck), 52)
            self.assertTupleEqual(self.table.split_central_pot, (0,))

        self.table.set_min_raise_increase(100)
        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_stopping_player(self.Coral)
        self.table.increase_central_pot(10)
        self.table.add_side_pot()
        self.table.increase_central_pot(5)
        for card in common_cards:
            self.table.remove_card_from_deck(card)
            self.table.assign_common_card(card)
        for player, card in zip(self.table.players, player_cards):
            player.mark_has_played()
            player.request_action(structures.Action(constants.ACTION_CHECK))
            self.table.remove_card_from_deck(card)
            player.assign_card(card)
            player.assign_hand(hand)
            if player in folded_players:
                player.mark_is_folded()
            else:
                player.increase_pot_index()
            player.mark_is_extra_blind()

        with self.subTest('updated states'):
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.stopping_player, self.Coral)
            for player in self.table.players:
                self.assertTrue(player.has_played)
                self.assertEqual(player.requested_action, structures.Action(constants.ACTION_CHECK))
                self.assertEqual(len(player.cards), 1)
                self.assertEqual(player.hand, hand)
                self.assertTrue(player.is_extra_blind)
                if player in folded_players:
                    self.assertTrue(player.is_folded)
                    self.assertIsNone(player.pot_index)
                else:
                    self.assertFalse(player.is_folded)
                    self.assertEqual(player.pot_index, 1)
            self.assertEqual(len(self.table.deck), 43)
            self.assertTupleEqual(self.table.split_central_pot, (10, 5))

        engines.HandCycle.reset_hand_cycle_states(self.table)

        with self.subTest('final states'):
            self.assertEqual(self.table.min_raise_increase, 1)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            for player in self.table.players:
                self.assertFalse(player.has_played)
                self.assertIsNone(player.requested_action)
                self.assertEqual(len(player.cards), 0)
                self.assertIsNone(player.hand)
                self.assertFalse(player.is_folded)
                self.assertEqual(player.pot_index, 0)
                self.assertFalse(player.is_extra_blind)
            self.assertEqual(len(self.table.deck), 52)
            self.assertTupleEqual(self.table.split_central_pot, (0,))


    def test_betting_round_setup_methods(self):

        "Tests valid input in the methods that set the current betting round."

        hand_cycle = engines.HandCycle('test', self.table)
        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before betting round setup'):
            self.assertIsNone(hand_cycle.betting_round)

        with self.subTest('after betting round setup'):
            hand_cycle.set_betting_round(betting_round)
            self.assertEqual(hand_cycle.betting_round, betting_round)

        with self.subTest('after betting round reset'):
            hand_cycle.reset_betting_round()
            self.assertIsNone(hand_cycle.betting_round)


    def test_extra_blind_setup_methods(self):

        "Tests valid input in the methods that set the extra blind phase indicator."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before indicator setup'):
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)

        with self.subTest('after indicator setup'):
            hand_cycle.mark_in_extra_big_blinds_phase()
            self.assertTrue(hand_cycle.in_extra_big_blinds_phase)

        with self.subTest('after indicator reset'):
            hand_cycle.unmark_in_extra_big_blinds_phase()
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)


class TestHandCycleFlow(BaseTestCase):


    "Runs unit tests on hand cycle flow."


    def setUp(self):

        super().setUp()
        self.table.set_button_player(self.setup_players[-1])
        self.round_names = (constants.PREFLOP, *constants.after_preflop_round_names)


    def test_flow_behaviour_from_boolean_setup(self):

        "Tests flow behaviour depending on boolean parameters."

        open_fold_allowed = True
        raise_invalid_actions = True
        hand_cycle = engines.HandCycle(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_CALL, 100))
            with self.assertRaises(RuntimeError) as context:
                self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            with self.assertRaises(StopIteration) as context:
                next(hand_cycle.listen())
            self.assertIsNone(context.exception.value)

        self.setUp()
        open_fold_allowed = True
        raise_invalid_actions = False
        hand_cycle = engines.HandCycle(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_CALL, 100))
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_FOLD))
            self.assertEqual(next(hand_cycle.listen()), self.Boa)

        self.setUp()
        open_fold_allowed = False
        raise_invalid_actions = True
        hand_cycle = engines.HandCycle(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_FOLD))
            with self.assertRaises(RuntimeError) as context:
                self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            with self.assertRaises(StopIteration) as context:
                next(hand_cycle.listen())
            self.assertIsNone(context.exception.value)


        self.setUp()
        open_fold_allowed = False
        raise_invalid_actions = False
        hand_cycle = engines.HandCycle(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_FOLD))
            self.assertEqual(next(hand_cycle.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_CHECK))
            self.assertEqual(next(hand_cycle.listen()), self.Boa)


    def test_flow_with_function_next_missing_close(self):

        "Tests flow with function next, missing close method."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)

        for round_name in self.round_names:
            for player in self.setup_players:
                with self.subTest(round=round_name, player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                    self.assertEqual(hand_cycle.betting_round.name, round_name)
                    self.assertFalse(hand_cycle.is_completed)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(hand_cycle.listen())
            self.assertIsNone(context.exception.value)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)


    def test_flow_with_function_next_calling_close_at_end(self):

        "Tests flow with function next, using close method at the end."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)

        for round_name in self.round_names:
            for player in self.setup_players:
                with self.subTest(round=round_name, player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                    self.assertEqual(hand_cycle.betting_round.name, round_name)
                    self.assertFalse(hand_cycle.is_completed)

        hand_cycle.close()
        with self.subTest('after actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertTrue(hand_cycle.is_completed)


    def test_flow_with_function_next_calling_close_before_end(self):

        "Tests flow with function next, using close method before the end."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)

        with self.subTest('close before time'):
            with self.assertRaises(RuntimeError) as context:
                hand_cycle.close()
            self.assertEqual(context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)


    def test_flow_with_loop_missing_close(self):

        "Tests flow with for loop, missing close method."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)

        for i, player in enumerate(hand_cycle.listen()):
            round_name = self.round_names[i // len(self.setup_players)]
            with self.subTest(round=round_name, player=player.name):
                self.assertEqual(player, self.setup_players[i % len(self.setup_players)])
                player.request_action(structures.Action(constants.ACTION_CHECK))
                self.assertEqual(hand_cycle.betting_round.name, round_name)
                self.assertFalse(hand_cycle.is_completed)

        with self.subTest('after actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)


    def test_flow_with_loop_calling_close_at_end(self):

        "Tests flow with for loop, calling close method at the end."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)

        for i, player in enumerate(hand_cycle.listen()):
            round_name = self.round_names[i // len(self.setup_players)]
            with self.subTest(round=round_name, player=player.name):
                self.assertEqual(player, self.setup_players[i % len(self.setup_players)])
                player.request_action(structures.Action(constants.ACTION_CHECK))
                self.assertEqual(hand_cycle.betting_round.name, round_name)
                self.assertFalse(hand_cycle.is_completed)

        hand_cycle.close()
        with self.subTest('after actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertTrue(hand_cycle.is_completed)


    def test_flow_with_loop_calling_close_before_end(self):

        "Tests flow with for loop, calling close method at the end."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)

        with self.subTest('close before time'):
            with self.assertRaises(RuntimeError) as context:
                for _ in hand_cycle.listen():
                    hand_cycle.close()
                    break
            self.assertEqual(context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.is_completed)


    def test_flow_with_context_manager_missing_close(self):

        "Tests flow with context manager, missing close method."

        with engines.HandCycle('test', self.table) as hand_cycle:

            for player in hand_cycle.listen():
                player.request_action(structures.Action(constants.ACTION_CHECK))

            with self.subTest('after actions inside manager'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.is_completed)

        with self.subTest('after actions outside manager'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertTrue(hand_cycle.is_completed)


    def test_flow_with_context_manager_calling_close_at_end(self):

        "Tests flow with context manager, using close method at the end."

        with engines.HandCycle('test', self.table) as hand_cycle:

            for player in hand_cycle.listen():
                player.request_action(structures.Action(constants.ACTION_CHECK))
            hand_cycle.close() ## redundant, the context manager closes the round

            with self.subTest('after actions inside manager'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertTrue(hand_cycle.is_completed)

        with self.subTest('after actions outside manager'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertTrue(hand_cycle.is_completed)


    def test_flow_with_context_manager_calling_close_before_end(self):

        "Tests flow with context manager, using close method before the end."

        with self.assertRaises(RuntimeError) as context:
            with engines.HandCycle('test', self.table) as hand_cycle:
                hand_cycle.close()

        self.assertEqual(context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
        self.assertIsNone(hand_cycle.betting_round)
        self.assertFalse(hand_cycle.is_completed)


    def test_flow_with_context_manager_overloading_the_listener(self):

        "Tests flow with context manager, using close method at the end."

        with self.assertRaises(RuntimeError) as context:
            with engines.HandCycle('test', self.table) as hand_cycle:
                for player in hand_cycle.listen():
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                next(hand_cycle.listen()) ## overloaded listener

        self.assertEqual(context.exception.args[0], messages.msg_overloaded_hand_cycle)
        self.assertIsNone(hand_cycle.betting_round)
        self.assertTrue(hand_cycle.is_completed)


if __name__ == '__main__':
    main()