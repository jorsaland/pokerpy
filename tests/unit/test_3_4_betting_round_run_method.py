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


if __name__ == '__main__':
    main()