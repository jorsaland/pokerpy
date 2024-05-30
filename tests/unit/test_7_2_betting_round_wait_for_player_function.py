"""
Defines unit tests on wait_for_player function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRoundWaitForPlayerFunction(TestCase):


    """
    Runs unit tests on wait_for_player function.
    """


    def test_under_bet_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object when round is under bet.
        """


        def parse_single_valid_action():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=True)

            # Request action
            player = next(generator)
            player.request_action(pk.ACTION_CALL)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_single_valid_action(), pk.ACTION_CALL)        


        def parse_single_invalid_action():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=True)

            # Request action
            player = next(generator)
            player.request_action(pk.ACTION_CHECK)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_single_invalid_action())


        def parse_multiple_invalid_actions():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=True)

            # Request actions
            player = next(generator)
            player.request_action(pk.ACTION_CHECK)
            player = next(generator)
            player.request_action(pk.ACTION_BET)
            player = next(generator)
            player.request_action(pk.ACTION_CHECK)
            player = next(generator)
            player.request_action(pk.ACTION_BET)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_multiple_invalid_actions())       


        def parse_multiple_invalid_actions_and_final_valid_action():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=True)

            # Request actions
            player = next(generator)
            player.request_action(pk.ACTION_CHECK)
            player = next(generator)
            player.request_action(pk.ACTION_BET)
            player = next(generator)
            player.request_action(pk.ACTION_CHECK)
            player = next(generator)
            player.request_action(pk.ACTION_BET)
            player = next(generator)
            player.request_action(pk.ACTION_BET)
            player = next(generator)
            player.request_action(pk.ACTION_CALL)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_multiple_invalid_actions_and_final_valid_action(), pk.ACTION_CALL)


    def test_not_under_bet_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object when round is not under bet.
        """


        def parse_single_valid_action():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=False)

            # Request action
            player = next(generator)
            player.request_action(pk.ACTION_CHECK)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_single_valid_action(), pk.ACTION_CHECK)        


        def parse_single_invalid_action():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=False)

            # Request action
            player = next(generator)
            player.request_action(pk.ACTION_RAISE)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_single_invalid_action())


        def parse_multiple_invalid_actions():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=False)

            # Request actions
            player = next(generator)
            player.request_action(pk.ACTION_RAISE)
            player = next(generator)
            player.request_action(pk.ACTION_CALL)
            player = next(generator)
            player.request_action(pk.ACTION_FOLD)
            player = next(generator)
            player.request_action(pk.ACTION_RAISE)
            player = next(generator)
            player.request_action(pk.ACTION_CALL)
            player = next(generator)
            player.request_action(pk.ACTION_FOLD)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_multiple_invalid_actions())


        def parse_multiple_invalid_actions_and_final_valid_action():

            player = pk.Player('Lugia')
            generator = pk.managers.wait_for_player(player, is_under_bet=False)

            # Request actions
            player = next(generator)
            player.request_action(pk.ACTION_RAISE)
            player = next(generator)
            player.request_action(pk.ACTION_CALL)
            player = next(generator)
            player.request_action(pk.ACTION_FOLD)
            player = next(generator)
            player.request_action(pk.ACTION_RAISE)
            player = next(generator)
            player.request_action(pk.ACTION_CALL)
            player = next(generator)
            player.request_action(pk.ACTION_FOLD)
            player = next(generator)
            player.request_action(pk.ACTION_CHECK)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_multiple_invalid_actions_and_final_valid_action(), pk.ACTION_CHECK)


if __name__ == '__main__':
    main()