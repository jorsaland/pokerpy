"""
Defines unit tests on set_action_effects function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class TestBettingRoundSetActionEffectsFunction(TestCase):


    """
    Runs unit tests on set_action_effects function.
    """


    def test_parse_a_fold(self):


        """
        Runs test cases where a fold is parsed.
        """

        
        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),            
        ])
        table.set_stopping_player(Dino)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 1)
        self.assertEqual(table.full_raise_increase, 1)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_FOLD),
        )

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertTrue(Boa.has_played)
        self.assertTrue(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 1)
        self.assertEqual(table.full_raise_increase, 1)


    def test_parse_a_check(self):


        """
        Runs test cases where a check is parsed.
        """


        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),            
        ])
        table.set_stopping_player(Dino)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 1)
        self.assertEqual(table.full_raise_increase, 1)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_CHECK),
        )

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 1)
        self.assertEqual(table.full_raise_increase, 1)


    def test_parse_a_call_smaller_than_a_full_call(self):


        """
        Runs test cases where a call smaller than a full call is parsed (all-in).
        """


        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 1),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),
        ])
        table.set_stopping_player(Dino)
        table.set_amount_level(2)
        table.set_full_amount_level(2)
        table.set_full_bet(2)
        table.set_full_raise_increase(2)


        # States before

        self.assertEqual(Boa.stack, 1)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 2)
        self.assertEqual(table.full_amount_level, 2)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_CALL, 1),
        )

        self.assertEqual(Boa.stack, 0)
        self.assertEqual(Boa.amount, 1)
        self.assertEqual(Boa.pot_participation, 1)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 2)
        self.assertEqual(table.full_amount_level, 2)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


    def test_parse_a_call_equal_to_a_full_call(self):


        """
        Runs test cases where a call equal to a full call is parsed.
        """


        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),
        ])
        table.set_stopping_player(Dino)
        table.set_amount_level(2)
        table.set_full_amount_level(2)
        table.set_full_bet(2)
        table.set_full_raise_increase(2)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 2)
        self.assertEqual(table.full_amount_level, 2)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_CALL, 2),
        )

        self.assertEqual(Boa.stack, 8)
        self.assertEqual(Boa.amount, 2)
        self.assertEqual(Boa.pot_participation, 2)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 2)
        self.assertEqual(table.full_amount_level, 2)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


    def test_parse_a_bet_smaller_than_a_full_bet(self):


        """
        Runs test cases where a bet smaller than a full bet is parsed (all-in).
        """


        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 1),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(2)


        # States before

        self.assertEqual(Boa.stack, 1)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_BET, 1),
        )

        self.assertEqual(Boa.stack, 0)
        self.assertEqual(Boa.amount, 1)
        self.assertEqual(Boa.pot_participation, 1)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 1)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


    def test_parse_a_bet_equal_to_a_full_bet(self):


        """
        Runs test cases where a bet equal to a full bet is parsed.
        """


        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(2)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_BET, 2),
        )

        self.assertEqual(Boa.stack, 8)
        self.assertEqual(Boa.amount, 2)
        self.assertEqual(Boa.pot_participation, 2)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 2)
        self.assertEqual(table.full_amount_level, 2)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


    def test_parse_a_bet_larger_than_a_full_bet(self):


        """
        Runs test cases where a bet larger than a full bet is parsed.
        """


        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(2)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 2)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_BET, 3),
        )

        self.assertEqual(Boa.stack, 7)
        self.assertEqual(Boa.amount, 3)
        self.assertEqual(Boa.pot_participation, 3)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 3)
        self.assertEqual(table.full_amount_level, 3)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


    def test_parse_a_raise_smaller_than_a_full_raise_not_having_played(self):


        """
        Runs test cases where a raise with an amount smaller than a full raise is parsed (all-in), not having played yet.
        """


        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 7),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(3)
        table.set_amount_level(5)
        table.set_full_amount_level(5)


        # States before

        self.assertEqual(Boa.stack, 7)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 5)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_RAISE, 7),
        )

        self.assertEqual(Boa.stack, 0)
        self.assertEqual(Boa.amount, 7)
        self.assertEqual(Boa.pot_participation, 7)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 7)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


    def test_parse_a_raise_smaller_than_a_full_raise_having_bet_previously(self):


        """
        Runs test cases where a raise with an amount smaller than a full raise is parsed (all-in), having bet previously.
        """


        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 5),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(3)
        table.set_amount_level(5)
        table.set_full_amount_level(5)
        Boa.increase_amount(2)
        Boa.increase_pot_participation(2)


        # States before

        self.assertEqual(Boa.stack, 5)
        self.assertEqual(Boa.amount, 2)
        self.assertEqual(Boa.pot_participation, 2)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 5)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_RAISE, 5),
        )

        self.assertEqual(Boa.stack, 0)
        self.assertEqual(Boa.amount, 7)
        self.assertEqual(Boa.pot_participation, 7)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 7)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


    def test_parse_a_raise_equal_to_a_full_raise_not_having_played(self):

        """
        Runs test cases where a raise with an amount equal to a full raise is parsed, not having played yet.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(3)
        table.set_amount_level(5)
        table.set_full_amount_level(5)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 5)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_RAISE, 8),
        )

        self.assertEqual(Boa.stack, 2)
        self.assertEqual(Boa.amount, 8)
        self.assertEqual(Boa.pot_participation, 8)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 8)
        self.assertEqual(table.full_amount_level, 8)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


    def test_parse_a_raise_equal_to_a_full_raise_having_bet_previously(self):

        """
        Runs test cases where a raise with an amount equal to a full raise is parsed, having bet previously.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(3)
        table.set_amount_level(5)
        table.set_full_amount_level(5)
        Boa.increase_amount(2)
        Boa.increase_pot_participation(2)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 2)
        self.assertEqual(Boa.pot_participation, 2)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 5)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_RAISE, 6),
        )

        self.assertEqual(Boa.stack, 4)
        self.assertEqual(Boa.amount, 8)
        self.assertEqual(Boa.pot_participation, 8)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 8)
        self.assertEqual(table.full_amount_level, 8)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


    def test_parse_a_raise_larger_than_a_full_raise_not_having_played(self):


        """
        Runs test cases where a raise with an amount larger than a full raise is parsed, not having played yet.
        """


        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(3)
        table.set_amount_level(5)
        table.set_full_amount_level(5)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 0)
        self.assertEqual(Boa.pot_participation, 0)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 5)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_RAISE, 9),
        )

        self.assertEqual(Boa.stack, 1)
        self.assertEqual(Boa.amount, 9)
        self.assertEqual(Boa.pot_participation, 9)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 9)
        self.assertEqual(table.full_amount_level, 9)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 4)


    def test_parse_a_raise_larger_than_a_full_raise_having_bet_previously(self):


        """
        Runs test cases where a raise with an amount larger than a full raise is parsed, having bet previously.
        """


        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.set_stopping_player(Dino)
        table.set_full_bet(2)
        table.set_full_raise_increase(3)
        table.set_amount_level(5)
        table.set_full_amount_level(5)
        Boa.increase_amount(2)
        Boa.increase_pot_participation(2)


        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.amount, 2)
        self.assertEqual(Boa.pot_participation, 2)
        self.assertFalse(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.amount_level, 5)
        self.assertEqual(table.full_amount_level, 5)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 3)


        # States after

        engines.set_action_effects(
            table = table,
            player = Boa,
            action = structures.Action(constants.ACTION_RAISE, 7),
        )

        self.assertEqual(Boa.stack, 3)
        self.assertEqual(Boa.amount, 9)
        self.assertEqual(Boa.pot_participation, 9)
        self.assertTrue(Boa.has_played)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.stopping_player, Andy)
        self.assertEqual(table.amount_level, 9)
        self.assertEqual(table.full_amount_level, 9)
        self.assertEqual(table.full_bet, 2)
        self.assertEqual(table.full_raise_increase, 4)


if __name__ == '__main__':
    main()