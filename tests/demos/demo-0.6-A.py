"""
Demo 0.6-A

This demo is made from Demo 0.5-E. Now, players have finite amounts of chips, making possible
all-in situations. They all start with the same amount of chips, to ensure there are no side pots
in case of all-in. Also, the new behaviour of the BettingRound context manager is applied.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
import random


import pokerpy as pk


# Constants

ANTE_ROUND = 'ante round'
PREFLOP = 'pre-flop'
after_preflop_round_names = [
    (FLOP := 'flop'),
    (TURN := 'turn'),
    (RIVER := 'river'),
]

ANTE = 1
SMALL_BLIND = 5
BIG_BLIND = 10
STACK_SIZE = 10_000

player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']


def display_cards_and_money(table: pk.Table, active_players: list[pk.Player] | None = None):
    if active_players is None:
        active_players = table.players
    print('\n--------------------------------------------------')
    print(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | central pot: {table.central_pot}')
    for player in active_players:
        hand = figure_out_hand(player.cards + table.common_cards)
        if hand is not None:
            player.assign_hand(hand)
        print(
            f"{player.name}'s cards: {''.join(str(c) for c in player.cards) if player.cards else None} | "
            f"hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''} | "
            f"stack: {player.stack}"
        )
    print('--------------------------------------------------\n')


def figure_out_hand(cards: list[pk.Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return pk.Hand(cards)
    
    possible_hands = [pk.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)


def ante_round(table: pk.Table, open_fold_allowed: bool):

    print(f'\n============ STARTING {ANTE_ROUND.upper()} ============\n')

    with pk.BettingRound(ANTE_ROUND, table, open_fold_allowed=open_fold_allowed) as betting_round:

        # Reset betting round states regarding to table and players
        table.reset_betting_round_states()

        # Place antes
        for player in table.players:
            player.remove_from_stack(ANTE)
            player.add_to_current_amount(ANTE)
            print(f"{player.name} PLACES ANTE {ANTE} ({player.name}'s current amount: {player.current_amount} | stack: {player.stack})")
        table.add_to_current_amount(ANTE)
        print(f'TABLE CURRENT AMOUNT: {table.current_amount}\n')

        # Let players to check
        for player in betting_round.listen():
            action = pk.Action(pk.ACTION_CHECK)
            player.request_action(action)

    display_cards_and_money(table, betting_round.active_players)
    print(f'\n============ ENDING {ANTE_ROUND.upper()} ============\n')


def preflop(table: pk.Table, open_fold_allowed: bool):

    print(f'\n============ STARTING {PREFLOP.upper()} ============\n')

    betting_round = pk.BettingRound(
        name = PREFLOP,
        table = table,
        smallest_bet = BIG_BLIND,
        starting_player = table.players[2],
        stopping_player = table.players[1],
        open_fold_allowed = open_fold_allowed
    )

    with betting_round:

        # Reset betting round states regarding to table and players

        table.reset_betting_round_states()

        # Place small blind

        small_blind_player = table.players[0]
        small_blind_player.remove_from_stack(SMALL_BLIND)
        small_blind_player.add_to_current_amount(SMALL_BLIND)
        table.add_to_current_amount(SMALL_BLIND)

        print(
            f"{small_blind_player.name} PLACES SMALL BLIND {SMALL_BLIND} "
            f"({small_blind_player.name}'s current amount: {small_blind_player.current_amount} | stack: {small_blind_player.stack})"
        )
        print(f'TABLE CURRENT AMOUNT: {table.current_amount}\n')

        # Place big blind

        big_blind_player = table.players[1]
        big_blind_player.remove_from_stack(BIG_BLIND)
        big_blind_player.add_to_current_amount(BIG_BLIND)
        table.add_to_current_amount(BIG_BLIND - SMALL_BLIND)

        print(
            f"{big_blind_player.name} PLACES BIG BLIND {BIG_BLIND} "
            f"({big_blind_player.name}'s current amount: {big_blind_player.current_amount} | stack: {big_blind_player.stack})"
        )
        print(f'TABLE CURRENT AMOUNT: {table.current_amount}\n')

        # Place random big blinds (players who want to enter before waiting for their turn to place the big blind)

        for player in table.players[2:]:

            if random.randint(0, 1):
                player.remove_from_stack(BIG_BLIND)
                player.add_to_current_amount(BIG_BLIND)
                print(
                    f"{player.name} PLACES BIG BLIND {BIG_BLIND} TO ENTER THE GAME WITHOUT WAITING "
                    f"({player.name}'s current amount: {player.current_amount} | stack: {player.stack})"
                )
                print(f'TABLE CURRENT AMOUNT: {table.current_amount}\n')

        # Deal pre-flop

        betting_round.deal_cards_to_players(2)
        print()

        # Let players to play

        for player in betting_round.listen():

            amount_to_call = table.current_amount - player.current_amount

            if amount_to_call == 0:
                if not betting_round.open_fold_allowed:
                    action_name = random.choice([pk.ACTION_CHECK, pk.ACTION_BET])
                else:
                    action_name = random.choice([pk.ACTION_CHECK, pk.ACTION_BET, pk.ACTION_FOLD])
            elif amount_to_call >= player.stack:
                action_name = random.choice([pk.ACTION_CALL, pk.ACTION_FOLD])
            else:
                action_name = random.choice([pk.ACTION_CALL, pk.ACTION_FOLD, pk.ACTION_RAISE])

            if action_name in [pk.ACTION_FOLD, pk.ACTION_CHECK]:
                action = pk.Action(action_name, 0)
            elif action_name == pk.ACTION_CALL:
                action = pk.Action(action_name, amount_to_call)
            elif action_name == pk.ACTION_BET:
                amount = random.randint(BIG_BLIND, BIG_BLIND*5)
                if amount > player.stack:
                    amount = player.stack
                action = pk.Action(action_name, amount)
            elif action_name == pk.ACTION_RAISE:
                smallest_amount = amount_to_call + betting_round.smallest_rising_amount
                amount = random.randint(smallest_amount, smallest_amount*3)
                if amount > player.stack:
                    amount = player.stack
                action = pk.Action(action_name, amount)
            else:
                raise RuntimeError('we live in a society')

            if amount_to_call == 0:
                print(f'To bet: {betting_round.smallest_bet}')
            else:
                print(f'To call: {amount_to_call} | to raise: {amount_to_call + betting_round.smallest_rising_amount}')
            player.request_action(action)

    display_cards_and_money(table, betting_round.active_players)
    print(f'\n============ ENDING {PREFLOP.upper()} ============\n')

    return betting_round.active_players


def postflop(table: pk.Table, betting_round_name: str, active_players: list[pk.Player], open_fold_allowed: bool):

    # Break before starting if only remains one player
    if len(active_players) == 1:
        return False, active_players

    print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

    betting_round = pk.BettingRound(
        name = betting_round_name,
        table = table,
        smallest_bet = BIG_BLIND,
        active_players = active_players,
        open_fold_allowed = open_fold_allowed,
    )

    with betting_round:

        # Reset betting round states regarding to table and players

        table.reset_betting_round_states()

        # Deal three cards to table if round is flop and one if is turn or river

        if betting_round_name == FLOP:
            betting_round.deal_common_cards(3)        
        else:
            betting_round.deal_common_cards(1)
        print()

        # Let players to play

        for player in betting_round.listen():

            amount_to_call = table.current_amount - player.current_amount

            if amount_to_call == 0:
                if not betting_round.open_fold_allowed:
                    action_name = random.choice([pk.ACTION_CHECK, pk.ACTION_BET])
                else:
                    action_name = random.choice([pk.ACTION_CHECK, pk.ACTION_BET, pk.ACTION_FOLD])
            elif amount_to_call >= player.stack:
                action_name = random.choice([pk.ACTION_CALL, pk.ACTION_FOLD])
            else:
                action_name = random.choice([pk.ACTION_CALL, pk.ACTION_FOLD, pk.ACTION_RAISE])

            if action_name in [pk.ACTION_FOLD, pk.ACTION_CHECK]:
                action = pk.Action(action_name, 0)
            elif action_name == pk.ACTION_CALL:
                action = pk.Action(action_name, amount_to_call)
            elif action_name == pk. ACTION_BET:
                amount = random.randint(table.central_pot//2, table.central_pot*2)
                if amount > player.stack:
                    amount = player.stack
                action = pk.Action(action_name, amount)
            elif action_name == pk.ACTION_RAISE:
                smallest_amount = amount_to_call + betting_round.smallest_rising_amount
                amount = random.randint(smallest_amount, smallest_amount*3)
                if amount > player.stack:
                    amount = player.stack
                action = pk.Action(action_name, amount)
            else:
                raise RuntimeError('we live in a society')

            if amount_to_call == 0:
                print(f'To bet: {betting_round.smallest_bet}')
            else:
                print(f'To call: {amount_to_call} | to raise: {amount_to_call + betting_round.smallest_rising_amount}')
            player.request_action(action)

    display_cards_and_money(table, betting_round.active_players)
    print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    return True, betting_round.active_players


def cycle(table: pk.Table, *, open_fold_allowed: bool = False):

    if not open_fold_allowed:
        print('\n======================================================'  )
        print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
        print(  '======================================================\n')
    
    else:
        print('\n=============================================='  )
        print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
        print(  '==============================================\n')

    display_cards_and_money(table)
    ante_round(table, open_fold_allowed)
    active_players = preflop(table, open_fold_allowed)

    for betting_round_name in after_preflop_round_names:
        keep_playing, active_players = postflop(table, betting_round_name, list(active_players), open_fold_allowed)
        if not keep_playing:
            break

    if len(active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')
        pk.showdown(active_players, table.central_pot)
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        pk.no_showdown(active_players, table.central_pot)


def game():

    # Cycle not allowing open fold
    table = pk.Table([pk.Player(name, stack=STACK_SIZE) for name in player_names])
    table.reset_cycle_states()
    cycle(table)
    input('\n\n--- ENTER ---\n')

    # Cycle allowing open fold
    table = pk.Table([pk.Player(name, stack=STACK_SIZE) for name in player_names])
    table.reset_cycle_states()
    cycle(table, open_fold_allowed=True)
    input('\n\n--- ENTER ---\n')


def main():
    game()

if __name__ == '__main__':
    main()