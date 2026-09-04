"""
Defines unit tests on set_action_effects function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class BasePlayersTestCase(TestCase):


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

        self.table = structures.Table(self.setup_players, min_bet=100)

        self.Andy = self.setup_players[0]
        self.Boa = self.setup_players[1]
        self.Coral = self.setup_players[2]
        self.Dino = self.setup_players[3]
        self.Epa = self.setup_players[4]
        self.Fomi = self.setup_players[5]


class TestBettingRoundSetActionEffectsFunctionOnPassiveActions(BasePlayersTestCase):


    "Runs unit tests on set_action_effects function on passive actions."


    def test_fold_effects(self):

        "Tests effects after folding."

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_FOLD),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertTrue(self.Boa.has_played)
            self.assertTrue(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_check_effects(self):

        "Tests effects after checking."

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_CHECK),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_call_effects_if_under_call_given_not_player_bet_level(self):

        """
        Tests effects after calling an amount smaller than a full call, given the player bet level is zero.
        """

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(100)

        self.table.set_bet_level(200)
        self.table.set_full_bet_level(200)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 100)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_CALL, 100),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_call_effects_if_under_call_given_player_bet_level(self):

        """
        Tests effects after calling an amount smaller than a full call, given the player has previously bet or called.
        """

        self.Boa.mark_has_played()
        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 100)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_CALL, 100),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 200)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_call_effects_if_full_call_given_not_player_bet_level(self):

        """
        Tests effects after calling an amount equal to a full call, given the player bet level is zero.
        """

        self.table.set_bet_level(200)
        self.table.set_full_bet_level(200)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_CALL, 200),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 800)
            self.assertEqual(self.Boa.bet_level, 200)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_call_effects_if_full_call_given_player_bet_level(self):

        """
        Tests effects after calling an amount equal to a full call, given the player has previously bet or called.
        """

        self.Boa.mark_has_played()
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_CALL, 200),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 700)
            self.assertEqual(self.Boa.bet_level, 300)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


class TestBettingRoundSetActionEffectsFunctionOnBetting(BasePlayersTestCase):


    "Runs unit tests on set_action_effects function on betting."


    def test_bet_effects_if_under_bet_given_no_bet_level(self):

        "Tests effects after betting an amount smaller than a minimum beet, given bet level is zero."

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(50)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 50)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 50),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 50)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 50)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_under_bet_given_previous_under_bet(self):

        """
        Tests effects after betting an amount smaller than a minimum bet, given previous under bet.
        """

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(50)

        self.table.set_bet_level(20)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 50)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 20)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 50)
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 50)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 50)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_under_bet_given_big_blind_bet_level(self):

        """
        Tests effects after betting an amount smaller than a minimum bet, given player placed big
        blind and nobody raised.
        """

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(50)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 50)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 50),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 150)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 150)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_under_bet_given_big_blind_and_previous_under_bet(self):

        """
        Tests effects after betting an amount smaller than a minimum bet, given player placed big
        blind and somebody previously bet an amount smaller than a minimum bet.
        """

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(50)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(120)
        self.table.set_full_bet_level(100)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 50)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 120)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 50),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 150)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 150)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_min_bet_given_no_bet_level(self):

        "Tests effects after betting an amount equal to a minimum bet, given bet level is zero."

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 100),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_min_bet_given_previous_under_bet(self):

        "Tests effects after betting an amount equal to a minimum bet, given previous under bet."

        self.table.set_bet_level(50)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 50)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 100)
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_min_bet_given_big_blind_bet_level(self):

        """
        Tests effects after betting an amount equal to a minimum bet, given player placed big
        blind and nobody raised.
        """

        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 100)
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 800)
            self.assertEqual(self.Boa.bet_level, 200)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_min_bet_given_big_blind_and_previous_under_bet(self):

        """
        Tests effects after betting an amount equal to a minimum bet, given player placed big
        blind and somebody previously bet an amount smaller than a minimum bet.
        """

        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(150)
        self.table.set_full_bet_level(100)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 150)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 100)
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 800)
            self.assertEqual(self.Boa.bet_level, 200)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)


    def test_bet_effects_if_over_bet_given_no_bet_level(self):

        "Tests effects after betting an amount larger than a minimum bet, given bet level is zero."

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 0)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 300),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 700)
            self.assertEqual(self.Boa.bet_level, 300)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 300)


    def test_bet_effects_if_over_bet_given_previous_under_bet(self):

        "Tests effects after betting an amount larger than a minimum bet, given previous under bet."

        self.table.set_bet_level(50)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 50)
            self.assertEqual(self.table.full_bet_level, 0)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 300)
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 700)
            self.assertEqual(self.Boa.bet_level, 300)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 300)


    def test_bet_effects_if_over_bet_given_big_blind_bet_level(self):

        """
        Tests effects after betting an amount larger than a minimum bet, given player placed big
        blind and nobody raised.
        """

        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(100)
        self.table.set_full_bet_level(100)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 100)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 300)
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 600)
            self.assertEqual(self.Boa.bet_level, 400)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 400)
            self.assertEqual(self.table.full_bet_level, 400)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 300)


    def test_bet_effects_if_over_bet_given_big_blind_and_previous_under_bet(self):

        """
        Tests effects after betting an amount larger than a minimum bet, given player placed big
        blind and somebody previously bet an amount smaller than a minimum bet.
        """

        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(150)
        self.table.set_full_bet_level(100)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 150)
            self.assertEqual(self.table.full_bet_level, 100)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 100)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_BET, 300)
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 600)
            self.assertEqual(self.Boa.bet_level, 400)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 400)
            self.assertEqual(self.table.full_bet_level, 400)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 300)


class TestBettingRoundSetActionEffectsFunctionOnRaising(BasePlayersTestCase):


    "Runs unit tests on set_action_effects function on raising."


    def test_raise_effects_if_under_raise_given_previous_bet(self):

        "Tests effects after raising on a bet an amount smaller than a minimum raise, given has not played yet."

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(300)

        self.table.set_bet_level(200)
        self.table.set_full_bet_level(200)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 300)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 300),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 300)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_raise_effects_if_under_raise_given_previous_raise(self):

        "Tests effects after re-raising an amount smaller than a minimum raise, given has not played yet."

        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(400)

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 400)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 400),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 400)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 400)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_raise_effects_if_under_raise_given_previous_raise_on_player(self):

        "Tests effects after re-raising an amount smaller than a minimum raise, given has already bet or called."

        self.Boa.mark_has_played()
        self.Boa.decrease_stack(self.Boa.stack)
        self.Boa.increase_stack(300)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 300)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 300),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 0)
            self.assertEqual(self.Boa.bet_level, 400)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 400)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_raise_effects_if_min_raise_given_previous_bet(self):

        "Tests effects after raising on a bet an amount equal to a minimum raise, given has not played yet."

        self.table.set_bet_level(200)
        self.table.set_full_bet_level(200)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 400),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 600)
            self.assertEqual(self.Boa.bet_level, 400)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 400)
            self.assertEqual(self.table.full_bet_level, 400)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_raise_effects_if_full_raise_given_previous_raise(self):

        "Tests effects after re-raising an amount equal to a minimum raise, given has not played yet."

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 500),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 500)
            self.assertEqual(self.Boa.bet_level, 500)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 500)
            self.assertEqual(self.table.full_bet_level, 500)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_raise_effects_if_full_raise_given_previous_raise_on_player(self):

        "Tests effects after re-raising an amount equal to a minimum raise, given has already bet or called."

        self.Boa.mark_has_played()
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 400),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 500)
            self.assertEqual(self.Boa.bet_level, 500)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 500)
            self.assertEqual(self.table.full_bet_level, 500)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)


    def test_raise_effects_if_over_raise_given_previous_bet(self):

        "Tests effects after raising on a bet an amount larger than a minimum raise, given has not played yet."

        self.table.set_bet_level(200)
        self.table.set_full_bet_level(200)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 200)
            self.assertEqual(self.table.full_bet_level, 200)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 500),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 500)
            self.assertEqual(self.Boa.bet_level, 500)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 500)
            self.assertEqual(self.table.full_bet_level, 500)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 300)


    def test_raise_effects_if_over_raise_given_previous_raise(self):

        "Tests effects after re-raising an amount larger than a minimum raise, given has not played yet."

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 1000)
            self.assertEqual(self.Boa.bet_level, 0)
            self.assertFalse(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 600),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 400)
            self.assertEqual(self.Boa.bet_level, 600)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 600)
            self.assertEqual(self.table.full_bet_level, 600)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 300)


    def test_raise_effects_if_over_raise_given_previous_raise_on_player(self):

        "Tests effects after re-raising an amount larger than a minimum raise, given has already bet or called."

        self.Boa.mark_has_played()
        self.Boa.decrease_stack(100)
        self.Boa.increase_bet_level(100)

        self.table.set_bet_level(300)
        self.table.set_full_bet_level(300)
        self.table.set_min_raise_increase(200)

        with self.subTest('before request'):
            self.assertEqual(self.Boa.stack, 900)
            self.assertEqual(self.Boa.bet_level, 100)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Fomi)
            self.assertEqual(self.table.bet_level, 300)
            self.assertEqual(self.table.full_bet_level, 300)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 200)

        engines.set_action_effects(
            table = self.table,
            player = self.Boa,
            action = structures.Action(constants.ACTION_RAISE, 500),
        )

        with self.subTest('after request'):
            self.assertEqual(self.Boa.stack, 400)
            self.assertEqual(self.Boa.bet_level, 600)
            self.assertTrue(self.Boa.has_played)
            self.assertFalse(self.Boa.is_folded)
            self.assertEqual(self.table.stopping_player, self.Andy)
            self.assertEqual(self.table.bet_level, 600)
            self.assertEqual(self.table.full_bet_level, 600)
            self.assertEqual(self.table.min_bet, 100)
            self.assertEqual(self.table.min_raise_increase, 300)


if __name__ == '__main__':
    main()