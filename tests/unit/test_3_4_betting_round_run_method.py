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
            table.activate_all_players()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(parse_as_many_actions_as_expected(), all_players)


        def parse_less_actions_than_expected():

            table = structures.Table(all_players)
            table.activate_all_players()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            # Dino is missing

            return awaited_players

        self.assertEqual(parse_less_actions_than_expected(), [Andy, Boa, Coral])


        def parse_more_actions_than_expected():

            table = structures.Table(all_players)
            table.activate_all_players()

            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Unexpected action
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            return awaited_players

        with self.assertRaises(StopIteration):
            parse_more_actions_than_expected()


    def test_action_chain(self):


        """
        Runs test cases to check run method can correctly chain multiple actions.
        """


        def all_check():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [structures.Player(name) for name in player_names]
            table = structures.Table(players)
            
            table.activate_all_players()
            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(all_check(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def bet_and_folds():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [structures.Player(name) for name in player_names]
            table = structures.Table(players)

            table.activate_all_players()
            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Andy
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Andy
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_and_folds(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def bet_and_calls():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [structures.Player(name) for name in player_names]
            table = structures.Table(players)

            table.activate_all_players()
            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Andy
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Andy
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_and_calls(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def bet_raises_and_folds():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [structures.Player(name) for name in player_names]
            table = structures.Table(players)

            table.activate_all_players()
            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Dino
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Dino
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            # Coral already folded

            player = next(betting_round) # Dino, responding to Boa
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            # Andy already folded

            # Boa is the only remaining player

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_raises_and_folds(), ['Andy', 'Boa', 'Coral', 'Dino', 'Andy', 'Boa', 'Dino'])


        def bet_raises_and_calls():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [structures.Player(name) for name in player_names]
            table = structures.Table(players)

            table.activate_all_players()
            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Dino
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Dino
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Boa
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            # Every player has responded to Boa

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_raises_and_calls(), ['Andy', 'Boa', 'Coral', 'Dino', 'Andy', 'Boa', 'Coral', 'Dino', 'Andy'])


        def bet_raises_folds_and_calls():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [structures.Player(name) for name in player_names]
            table = structures.Table(players)

            table.activate_all_players()
            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Andy
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Dino
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Dino
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            # Coral already folded
            
            player = next(betting_round) # Dino, responding to Boa
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Boa
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            # Every remaining player has responded to Boa

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_raises_folds_and_calls(), ['Andy', 'Boa', 'Coral', 'Dino', 'Andy', 'Boa', 'Dino', 'Andy'])


        def all_actions():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [structures.Player(name) for name in player_names]
            table = structures.Table(players)

            table.activate_all_players()
            awaited_players: list[structures.Player] = []

            betting_round_cm = managers.BettingRound(name='round', table=table)
            betting_round = betting_round_cm.run()

            player = next(betting_round) # Andy
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Boa
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Coral
            player.request(constants.ACTION_CHECK)
            awaited_players.append(player)

            player = next(betting_round) # Dino
            player.request(constants.ACTION_BET)
            awaited_players.append(player)

            player = next(betting_round) # Andy, responding to Dino
            player.request(constants.ACTION_FOLD)
            awaited_players.append(player)

            player = next(betting_round) # Boa, responding to Dino
            player.request(constants.ACTION_RAISE)
            awaited_players.append(player)

            player = next(betting_round) # Coral, responding to Boa
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            player = next(betting_round) # Dino, responding to Boa
            player.request(constants.ACTION_CALL)
            awaited_players.append(player)

            # Andy already folded

            # Every remaining player has responded to Boa

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(all_actions(), ['Andy', 'Boa', 'Coral', 'Dino', 'Andy', 'Boa', 'Coral', 'Dino'])

if __name__ == '__main__':
    main()