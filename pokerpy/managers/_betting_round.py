"""
Defines the class that represents a betting round context manager.
"""


from pokerpy.constants import ACTION_FOLD, aggressive_actions
from pokerpy.structures import Table
from pokerpy.utils import action_is_valid


class BettingRound:


    """
    Represents a betting round context manager.
    """


    def __init__(self, *, name: str, table: Table):
        self.name = name
        self.table = table
    
    def __enter__(self):
        yield from self.start()
    
    def __exit__(self, *_):
        self.end()


    def start(self):

        """
        Inicia la ronda de apuestas, permitiendo que los jugadores alternen sus turnos.
        """

        print(f'\n=== STARTING {self.name.upper()} ===\n')

        # Prepare betting round before players start their actions
        self.table.reset_betting_round_states()
        self.table.deal(self.name)
        
        # All players are itered but only active ones are allowed to act
        for player in self.table.players:

            # Determine whether betting round should be stopped or not
            if len(self.table.active_players) == 1:
                print(f'<< ONLY ONE ACTIVE PLAYER ({self.table.active_players[0].name.upper()})... ENDING ROUND >>\n')
                break

            # Determine whether player should be allowed to play or not
            if player not in self.table.active_players:
                print(f'<< {player.name.upper()} ALREADY FOLDED >>\n')
                continue

            # Player keeps its turn until selects a valid action
            while True:

                # Wait for player's action
                print(f'Waiting for {player.name}...')
                yield player

                # Determine wheter action is valid or not
                action = player.requested_action
                if action is not None and action_is_valid(action=action, is_under_bet=self.table.is_under_bet):
                    print(f'{player.name} {action}s\n'.upper())
                    break
                print(f'<< INVALID ACTION: {action.upper()} >>')
            
            # Determine whether round becomes under bet or not
            if action in aggressive_actions:
                self.table.is_under_bet = True
            
            # Determine whether the player becomes inactive or not
            if action == ACTION_FOLD:
                self.table.active_players.remove(player)



    def end(self):

        """
        Finaliza la ronda de apuestas.
        """

        print(f'=== ENDING {self.name.upper()} ===\n')