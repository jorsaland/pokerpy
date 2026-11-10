"""
Defines unit tests on HandCycle class.
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


class BaseFlowTestCase(BaseTestCase):


    "Base class for test cases that require a shared setup for flow unit tests."


    def setUp(self):

        super().setUp()

        self.table.set_small_blind(50)
        self.table.set_big_blind(100)

        self.table.set_button_player(self.Andy)
        self.table.set_small_blind_player(self.Boa)
        self.table.set_big_blind_player(self.Coral)

        self.extra_blind_players = (self.Dino, self.Epa, self.Fomi, self.Andy)
        self.round_names = (constants.PREFLOP, *constants.after_preflop_round_names)


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


class TestHandCycleFlowWithoutContextManager(BaseFlowTestCase):


    "Runs unit tests on hand cycle flow without context manager."


    def test_no_context_manager_flow_with_function_next_missing_close(self):

        "Tests flow with function next, missing close method."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        for player in self.extra_blind_players:
            with self.subTest('extra blind phase (preflop)', player=player.name):
                self.assertEqual(next(hand_cycle.listen()), player)
                self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        for player in [*self.setup_players[3:], *self.setup_players[:3]]:
            if player == self.Boa:
                action = structures.Action(constants.ACTION_CALL, 50)
            elif player == self.Coral:
                action = structures.Action(constants.ACTION_CHECK)
            else:
                action = structures.Action(constants.ACTION_CALL, 100)
            with self.subTest(round=constants.PREFLOP, player=player.name):
                self.assertEqual(next(hand_cycle.listen()), player)
                player.request_action(action)
                self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        for round_name in constants.after_preflop_round_names:
            for player in [*self.setup_players[1:], *self.setup_players[:1]]:
                with self.subTest(round=round_name, player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                    self.assertEqual(hand_cycle.betting_round.name, round_name)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('after actions'):
            self.assertEqual(hand_cycle.betting_round.name, constants.RIVER)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)


    def test_no_context_manager_flow_with_function_next_calling_close_at_end(self):

        "Tests flow with function next, using close method at the end."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        for player in self.extra_blind_players:
            with self.subTest('extra blind phase (preflop)', player=player.name):
                self.assertEqual(next(hand_cycle.listen()), player)
                self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        for player in [*self.setup_players[3:], *self.setup_players[:3]]:
            if player == self.Boa:
                action = structures.Action(constants.ACTION_CALL, 50)
            elif player == self.Coral:
                action = structures.Action(constants.ACTION_CHECK)
            else:
                action = structures.Action(constants.ACTION_CALL, 100)
            with self.subTest(round=constants.PREFLOP, player=player.name):
                self.assertEqual(next(hand_cycle.listen()), player)
                player.request_action(action)
                self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        for round_name in constants.after_preflop_round_names:
            for player in [*self.setup_players[1:], *self.setup_players[:1]]:
                with self.subTest(round=round_name, player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                    self.assertEqual(hand_cycle.betting_round.name, round_name)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('after actions, before close'):
            self.assertEqual(hand_cycle.betting_round.name, constants.RIVER)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        hand_cycle.close() # needed in this case to finish the generator after the last action

        with self.subTest('after actions, after close'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_no_context_manager_flow_with_function_next_calling_close_at_extra_blind_phase(self):

        "Tests flow with function next, using close method at extra blind phase."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('close before time'):
            next(hand_cycle.listen())
            with self.assertRaises(RuntimeError) as context:
                hand_cycle.close()

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_no_context_manager_flow_with_function_next_calling_close_before_end(self):

        "Tests flow with function next, using close method before the end."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        for player in self.extra_blind_players:
            with self.subTest('extra blind phase (preflop)', player=player.name):
                self.assertEqual(next(hand_cycle.listen()), player)
                self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        for player in [*self.setup_players[3:], *self.setup_players[:3]]:
            if player == self.Boa:
                action = structures.Action(constants.ACTION_CALL, 50)
            elif player == self.Coral:
                action = structures.Action(constants.ACTION_CHECK)
            else:
                action = structures.Action(constants.ACTION_CALL, 100)
            with self.subTest(round=constants.PREFLOP, player=player.name):
                self.assertEqual(next(hand_cycle.listen()), player)
                player.request_action(action)
                self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('close before time'):
            with self.assertRaises(RuntimeError) as inner_context:
                hand_cycle.close()

        with self.subTest('after close'):
            self.assertEqual(inner_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_no_context_manager_flow_with_loop_missing_close(self):

        "Tests flow with for loop, missing close method."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        for i, player in enumerate(hand_cycle.listen()):

            if i <= 3:
                with self.subTest('extra blind phase (preflop)', player=player.name):
                    self.assertEqual(player, self.extra_blind_players[i])
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            elif i <= 9:
                if player == self.Boa:
                    action = structures.Action(constants.ACTION_CALL, 50)
                elif player == self.Coral:
                    action = structures.Action(constants.ACTION_CHECK)
                else:
                    action = structures.Action(constants.ACTION_CALL, 100)
                with self.subTest(round=constants.PREFLOP, player=player.name):
                    self.assertEqual(player, [*self.setup_players[3:], *self.setup_players[:3]][i-4])
                    player.request_action(action)
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            elif i <= 27:
                if i <= 15:
                    round_name = constants.FLOP
                elif i <= 21:
                    round_name = constants.TURN
                else:
                    round_name = constants.RIVER
                with self.subTest(round=round_name, player=player.name):
                    self.assertEqual(player, [*self.setup_players[1:], *self.setup_players[:1]][(i-10) % 6])
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                    self.assertEqual(hand_cycle.betting_round.name, round_name)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('after actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)


    def test_no_context_manager_flow_with_loop_calling_close_at_end(self):

        "Tests flow with for loop, calling close method at the end."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        for i, player in enumerate(hand_cycle.listen()):

            if i <= 3:
                with self.subTest('extra blind phase (preflop)', player=player.name):
                    self.assertEqual(player, self.extra_blind_players[i])
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            elif i <= 9:
                if player == self.Boa:
                    action = structures.Action(constants.ACTION_CALL, 50)
                elif player == self.Coral:
                    action = structures.Action(constants.ACTION_CHECK)
                else:
                    action = structures.Action(constants.ACTION_CALL, 100)
                with self.subTest(round=constants.PREFLOP, player=player.name):
                    self.assertEqual(player, [*self.setup_players[3:], *self.setup_players[:3]][i-4])
                    player.request_action(action)
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            elif i <= 27:
                if i <= 15:
                    round_name = constants.FLOP
                elif i <= 21:
                    round_name = constants.TURN
                else:
                    round_name = constants.RIVER
                with self.subTest(round=round_name, player=player.name):
                    self.assertEqual(player, [*self.setup_players[1:], *self.setup_players[:1]][(i-10) % 6])
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                    self.assertEqual(hand_cycle.betting_round.name, round_name)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('after actions, before close'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        hand_cycle.close() # redundant, the loop already closed the generator

        with self.subTest('after actions, after close'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_no_context_manager_flow_with_loop_calling_close_at_extra_blind_phase(self):

        "Tests flow with for loop, using close method at extra blind phase."

        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('close before time'):
            context = None
            for _ in hand_cycle.listen():
                with self.assertRaises(RuntimeError) as context:
                    hand_cycle.close()
                break

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_no_context_manager_flow_with_loop_calling_close_before_end(self):

        "Tests flow with for loop, calling close method at the end."


        hand_cycle = engines.HandCycle('test', self.table)

        with self.subTest('before actions'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('close before time'):

            context = None

            for i, player in enumerate(hand_cycle.listen()):

                if i <= 3: # extra blind phase
                    self.assertEqual(player, self.extra_blind_players[i])
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                elif i <= 9: # preflop
                    if player == self.Boa:
                        action = structures.Action(constants.ACTION_CALL, 50)
                    elif player == self.Coral:
                        action = structures.Action(constants.ACTION_CHECK)
                    else:
                        action = structures.Action(constants.ACTION_CALL, 100)
                    player.request_action(action)
                    self.assertEqual(player, [*self.setup_players[3:], *self.setup_players[:3]][i-4])
                    player.request_action(action)
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                else:
                    with self.assertRaises(RuntimeError) as context:
                        hand_cycle.close()
                    break

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


class TestHandCycleFlowWithContextManager(BaseFlowTestCase):


    "Runs unit tests on hand cycle flow with context manager."


    def test_context_manager_flow_with_function_next_missing_close(self):

        "Tests flow with function next, missing close method."

        with engines.HandCycle('test', self.table) as hand_cycle:

            with self.subTest('before actions'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

            for player in self.extra_blind_players:
                with self.subTest('extra blind phase (preflop)', player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            for player in [*self.setup_players[3:], *self.setup_players[:3]]:
                if player == self.Boa:
                    action = structures.Action(constants.ACTION_CALL, 50)
                elif player == self.Coral:
                    action = structures.Action(constants.ACTION_CHECK)
                else:
                    action = structures.Action(constants.ACTION_CALL, 100)
                with self.subTest(round=constants.PREFLOP, player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    player.request_action(action)
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            for round_name in constants.after_preflop_round_names:
                for player in [*self.setup_players[1:], *self.setup_players[:1]]:
                    with self.subTest(round=round_name, player=player.name):
                        self.assertEqual(next(hand_cycle.listen()), player)
                        player.request_action(structures.Action(constants.ACTION_CHECK))
                        self.assertEqual(hand_cycle.betting_round.name, round_name)
                        self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

            with self.subTest('after actions'):
                self.assertEqual(hand_cycle.betting_round.name, constants.RIVER)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_with_function_next_calling_close_at_end(self):

        "Tests flow with function next, using close method at the end."

        with engines.HandCycle('test', self.table) as hand_cycle:

            with self.subTest('before actions'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

            for player in self.extra_blind_players:
                with self.subTest('extra blind phase (preflop)', player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            for player in [*self.setup_players[3:], *self.setup_players[:3]]:
                if player == self.Boa:
                    action = structures.Action(constants.ACTION_CALL, 50)
                elif player == self.Coral:
                    action = structures.Action(constants.ACTION_CHECK)
                else:
                    action = structures.Action(constants.ACTION_CALL, 100)
                with self.subTest(round=constants.PREFLOP, player=player.name):
                    self.assertEqual(next(hand_cycle.listen()), player)
                    player.request_action(action)
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

            for round_name in constants.after_preflop_round_names:
                for player in [*self.setup_players[1:], *self.setup_players[:1]]:
                    with self.subTest(round=round_name, player=player.name):
                        self.assertEqual(next(hand_cycle.listen()), player)
                        player.request_action(structures.Action(constants.ACTION_CHECK))
                        self.assertEqual(hand_cycle.betting_round.name, round_name)
                        self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

            with self.subTest('after actions, before close'):
                self.assertEqual(hand_cycle.betting_round.name, constants.RIVER)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

            hand_cycle.close() # redundant, the context manager will close the generator

            with self.subTest('after actions, after close'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertTrue(hand_cycle.is_completed)
                self.assertTrue(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_with_function_next_calling_close_at_extra_blind_phase(self):

        "Tests flow with function next, using close method at extra blind phase."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.HandCycle('test', self.table) as hand_cycle:

                with self.subTest('before actions'):
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                with self.subTest('close before time'):
                    next(hand_cycle.listen())
                    with self.assertRaises(RuntimeError) as inner_context:
                        hand_cycle.close()

                with self.subTest('after close'):
                    self.assertEqual(inner_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertTrue(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_with_function_next_calling_close_before_end(self):

        "Tests flow with function next, using close method before the end."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.HandCycle('test', self.table) as hand_cycle:

                with self.subTest('before actions'):
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                for player in self.extra_blind_players:
                    with self.subTest('extra blind phase (preflop)', player=player.name):
                        self.assertEqual(next(hand_cycle.listen()), player)
                        self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                        self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

                for player in [*self.setup_players[3:], *self.setup_players[:3]]:
                    if player == self.Boa:
                        action = structures.Action(constants.ACTION_CALL, 50)
                    elif player == self.Coral:
                        action = structures.Action(constants.ACTION_CHECK)
                    else:
                        action = structures.Action(constants.ACTION_CALL, 100)
                    with self.subTest(round=constants.PREFLOP, player=player.name):
                        self.assertEqual(next(hand_cycle.listen()), player)
                        player.request_action(action)
                        self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                        self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

                with self.subTest('close before time'):
                    with self.assertRaises(RuntimeError) as inner_context:
                        hand_cycle.close()

                with self.subTest('after close'):
                    self.assertEqual(inner_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertTrue(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_with_loop_missing_close(self):

        "Tests flow with for loop, missing close method."

        with engines.HandCycle('test', self.table) as hand_cycle:

            with self.subTest('before actions'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

            for i, player in enumerate(hand_cycle.listen()):

                if i <= 3:
                    with self.subTest('extra blind phase (preflop)', player=player.name):
                        self.assertEqual(player, self.extra_blind_players[i])
                        self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                        self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

                elif i <= 9:
                    if player == self.Boa:
                        action = structures.Action(constants.ACTION_CALL, 50)
                    elif player == self.Coral:
                        action = structures.Action(constants.ACTION_CHECK)
                    else:
                        action = structures.Action(constants.ACTION_CALL, 100)
                    with self.subTest(round=constants.PREFLOP, player=player.name):
                        self.assertEqual(player, [*self.setup_players[3:], *self.setup_players[:3]][i-4])
                        player.request_action(action)
                        self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                        self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

                elif i <= 27:
                    if i <= 15:
                        round_name = constants.FLOP
                    elif i <= 21:
                        round_name = constants.TURN
                    else:
                        round_name = constants.RIVER
                    with self.subTest(round=round_name, player=player.name):
                        self.assertEqual(player, [*self.setup_players[1:], *self.setup_players[:1]][(i-10) % 6])
                        player.request_action(structures.Action(constants.ACTION_CHECK))
                        self.assertEqual(hand_cycle.betting_round.name, round_name)
                        self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

            with self.subTest('after actions'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertTrue(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_with_loop_calling_close_at_end(self):

        "Tests flow with for loop, calling close method at the end."

        with engines.HandCycle('test', self.table) as hand_cycle:

            with self.subTest('before actions'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertFalse(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

            for i, player in enumerate(hand_cycle.listen()):

                if i <= 3:
                    with self.subTest('extra blind phase (preflop)', player=player.name):
                        self.assertEqual(player, self.extra_blind_players[i])
                        self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                        self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

                elif i <= 9:
                    if player == self.Boa:
                        action = structures.Action(constants.ACTION_CALL, 50)
                    elif player == self.Coral:
                        action = structures.Action(constants.ACTION_CHECK)
                    else:
                        action = structures.Action(constants.ACTION_CALL, 100)
                    with self.subTest(round=constants.PREFLOP, player=player.name):
                        self.assertEqual(player, [*self.setup_players[3:], *self.setup_players[:3]][i-4])
                        player.request_action(action)
                        self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                        self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

                elif i <= 27:
                    if i <= 15:
                        round_name = constants.FLOP
                    elif i <= 21:
                        round_name = constants.TURN
                    else:
                        round_name = constants.RIVER
                    with self.subTest(round=round_name, player=player.name):
                        self.assertEqual(player, [*self.setup_players[1:], *self.setup_players[:1]][(i-10) % 6])
                        player.request_action(structures.Action(constants.ACTION_CHECK))
                        self.assertEqual(hand_cycle.betting_round.name, round_name)
                        self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                        self.assertFalse(hand_cycle.is_completed)
                        self.assertFalse(hand_cycle.was_reseted_at_closure)

            with self.subTest('after actions, before close'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertTrue(hand_cycle.is_completed)
                self.assertFalse(hand_cycle.was_reseted_at_closure)

            hand_cycle.close() # redundant, the loop already closed the generator

            with self.subTest('after actions, after close'):
                self.assertIsNone(hand_cycle.betting_round)
                self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                self.assertTrue(hand_cycle.is_completed)
                self.assertTrue(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_with_loop_calling_close_at_extra_blind_phase(self):

        "Tests flow with for loop, using close method at extra blind phase."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.HandCycle('test', self.table) as hand_cycle:

                with self.subTest('before actions'):
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                with self.subTest('close before time'):
                    inner_context = None
                    for _ in hand_cycle.listen():
                        with self.assertRaises(RuntimeError) as inner_context:
                            hand_cycle.close()
                        break

                with self.subTest('after close'):
                    self.assertEqual(inner_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertTrue(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_with_loop_calling_close_before_end(self):

        "Tests flow with for loop, calling close method at the end."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.HandCycle('test', self.table) as hand_cycle:

                with self.subTest('before actions'):
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                with self.subTest('close before time'):

                    inner_context = None

                    for i, player in enumerate(hand_cycle.listen()):

                        if i <= 3: # extra blind phase
                            self.assertEqual(player, self.extra_blind_players[i])
                            self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                            self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                            self.assertFalse(hand_cycle.is_completed)
                            self.assertFalse(hand_cycle.was_reseted_at_closure)

                        elif i <= 9: # preflop
                            if player == self.Boa:
                                action = structures.Action(constants.ACTION_CALL, 50)
                            elif player == self.Coral:
                                action = structures.Action(constants.ACTION_CHECK)
                            else:
                                action = structures.Action(constants.ACTION_CALL, 100)
                            player.request_action(action)
                            self.assertEqual(player, [*self.setup_players[3:], *self.setup_players[:3]][i-4])
                            self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                            self.assertFalse(hand_cycle.is_completed)
                            self.assertFalse(hand_cycle.was_reseted_at_closure)

                        else:
                            with self.assertRaises(RuntimeError) as inner_context:
                                hand_cycle.close()
                            break

                with self.subTest('after close'):
                    self.assertEqual(inner_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertTrue(hand_cycle.was_reseted_at_closure)

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_hand_cycle_was_not_completed)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_overloading_the_listener(self):

        "Tests flow, overloading the listener."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.HandCycle('test', self.table) as hand_cycle:

                with self.subTest('before actions'):
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                for i, player in enumerate(hand_cycle.listen()):

                    if i <= 3:
                        with self.subTest('extra blind phase (preflop)', player=player.name):
                            self.assertEqual(player, self.extra_blind_players[i])
                            self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                            self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                            self.assertFalse(hand_cycle.is_completed)
                            self.assertFalse(hand_cycle.was_reseted_at_closure)

                    elif i <= 9:
                        if player == self.Boa:
                            action = structures.Action(constants.ACTION_CALL, 50)
                        elif player == self.Coral:
                            action = structures.Action(constants.ACTION_CHECK)
                        else:
                            action = structures.Action(constants.ACTION_CALL, 100)
                        with self.subTest(round=constants.PREFLOP, player=player.name):
                            self.assertEqual(player, [*self.setup_players[3:], *self.setup_players[:3]][i-4])
                            player.request_action(action)
                            self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                            self.assertFalse(hand_cycle.is_completed)
                            self.assertFalse(hand_cycle.was_reseted_at_closure)

                    elif i <= 27:
                        if i <= 15:
                            round_name = constants.FLOP
                        elif i <= 21:
                            round_name = constants.TURN
                        else:
                            round_name = constants.RIVER
                        with self.subTest(round=round_name, player=player.name):
                            self.assertEqual(player, [*self.setup_players[1:], *self.setup_players[:1]][(i-10) % 6])
                            player.request_action(structures.Action(constants.ACTION_CHECK))
                            self.assertEqual(hand_cycle.betting_round.name, round_name)
                            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                            self.assertFalse(hand_cycle.is_completed)
                            self.assertFalse(hand_cycle.was_reseted_at_closure)

                with self.subTest('after actions'):
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertTrue(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                with self.subTest('listener overload'):
                    with self.assertRaises(StopIteration) as inner_context:
                        next(hand_cycle.listen())
                    self.assertIsNone(inner_context.exception.value)
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertTrue(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_overloaded_hand_cycle)
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertTrue(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


    def test_context_manager_flow_raising_exception(self):

        "Tests flow, raising an exception inside the context manager."

        with self.assertRaises(ValueError) as outer_context:

            with engines.HandCycle('test', self.table) as hand_cycle:

                with self.subTest('before actions'):
                    self.assertIsNone(hand_cycle.betting_round)
                    self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)

                with self.subTest('raise exception'):
                    next(hand_cycle.listen())
                    with self.assertRaises(ValueError) as inner_context:
                        raise ValueError('inner error')
                    self.assertEqual(inner_context.exception.args[0], 'inner error')
                    self.assertEqual(hand_cycle.betting_round.name, constants.PREFLOP)
                    self.assertTrue(hand_cycle.in_extra_big_blinds_phase)
                    self.assertFalse(hand_cycle.is_completed)
                    self.assertFalse(hand_cycle.was_reseted_at_closure)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], 'inner error')
            self.assertIsNone(hand_cycle.betting_round)
            self.assertFalse(hand_cycle.in_extra_big_blinds_phase)
            self.assertFalse(hand_cycle.is_completed)
            self.assertTrue(hand_cycle.was_reseted_at_closure)


if __name__ == '__main__':
    main()