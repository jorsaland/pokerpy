"""
Runs unit tests on managers section.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRound(TestCase):


    """
    Runs unit tests on class BettingRound.
    """


    # Resources


    player_names = ['Andy', 'Boa', 'Coral', 'Dino']
    players = [pk.Player(name) for name in player_names]
    table = pk.Table(players)


    def test_iterator_object(self):


        """
        Runs test cases to check if the context manager opens an iterator object.
        """


        def run_iterator_on_for_loop():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                for player in betting_round:
                    player.request(pk.ACTION_CHECK)
                    awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(run_iterator_on_for_loop(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def run_iterator_on_next_function():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

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

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(run_iterator_on_next_function(), ['Andy', 'Boa', 'Coral', 'Dino'])


if __name__ == '__main__':
    main()