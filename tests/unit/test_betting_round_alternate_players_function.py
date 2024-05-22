"""
Defines unit tests on alternate_players function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRoundAlternatePlayersFunction(TestCase):


    """
    Runs unit tests on alternate_players function.
    """


    def test_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object.
        """


        def parse_as_many_actions_as_expected():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(parse_as_many_actions_as_expected(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def parse_less_actions_than_expected():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            # Dino is missing

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(parse_less_actions_than_expected(), ['Andy', 'Boa', 'Coral'])


        def parse_more_actions_than_expected():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Unexpected action
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            print(f'{awaited_player_names = }')
            return awaited_player_names

        with self.assertRaises(StopIteration):
            parse_more_actions_than_expected()


if __name__ == '__main__':
    main()