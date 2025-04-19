"""
Defines unit tests on BettingRound class run method.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, structures


class TestBettingRoundRunMethod(TestCase):


    """
    Runs unit tests on BettingRound class run method.
    """


    def test_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object returned by run method.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
            Dino := structures.Player('Dino'),
        ]


        def parse_as_many_actions_as_expected():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(parse_as_many_actions_as_expected(), all_players)


        def parse_less_actions_than_expected():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            # Dino is missing

            return awaited_players

        self.assertEqual(parse_less_actions_than_expected(), [Andy, Boa, Coral])


        def parse_more_actions_than_expected():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(betting_round) # Unexpected action
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            return awaited_players

        with self.assertRaises(StopIteration):
            parse_more_actions_than_expected()


    def test_action_chain(self):


        """
        Runs test cases to check run method can correctly chain multiple actions.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
            Dino := structures.Player('Dino'),
        ]


        def all_check():

            table = structures.Table(all_players, smallest_bet=50)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_CHECK)) # Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_CHECK)) # Boa
            awaited_players.append(player)
            
            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_CHECK)) # Coral
            awaited_players.append(player)
            
            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_CHECK)) # Dino
            awaited_players.append(player)
            
            return awaited_players

        self.assertEqual(all_check(), all_players)


        def bet_and_folds():

            table = structures.Table(all_players, smallest_bet=50)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)
            
            player.request_action(structures.Action(constants.ACTION_BET, 100)) # Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Boa, responding to Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Coral, responding to Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Dino, responding to Andy
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(bet_and_folds(), all_players)


        def bet_and_calls():

            table = structures.Table(all_players, smallest_bet=50)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_BET, 100)) # Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_CALL, 100)) # Boa, responding to Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_CALL, 100)) # Coral, responding to Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_CALL, 100)) # Dino, responding to Andy
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(bet_and_calls(), all_players)


        def bet_raises_and_folds():

            table = structures.Table(all_players, smallest_bet=50)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_BET, 100)) # Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_RAISE, 200)) # Boa, responding to Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 200)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Coral, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 0)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 200)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_RAISE, 400)) # Dino, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 100)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 400)
            self.assertEqual(table.smallest_rising_amount, 200)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Andy, responding to Dino
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 200)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 400)
            self.assertEqual(table.smallest_rising_amount, 200)

            player.request_action(structures.Action(constants.ACTION_RAISE, 600)) # Boa, responding to Dino
            awaited_players.append(player)

            # Coral already folded

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 400)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 800)
            self.assertEqual(table.smallest_rising_amount, 400)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Dino, responding to Boa
            awaited_players.append(player)

            # Andy already folded

            # Boa is the only remaining player

            return awaited_players

        self.assertEqual(bet_raises_and_folds(), [Andy, Boa, Coral, Dino, Andy, Boa, Dino])


        def bet_raises_and_calls():

            table = structures.Table(all_players, smallest_bet=50)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_BET, 50)) # Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 50)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_RAISE, 200)) # Boa, responding to Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 200)
            self.assertEqual(table.smallest_rising_amount, 150)

            player.request_action(structures.Action(constants.ACTION_CALL, 200)) # Coral, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 0)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 200)
            self.assertEqual(table.smallest_rising_amount, 150)

            player.request_action(structures.Action(constants.ACTION_RAISE, 400)) # Dino, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 50)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 400)
            self.assertEqual(table.smallest_rising_amount, 200)

            player.request_action(structures.Action(constants.ACTION_CALL, 350)) # Andy, responding to Dino
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 200)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 400)
            self.assertEqual(table.smallest_rising_amount, 200)

            player.request_action(structures.Action(constants.ACTION_RAISE, 500)) # Boa, responding to Dino
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 200)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 700)
            self.assertEqual(table.smallest_rising_amount, 300)

            player.request_action(structures.Action(constants.ACTION_CALL, 500)) # Coral, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 400)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 700)
            self.assertEqual(table.smallest_rising_amount, 300)

            player.request_action(structures.Action(constants.ACTION_CALL, 300)) # Dino, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 400)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 700)
            self.assertEqual(table.smallest_rising_amount, 300)

            player.request_action(structures.Action(constants.ACTION_CALL, 300)) # Andy, responding to Boa
            awaited_players.append(player)

            # Every player has responded to Boa

            return awaited_players

        self.assertEqual(bet_raises_and_calls(), [Andy, Boa, Coral, Dino, Andy, Boa, Coral, Dino, Andy])


        def bet_raises_folds_and_calls():

            table = structures.Table(all_players, smallest_bet=50)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_BET, 100)) # Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 100)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_RAISE, 200)) # Boa, responding to Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 200)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Coral, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 0)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 200)
            self.assertEqual(table.smallest_rising_amount, 100)

            player.request_action(structures.Action(constants.ACTION_RAISE, 400)) # Dino, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 100)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 400)
            self.assertEqual(table.smallest_rising_amount, 200)

            player.request_action(structures.Action(constants.ACTION_CALL, 300)) # Andy, responding to Dino
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 200)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 400)
            self.assertEqual(table.smallest_rising_amount, 200)

            player.request_action(structures.Action(constants.ACTION_RAISE, 600)) # Boa, responding to Dino
            awaited_players.append(player)

            # Coral already folded
            
            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 400)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 800)
            self.assertEqual(table.smallest_rising_amount, 400)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Dino, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 400)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 800)
            self.assertEqual(table.smallest_rising_amount, 400)

            player.request_action(structures.Action(constants.ACTION_CALL, 400)) # Andy, responding to Boa
            awaited_players.append(player)

            # Every remaining player has responded to Boa

            return awaited_players

        self.assertEqual(bet_raises_folds_and_calls(), [Andy, Boa, Coral, Dino, Andy, Boa, Dino, Andy])


        def all_actions():

            table = structures.Table(all_players, smallest_bet=50)
            table.reset_cycle_states()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_CHECK)) # Andy
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_CHECK)) # Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_CHECK)) # Coral
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 0)
            self.assertEqual(table.stopping_player, Dino)
            self.assertEqual(table.current_amount, 0)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_BET, 50)) # Dino
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Andy.current_amount, 0)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 50)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_FOLD)) # Andy, responding to Dino
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 0)
            self.assertEqual(table.stopping_player, Coral)
            self.assertEqual(table.current_amount, 50)
            self.assertEqual(table.smallest_rising_amount, 50)

            player.request_action(structures.Action(constants.ACTION_RAISE, 200)) # Boa, responding to Dino
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Coral.current_amount, 0)
            self.assertEqual(table.stopping_player, Andy)
            self.assertEqual(table.current_amount, 200)
            self.assertEqual(table.smallest_rising_amount, 150)

            player.request_action(structures.Action(constants.ACTION_RAISE, 350)) # Coral, responding to Boa
            awaited_players.append(player)

            player = next(betting_round)
            self.assertEqual(Dino.current_amount, 50)
            self.assertEqual(table.stopping_player, Boa)
            self.assertEqual(table.current_amount, 350)
            self.assertEqual(table.smallest_rising_amount, 150)

            player.request_action(structures.Action(constants.ACTION_CALL, 300)) # Dino, responding to Coral
            awaited_players.append(player)

            # Andy already folded

            player = next(betting_round)
            self.assertEqual(Boa.current_amount, 200)
            self.assertEqual(table.stopping_player, Boa)
            self.assertEqual(table.current_amount, 350)
            self.assertEqual(table.smallest_rising_amount, 150)

            player.request_action(structures.Action(constants.ACTION_CALL, 150)) # Boa, responding to Coral
            awaited_players.append(player)

            # Every remaining player has responded to Coral

            return awaited_players

        self.assertEqual(all_actions(), [Andy, Boa, Coral, Dino, Andy, Boa, Coral, Dino, Boa])


if __name__ == '__main__':
    main()