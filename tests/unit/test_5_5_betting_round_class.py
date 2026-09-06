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

        self.Andy = self.setup_players[0]
        self.Boa = self.setup_players[1]
        self.Coral = self.setup_players[2]
        self.Dino = self.setup_players[3]
        self.Epa = self.setup_players[4]
        self.Fomi = self.setup_players[5]

        self.table = structures.Table(self.setup_players)


class TestBettingRoundInstantiation(BaseTestCase):


    "Runs unit tests on betting round instantiation."


    def test_name_type_error(self):

        "Tests type error detection on the field name."

        bad_names = (1, None)

        for bad_name in bad_names:

            with self.subTest(name=bad_name):
                with self.assertRaises(TypeError) as context:
                    engines.BettingRound(name=bad_name, table=self.table)
                self.assertEqual(context.exception.args[0], messages.msg_not_str.format(type(bad_name).__name__))


    def test_table_type_error(self):

        "Tests type error detection on the field name."

        bad_tables = (1, 'pivot_table', None)

        for bad_table in bad_tables:

            with self.subTest(table=bad_table):
                with self.assertRaises(TypeError) as context:
                    engines.BettingRound(name='test', table=bad_table)
                self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(type(bad_table).__name__))


    def test_min_bet_type_error(self):

        "Tests type error detection on field min_bet."

        bad_amounts = ('300', 300.0, Decimal('300'))

        for bad_amount in bad_amounts:

            with self.subTest(min_bet=bad_amount):
                with self.assertRaises(TypeError) as context:
                    engines.BettingRound('test', self.table, min_bet=bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))


    def test_starting_player_type_error(self):

        "Tests type error detection on field starting_player."

        bad_starting_players = ('Dino', 1)

        for bad_starting_player in bad_starting_players:

            with self.subTest(starting_player=bad_starting_player):
                with self.assertRaises(TypeError) as context:
                    engines.BettingRound('test', self.table, starting_player=bad_starting_player)
                self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(type(bad_starting_player).__name__))


    def test_stopping_player_type_error(self):

        "Tests type error detection on field stopping_player."

        bad_stopping_players = ('Dino', 1)

        for bad_stopping_player in bad_stopping_players:

            with self.subTest(stopping_player=bad_stopping_player):
                with self.assertRaises(TypeError) as context:
                    engines.BettingRound('test', self.table, stopping_player=bad_stopping_player)
                self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(type(bad_stopping_player).__name__))


    def test_min_bet_value_error(self):

        "Tests value error detection on field min_bet."

        bad_min_bet = 0
        with self.subTest('zero minimum bet'):
            with self.assertRaises(ValueError) as context:
                engines.BettingRound('test', self.table, min_bet=bad_min_bet)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_min_bet))

        bad_min_bet = -10
        with self.subTest('negative minimum bet'):
            with self.assertRaises(ValueError) as context:
                engines.BettingRound('test', self.table, min_bet=bad_min_bet)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_min_bet))


    def test_starting_player_value_error(self):

        "Tests value error detection on field starting_player."

        player_not_in_table = structures.Player('Zero', 1000)
        with self.subTest('player not in table'):
            with self.assertRaises(ValueError) as context:
                engines.BettingRound('test', self.table, starting_player=player_not_in_table)
            self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(player_not_in_table.name))


    def test_stopping_player_value_error(self):

        "Tests value error detection on field stopping_player."

        player_not_in_table = structures.Player('Zero', 1000)
        with self.subTest('player not in table'):
            with self.assertRaises(ValueError) as context:
                engines.BettingRound('test', self.table, stopping_player=player_not_in_table)
            self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(player_not_in_table.name))


    def test_valid_input(self):

        "Tests valid input."

        betting_round = engines.BettingRound('test', self.table)
        with self.subTest('simple instantiation'):
            self.assertEqual(betting_round.name, 'test')
            self.assertEqual(betting_round.table, self.table)
            self.assertEqual(betting_round.table.min_bet, 1)
            self.assertEqual(betting_round.table.starting_player, self.Andy)
            self.assertEqual(betting_round.table.stopping_player, self.Fomi)
            self.assertEqual(betting_round.lap_counts, 0)
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.open_fold_allowed)
            self.assertFalse(betting_round.raise_invalid_actions)

        betting_round = engines.BettingRound(
            'test',
            self.table,
            min_bet = 10,
            starting_player = self.Boa,
            stopping_player = self.Epa,
            open_fold_allowed = True,
            raise_invalid_actions = True,
        )
        with self.subTest('complex instantiation'):
            self.assertEqual(betting_round.name, 'test')
            self.assertEqual(betting_round.table, self.table)
            self.assertEqual(betting_round.table.min_bet, 10)
            self.assertEqual(betting_round.table.starting_player, self.Boa)
            self.assertEqual(betting_round.table.stopping_player, self.Epa)
            self.assertEqual(betting_round.lap_counts, 0)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.open_fold_allowed)
            self.assertTrue(betting_round.raise_invalid_actions)


class TestBettingRoundMethods(BaseTestCase):


    "Runs unit tests on betting round methods."


    def test_type_errors_in_dealing_related_methods(self):

        "Tests type error detection in methods related to dealing."

        betting_round = engines.BettingRound('test', self.table)

        methods = (
            betting_round.deal_cards_to_players,
            betting_round.deal_common_cards,
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
                    engines.BettingRound.reset_betting_round_states(bad_table)
                self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(type(bad_table).__name__))


    def test_value_errors_in_dealing_related_methods(self):

        "Tests type error detection in methods related to dealing."

        betting_round = engines.BettingRound('test', self.table)

        methods = (
            betting_round.deal_cards_to_players,
            betting_round.deal_common_cards,
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

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before card deal'):
            self.assertEqual(len(self.table.deck), 52)
            self.assertEqual(len(self.table.common_cards), 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 0)

        betting_round.deal_cards_to_players(2)

        with self.subTest('after card deal to players'):
            self.assertEqual(len(self.table.deck), 40)
            self.assertEqual(len(self.table.common_cards), 0)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)

        betting_round.deal_common_cards(5)

        with self.subTest('after card deal to table'):
            self.assertEqual(len(self.table.deck), 35)
            self.assertEqual(len(self.table.common_cards), 5)
            for player in self.setup_players:
                self.assertEqual(len(player.cards), 2)


    def test_valid_input_in_reset_method(self):

        "Tests valid input detection in the reset method."

        with self.subTest('initial states'):
            self.assertEqual(self.table.min_raise_increase, 1)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            for player in self.table.players:
                self.assertFalse(player.has_played)
                self.assertIsNone(player.requested_action)

        self.table.set_min_raise_increase(100)
        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_stopping_player(self.Coral)
        for player in self.table.players:
            player.mark_has_played()
            player.request_action(structures.Action(constants.ACTION_CHECK))

        with self.subTest('updated states'):
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.stopping_player, self.Coral)
            for player in self.table.players:
                self.assertTrue(player.has_played)
                self.assertEqual(player.requested_action, structures.Action(constants.ACTION_CHECK))

        engines.BettingRound.reset_betting_round_states(self.table)

        with self.subTest('final states'):
            self.assertEqual(self.table.min_raise_increase, 1)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            for player in self.table.players:
                self.assertFalse(player.has_played)
                self.assertIsNone(player.requested_action)


    def test_counter_increase_method(self):

        "Tests valid input in the method that increases the counter."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before counter increase'):
            self.assertEqual(betting_round.lap_counts, 0)

        for i in range(1, 6):
            with self.subTest('counter increase', i=i):
                betting_round.increase_counter()
                self.assertEqual(betting_round.lap_counts, i)


    def test_action_ranges_method(self):

        "Tests valid input in the method that retrieves the action ranges."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before counter increase'):
            self.assertDictEqual(
                betting_round.get_action_ranges(),
                {
                    constants.ACTION_CHECK: range(0, 1),
                    constants.ACTION_BET: range(1, 1001)
                }
            )


class TestBettingRoundFlow(BaseTestCase):


    "Runs unit tests on betting round flow."


    def test_flow_behaviour_from_boolean_setup(self):

        "Tests flow behaviour depending on boolean parameters."

        open_fold_allowed = True
        raise_invalid_actions = True
        betting_round = engines.BettingRound(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(betting_round.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(betting_round.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_CALL, 100))
            with self.assertRaises(RuntimeError) as context:
                self.assertEqual(next(betting_round.listen()), self.Andy)
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            with self.assertRaises(StopIteration) as context:
                next(betting_round.listen())
            self.assertIsNone(context.exception.value)

        self.setUp()
        open_fold_allowed = True
        raise_invalid_actions = False
        betting_round = engines.BettingRound(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(betting_round.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(betting_round.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_CALL, 100))
            self.assertEqual(next(betting_round.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_FOLD))
            self.assertEqual(next(betting_round.listen()), self.Boa)

        self.setUp()
        open_fold_allowed = False
        raise_invalid_actions = True
        betting_round = engines.BettingRound(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(betting_round.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(betting_round.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_FOLD))
            with self.assertRaises(RuntimeError) as context:
                self.assertEqual(next(betting_round.listen()), self.Andy)
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            with self.assertRaises(StopIteration) as context:
                next(betting_round.listen())
            self.assertIsNone(context.exception.value)


        self.setUp()
        open_fold_allowed = False
        raise_invalid_actions = False
        betting_round = engines.BettingRound(
            'test',
            self.table,
            open_fold_allowed = open_fold_allowed,
            raise_invalid_actions = raise_invalid_actions
        )

        with self.subTest(open_fold_allowed=open_fold_allowed, raise_invalid_actions=raise_invalid_actions):
            self.assertEqual(next(betting_round.listen()), self.Andy)
            # no action parsed
            self.assertEqual(next(betting_round.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_FOLD))
            self.assertEqual(next(betting_round.listen()), self.Andy)
            self.Andy.request_action(structures.Action(constants.ACTION_CHECK))
            self.assertEqual(next(betting_round.listen()), self.Boa)


    def test_flow_without_context_manager_with_function_next_missing_close(self):

        "Tests flow with function next, missing close method."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)

        for player in self.setup_players:
            with self.subTest(player=player):
                self.assertEqual(next(betting_round.listen()), player)
                player.request_action(structures.Action(constants.ACTION_CHECK))
                self.assertFalse(betting_round.is_completed)

        with self.subTest('after actions'):
            with self.assertRaises(StopIteration) as context:
                next(betting_round.listen())
            self.assertIsNone(context.exception.value)
            self.assertFalse(betting_round.is_completed)


    def test_flow_without_context_manager_with_function_next_calling_close_at_end(self):

        "Tests flow with function next, using close method at the end."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)

        for player in self.setup_players:
            with self.subTest(player=player):
                self.assertEqual(next(betting_round.listen()), player)
                player.request_action(structures.Action(constants.ACTION_CHECK))
                self.assertFalse(betting_round.is_completed)

        betting_round.close()
        with self.subTest('after actions'):
            self.assertTrue(betting_round.is_completed)


    def test_flow_without_context_manager_with_function_next_calling_close_before_end(self):

        "Tests flow with function next, using close method before the end."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)

        with self.subTest('close before time'):
            with self.assertRaises(RuntimeError) as context:
                betting_round.close()
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)


    def test_flow_without_context_manager_with_loop_missing_close(self):

        "Tests flow with for loop, missing close method."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)

        for i, player in enumerate(betting_round.listen()):
            with self.subTest(player=self.setup_players[i]):
                self.assertEqual(player, self.setup_players[i])
                player.request_action(structures.Action(constants.ACTION_CHECK))
                self.assertFalse(betting_round.is_completed)

        with self.subTest('after actions'):
            self.assertFalse(betting_round.is_completed)


    def test_flow_without_context_manager_with_loop_calling_close_at_end(self):

        "Tests flow with for loop, calling close method at the end."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)

        for i, player in enumerate(betting_round.listen()):
            with self.subTest(player=self.setup_players[i]):
                self.assertEqual(player, self.setup_players[i])
                player.request_action(structures.Action(constants.ACTION_CHECK))
                self.assertFalse(betting_round.is_completed)

        betting_round.close()
        with self.subTest('after actions'):
            self.assertTrue(betting_round.is_completed)


    def test_flow_without_context_manager_with_loop_calling_close_before_end(self):

        "Tests flow with for loop, calling close method at the end."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)

        with self.subTest('close before time'):
            with self.assertRaises(RuntimeError) as context:
                for _ in betting_round.listen():
                    betting_round.close()
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)


    def test_flow_with_context_manager_with_function_next_missing_close(self):

        "Tests flow with function next, missing close method."

        with engines.BettingRound('test', self.table) as betting_round:

            for player in betting_round.listen():
                player.request_action(structures.Action(constants.ACTION_CHECK))

            with self.subTest('after actions inside manager'):
                self.assertFalse(betting_round.is_completed)

        with self.subTest('after actions outside manager'):
            self.assertTrue(betting_round.is_completed)


    def test_flow_with_context_manager_with_function_next_calling_close_at_end(self):

        "Tests flow with function next, using close method at the end."

        with engines.BettingRound('test', self.table) as betting_round:

            for player in betting_round.listen():
                player.request_action(structures.Action(constants.ACTION_CHECK))
            betting_round.close() ## redundant, the context manager closes the round

            with self.subTest('after actions inside manager'):
                self.assertTrue(betting_round.is_completed)

        with self.subTest('after actions outside manager'):
            self.assertTrue(betting_round.is_completed)


    def test_flow_with_context_manager_with_function_next_calling_close_before_end(self):

        "Tests flow with function next, using close method before the end."

        with self.assertRaises(RuntimeError) as context:
            with engines.BettingRound('test', self.table) as betting_round:
                betting_round.close()

        self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
        self.assertFalse(betting_round.is_completed)


    def test_flow_with_context_manager_with_function_next_overloading_the_listener(self):

        "Tests flow with function next, using close method at the end."

        with self.assertRaises(RuntimeError) as context:
            with engines.BettingRound('test', self.table) as betting_round:
                for player in self.setup_players:
                    player = next(betting_round.listen())
                    player.request_action(structures.Action(constants.ACTION_CHECK))
                next(betting_round.listen()) ## overloaded listener

        self.assertEqual(context.exception.args[0], messages.msg_overloaded_betting_round_message)


if __name__ == '__main__':
    main()