"""
Defines the class that represents a betting round context manager.
"""


from pokerpy.structures import Table


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

        self.table.reset_betting_round_states()
        self.table.deal(self.name)
        
        for player in self.table.players:

            # Determine whether betting round should be stopped or not
            if len(self.table.active_players) == 1:
                print(f'<< ONLY ONE ACTIVE PLAYER ({self.table.active_players[0].name.upper()})... ENDING ROUND >>')
                break

            # Determine whether player should be allowed to play or not
            if player not in self.table.active_players:
                print(f'<< {player.name.upper()} ALREADY FOLDED >>')
                continue

            yield player


    def end(self):

        """
        Finaliza la ronda de apuestas.
        """

        print(f'\n=== ENDING {self.name.upper()} ===\n')