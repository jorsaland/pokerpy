"""
Defines unit tests on BettingRound class.
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
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]
        self.Andy, self.Boa, self.Coral, self.Dino, self.Epa, self.Fomi = self.setup_players

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


    def test_valid_input(self):

        "Tests valid input."

        betting_round = engines.BettingRound('test', self.table)
        with self.subTest('simple instantiation'):
            self.assertEqual(betting_round.name, 'test')
            self.assertEqual(betting_round.table, self.table)
            self.assertEqual(betting_round.lap_counts, 0)
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.open_fold_allowed)

        betting_round = engines.BettingRound(
            'test',
            self.table,
            open_fold_allowed = True,
        )
        with self.subTest('complex instantiation'):
            self.assertEqual(betting_round.name, 'test')
            self.assertEqual(betting_round.table, self.table)
            self.assertEqual(betting_round.lap_counts, 0)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.open_fold_allowed)


class TestBettingRoundMethods(BaseTestCase):


    "Runs unit tests on betting round methods."


    def test_type_errors_in_reset_method(self):

        "Tests type error detection in the reset method."

        bad_tables = (1, 'pivot_table', None)

        for bad_table in bad_tables:

            with self.subTest(table=bad_table):
                with self.assertRaises(TypeError) as context:
                    engines.BettingRound.reset_betting_round_states(bad_table)
                self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(type(bad_table).__name__))


    def test_valid_input_in_reset_method(self):

        "Tests valid input detection in the reset method."

        with self.subTest('initial states'):
            self.assertEqual(self.table.min_raise_increase, 1)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            for player in self.table.players:
                self.assertFalse(player.has_played)

        self.table.set_min_raise_increase(100)
        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)
        self.table.set_stopping_player(self.Coral)
        for player in self.table.players:
            player.mark_has_played()

        with self.subTest('updated states'):
            self.assertEqual(self.table.min_raise_increase, 100)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.stopping_player, self.Coral)
            for player in self.table.players:
                self.assertTrue(player.has_played)

        engines.BettingRound.reset_betting_round_states(self.table)

        with self.subTest('final states'):
            self.assertEqual(self.table.min_raise_increase, 1)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            for player in self.table.players:
                self.assertFalse(player.has_played)


class TestBettingRoundFlowWithoutContextManagerWithFunctionNext(BaseTestCase):


    "Runs unit tests on betting round flow without context manager, using function next."


    def test_no_context_manager_flow_with_function_next_missing_close(self):

        "Tests flow with function next, missing close method."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        for player in self.setup_players:
            with self.subTest(player=player):
                await_state = next(betting_round.listen())
                self.assertEqual(await_state.player, player)
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)
            await_state.request_action(structures.Action(constants.ACTION_CHECK))

        with self.subTest('after actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)


    def test_no_context_manager_flow_with_function_next_calling_close_at_end(self):

        "Tests flow with function next, using close method at the end."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        for player in self.setup_players:
            with self.subTest(player=player):
                await_state = next(betting_round.listen())
                self.assertEqual(await_state.player, player)
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)
            await_state.request_action(structures.Action(constants.ACTION_CHECK))

        with self.subTest('after actions, before close'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        betting_round.close() # needed in this case to finish the generator after the last action

        with self.subTest('after actions, after close'):
            self.assertTrue(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_no_context_manager_flow_with_function_next_calling_close_before_end_skipping_action(self):

        "Tests flow with function next, using close method before the end, skipping the awaited action."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        with self.subTest('close before time'):
            next(betting_round.listen())
            with self.assertRaises(RuntimeError) as context:
                betting_round.close()

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_no_context_manager_flow_with_function_next_calling_close_before_end_parsing_valid_action(self):

        "Tests flow with function next, using close method before the end, after parsing a valid action during await."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        with self.subTest('close before time'):
            await_state = next(betting_round.listen())
            await_state.request_action(structures.Action(constants.ACTION_CHECK))
            with self.assertRaises(RuntimeError) as context:
                betting_round.close()

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_no_context_manager_flow_with_function_next_calling_close_before_end_parsing_invalid_action(self):

        "Tests flow with function next, using close method before the end, after parsing an invalid action during await."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        with self.subTest('close before time'):
            await_state = next(betting_round.listen())
            await_state.request_action(structures.Action(constants.ACTION_RAISE, 100))
            with self.assertRaises(RuntimeError) as context:
                betting_round.close()

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


class TestBettingRoundFlowWithoutContextManagerWithLoop(BaseTestCase):


    "Runs unit tests on betting round flow without context manager, using a for loop."


    def test_no_context_manager_flow_with_loop_missing_close(self):

        "Tests flow with for loop, missing close method."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        for i, await_state in enumerate(betting_round.listen()):
            with self.subTest(player=self.setup_players[i]):
                self.assertEqual(await_state.player, self.setup_players[i])
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)
            await_state.request_action(structures.Action(constants.ACTION_CHECK))

        with self.subTest('after actions'):
            self.assertTrue(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)


    def test_no_context_manager_flow_with_loop_calling_close_at_end(self):

        "Tests flow with for loop, calling close method at the end."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        for i, await_state in enumerate(betting_round.listen()):
            with self.subTest(player=self.setup_players[i]):
                self.assertEqual(await_state.player, self.setup_players[i])
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)
            await_state.request_action(structures.Action(constants.ACTION_CHECK))

        with self.subTest('after actions, before close'):
            self.assertTrue(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        betting_round.close() # redundant, the loop already closed the generator

        with self.subTest('after actions, after close'):
            self.assertTrue(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_no_context_manager_flow_with_loop_calling_close_before_end_skipping_action(self):

        "Tests flow with for loop, calling close method at the end, skipping the awaited action."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        with self.subTest('close before time'):
            context = None
            for _ in betting_round.listen():
                with self.assertRaises(RuntimeError) as context:
                    betting_round.close()
                break

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_no_context_manager_flow_with_loop_calling_close_before_end_parsing_valid_action(self):

        "Tests flow with for loop, calling close method at the end, after parsing a valid action during await."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        with self.subTest('close before time'):
            context = None
            for await_state in betting_round.listen():
                await_state.request_action(structures.Action(constants.ACTION_CHECK))
                with self.assertRaises(RuntimeError) as context:
                    betting_round.close()
                break

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_no_context_manager_flow_with_loop_calling_close_before_end_parsing_invalid_action(self):

        "Tests flow with for loop, calling close method at the end, after parsing an invalid action during await."

        betting_round = engines.BettingRound('test', self.table)

        with self.subTest('before actions'):
            self.assertFalse(betting_round.is_completed)
            self.assertFalse(betting_round.is_closed)

        with self.subTest('close before time'):
            context = None
            for await_state in betting_round.listen():
                await_state.request_action(structures.Action(constants.ACTION_RAISE, 100))
                with self.assertRaises(RuntimeError) as context:
                    betting_round.close()
                break

        with self.subTest('after close'):
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


class TestBettingRoundFlowWithContextManagerWithFunctionNext(BaseTestCase):


    "Runs unit tests on betting round flow with context manager, using function next."


    def test_context_manager_flow_with_function_next_missing_close(self):

        "Tests flow with function next, missing close method."

        with engines.BettingRound('test', self.table) as betting_round:

            with self.subTest('before actions'):
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)

            for player in self.setup_players:
                with self.subTest(player=player):
                    await_state = next(betting_round.listen())
                    self.assertEqual(await_state.player, player)
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)
                await_state.request_action(structures.Action(constants.ACTION_CHECK))

            with self.subTest('after actions'):
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)

        with self.subTest('after exit'):
            self.assertTrue(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_function_next_calling_close_at_end(self):

        "Tests flow with function next, using close method at the end."

        with engines.BettingRound('test', self.table) as betting_round:

            with self.subTest('before actions'):
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)

            for player in self.setup_players:
                with self.subTest(player=player):
                    await_state = next(betting_round.listen())
                    self.assertEqual(await_state.player, player)
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)
                await_state.request_action(structures.Action(constants.ACTION_CHECK))

            with self.subTest('after actions, before close'):
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)

            betting_round.close() # redundant, the context manager will close the generator

            with self.subTest('after actions, after close'):
                self.assertTrue(betting_round.is_completed)
                self.assertTrue(betting_round.is_closed)

        with self.subTest('after exit'):
            self.assertTrue(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_function_next_calling_close_before_end_skipping_action(self):

        "Tests flow with function next, using close method before the end, skipping the awaited action."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('close before time'):
                    next(betting_round.listen())
                    with self.assertRaises(RuntimeError) as inner_context:
                        betting_round.close()
                    self.assertEqual(inner_context.exception.args[0], messages.msg_betting_round_was_not_completed)
                    self.assertFalse(betting_round.is_completed)
                    self.assertTrue(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_function_next_calling_close_before_end_parsing_valid_action(self):

        "Tests flow with function next, using close method before the end, after parsing a valid action during await."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('close before time'):
                    await_state = next(betting_round.listen())
                    await_state.request_action(structures.Action(constants.ACTION_CHECK))
                    with self.assertRaises(RuntimeError) as inner_context:
                        betting_round.close()
                    self.assertEqual(inner_context.exception.args[0], messages.msg_betting_round_was_not_completed)
                    self.assertFalse(betting_round.is_completed)
                    self.assertTrue(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_function_next_calling_close_before_end_parsing_invalid_action(self):

        "Tests flow with function next, using close method before the end, after parsing an invalid action during await."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('close before time'):
                    await_state = next(betting_round.listen())
                    await_state.request_action(structures.Action(constants.ACTION_RAISE, 100))
                    with self.assertRaises(RuntimeError) as inner_context:
                        betting_round.close()
                    self.assertEqual(inner_context.exception.args[0], messages.msg_forbidden_action)
                    self.assertFalse(betting_round.is_completed)
                    self.assertTrue(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_forbidden_action)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


class TestBettingRoundFlowWithContextManagerWithLoop(BaseTestCase):


    "Runs unit tests on betting round flow with context manager, using a for loop."


    def test_context_manager_flow_with_loop_missing_close(self):

        "Tests flow with for loop, missing close method."

        with engines.BettingRound('test', self.table) as betting_round:

            with self.subTest('before actions'):
                self.assertFalse(betting_round.is_completed)

            for i, await_state in enumerate(betting_round.listen()):
                with self.subTest(player=self.setup_players[i]):
                    self.assertEqual(await_state.player, self.setup_players[i])
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)
                await_state.request_action(structures.Action(constants.ACTION_CHECK))

            with self.subTest('after actions'):
                self.assertTrue(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)

        with self.subTest('after exit'):
            self.assertTrue(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_loop_calling_close_at_end(self):

        "Tests flow with for loop, calling close method at the end."

        with engines.BettingRound('test', self.table) as betting_round:

            with self.subTest('before actions'):
                self.assertFalse(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)

            for i, await_state in enumerate(betting_round.listen()):
                with self.subTest(player=self.setup_players[i]):
                    self.assertEqual(await_state.player, self.setup_players[i])
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)
                await_state.request_action(structures.Action(constants.ACTION_CHECK))

            with self.subTest('after actions, before close'):
                self.assertTrue(betting_round.is_completed)
                self.assertFalse(betting_round.is_closed)

            betting_round.close() # redundant, the loop already closed the generator

            with self.subTest('after actions, after close'):
                self.assertTrue(betting_round.is_completed)
                self.assertTrue(betting_round.is_closed)

        with self.subTest('after exit'):
            self.assertTrue(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_loop_calling_close_before_end_skipping_action(self):

        "Tests flow with for loop, calling close method at the end, skipping the awaited action."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('close before time'):
                    inner_context = None
                    for _ in betting_round.listen():
                        with self.assertRaises(RuntimeError) as inner_context:
                            betting_round.close()
                        break
                    self.assertEqual(inner_context.exception.args[0], messages.msg_betting_round_was_not_completed)
                    self.assertFalse(betting_round.is_completed)
                    self.assertTrue(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_loop_calling_close_before_end_parsing_valid_action(self):

        "Tests flow with for loop, calling close method at the end, after parsing a valid action during await."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('close before time'):
                    inner_context = None
                    for await_state in betting_round.listen():
                        await_state.request_action(structures.Action(constants.ACTION_CHECK))
                        with self.assertRaises(RuntimeError) as inner_context:
                            betting_round.close()
                        break
                    self.assertEqual(inner_context.exception.args[0], messages.msg_betting_round_was_not_completed)
                    self.assertFalse(betting_round.is_completed)
                    self.assertTrue(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_with_loop_calling_close_before_end_parsing_invalid_action(self):

        "Tests flow with for loop, calling close method at the end, after parsing an invalid action during await."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('close before time'):
                    inner_context = None
                    for await_state in betting_round.listen():
                        await_state.request_action(structures.Action(constants.ACTION_RAISE, 100))
                        with self.assertRaises(RuntimeError) as inner_context:
                            betting_round.close()
                        break
                    self.assertEqual(inner_context.exception.args[0], messages.msg_forbidden_action)
                    self.assertFalse(betting_round.is_completed)
                    self.assertTrue(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_forbidden_action)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


class TestBettingRoundFlowWithContextManagerWithSpecialCases(BaseTestCase):


    "Runs unit tests on betting round flow with context manager, with special cases."


    def test_context_manager_flow_overloading_the_listener(self):

        "Tests flow, overloading the listener."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)

                for i, await_state in enumerate(betting_round.listen()):
                    with self.subTest(player=self.setup_players[i]):
                        self.assertEqual(await_state.player, self.setup_players[i])
                        self.assertFalse(betting_round.is_completed)
                        self.assertFalse(betting_round.is_closed)
                    await_state.request_action(structures.Action(constants.ACTION_CHECK))

                with self.subTest('after actions'):
                    self.assertTrue(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('listener overload'):
                    with self.assertRaises(StopIteration) as inner_context:
                        next(betting_round.listen())
                    self.assertIsNone(inner_context.exception.value)
                    self.assertTrue(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)
                raise inner_context.exception
        
        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_overloaded_betting_round)
            self.assertTrue(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_exiting_before_end_skipping_action(self):

        "Tests flow with function next, exiting the context manager before the end, skipping the awaited action."

        with self.assertRaises(RuntimeError) as context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('first await'):
                    next(betting_round.listen())
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

        with self.subTest('after exit'):
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_exiting_before_end_parsing_valid_action(self):

        "Tests flow with function next, exiting the context manager before the end, after parsing a valid action during await."

        with self.assertRaises(RuntimeError) as context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('first await'):
                    await_state = next(betting_round.listen())
                    await_state.request_action(structures.Action(constants.ACTION_CHECK))
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

        with self.subTest('after exit'):
            self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_exiting_before_end_parsing_invalid_action(self):

        "Tests flow with function next, exiting the context manager before the end, after parsing an invalid action during await."

        with self.assertRaises(RuntimeError) as context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('first await'):
                    await_state = next(betting_round.listen())
                    await_state.request_action(structures.Action(constants.ACTION_RAISE, 100))
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

        with self.subTest('after exit'):
            self.assertEqual(context.exception.args[0], messages.msg_forbidden_action)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_raising_exception_due_to_skipped_action(self):

        "Tests flow, raising an exception inside the context manager due to a skipped action."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('raise exception'):
                    next(betting_round.listen())
                    with self.assertRaises(RuntimeError) as inner_context:
                        next(betting_round.listen())
                    self.assertEqual(inner_context.exception.args[0], messages.msg_missing_action)
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_missing_action)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_raising_exception_due_to_invalid_action(self):

        "Tests flow, raising an exception inside the context manager due to an invalid action."

        with self.assertRaises(RuntimeError) as outer_context:

            with engines.BettingRound('test', self.table) as betting_round:

                with self.subTest('before actions'):
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)

                with self.subTest('raise exception'):
                    await_state = next(betting_round.listen())
                    await_state.request_action(structures.Action(constants.ACTION_RAISE, 100))
                    with self.assertRaises(RuntimeError) as inner_context:
                        next(betting_round.listen())
                    self.assertEqual(inner_context.exception.args[0], messages.msg_forbidden_action)
                    self.assertFalse(betting_round.is_completed)
                    self.assertFalse(betting_round.is_closed)
                raise inner_context.exception

        with self.subTest('after exit'):
            self.assertEqual(outer_context.exception.args[0], messages.msg_forbidden_action)
            self.assertFalse(betting_round.is_completed)
            self.assertTrue(betting_round.is_closed)


    def test_context_manager_flow_raising_external_exception(self):

        "Tests flow, raising an exception inside the context manager due to an external exception."

        exception_types = (
            ValueError,
            TypeError,
            RuntimeError, # needed to test collisions with internal RuntimeError instances
        )

        for exception_type in exception_types:

            with self.assertRaises(exception_type) as outer_context:

                with engines.BettingRound('test', self.table) as betting_round:

                    with self.subTest('before actions', exception_type=exception_type.__name__):
                        self.assertFalse(betting_round.is_completed)
                        self.assertFalse(betting_round.is_closed)

                    with self.subTest('raise exception', exception_type=exception_type.__name__):
                        next(betting_round.listen())
                        with self.assertRaises(exception_type) as inner_context:
                            raise(exception_type('test'))
                        self.assertEqual(inner_context.exception.args[0], 'test')
                        self.assertFalse(betting_round.is_completed)
                        self.assertFalse(betting_round.is_closed)
                    raise inner_context.exception

            with self.subTest('after exit', exception_type=exception_type.__name__):
                self.assertEqual(outer_context.exception.args[0], 'test')
                self.assertFalse(betting_round.is_completed)
                self.assertTrue(betting_round.is_closed)


if __name__ == '__main__':
    main()