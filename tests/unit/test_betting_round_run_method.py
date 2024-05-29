"""
Defines unit tests on BettingRound class run method.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRoundRunMethod(TestCase):


    """
    Runs unit tests on BettingRound class run method.
    """


    def test_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object returned by run method.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
            Dino := pk.Player('Dino'),
        ]


        def parse_as_many_actions_as_expected():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(parse_as_many_actions_as_expected(), all_players)


        def parse_less_actions_than_expected():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            # Dino is missing

            return awaited_players

        self.assertEqual(parse_less_actions_than_expected(), [Andy, Boa, Coral])


        def parse_more_actions_than_expected():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Unexpected action
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            return awaited_players

        with self.assertRaises(StopIteration):
            parse_more_actions_than_expected()


    def test_action_chain(self):


        """
        Runs test cases to check run method can correctly chain multiple actions.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
            Dino := pk.Player('Dino'),
        ]


        def all_check():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(all_check(), all_players)


        def bet_and_folds():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Andy
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Andy
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(bet_and_folds(), all_players)


        def bet_and_calls():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Andy
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Andy
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(bet_and_calls(), all_players)


        def bet_raises_and_folds():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Dino
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Dino
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            # Coral already folded

            player = next(betting_round) # Dino, responding to Boa
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            # Andy already folded

            # Boa is the only remaining player

            return awaited_players

        self.assertEqual(bet_raises_and_folds(), [Andy, Boa, Coral, Dino, Andy, Boa, Dino])


        def bet_raises_and_calls():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Dino
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Dino
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Boa
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            # Every player has responded to Boa

            return awaited_players

        self.assertEqual(bet_raises_and_calls(), [Andy, Boa, Coral, Dino, Andy, Boa, Coral, Dino, Andy])


        def bet_raises_folds_and_calls():

            table = pk.Table(all_players)
            table.reset_cycle_states()

            awaited_players: list[pk.Player] = []

            betting_round_cm = pk.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(pk.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Dino
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Dino
            player.request(pk.ACTION_RAISE)
            awaited_players.append(player)

            # Coral already folded
            
            player = next(betting_round) # Dino, responding to Boa
            player.request(pk.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Boa
            player.request(pk.ACTION_CALL)
            awaited_players.append(player)

            # Every remaining player has responded to Boa

            return awaited_players

        self.assertEqual(bet_raises_folds_and_calls(), [Andy, Boa, Coral, Dino, Andy, Boa, Dino, Andy])


if __name__ == '__main__':
    main()