"""
Demo 0.6-A

This demo is made from Demo 0.6-E. Now, players start with different amounts of chips, making side
pots possible. Also, the rules to choose an action are now available in the BettingRound instance,
so the player can just check them and choose one.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
import random


import pokerpy as pk


# Constants

PREFLOP = 'pre-flop'
after_preflop_round_names = [
    (FLOP := 'flop'),
    (TURN := 'turn'),
    (RIVER := 'river'),
]

ANTE = 1
SMALL_BLIND = 5
BIG_BLIND = 10

STACK_MIN_SIZE = BIG_BLIND + ANTE
STACK_MAX_SIZE = 10_000

player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']


def display_cards_and_money(table: pk.Table):
    print('\n--------------------------------------------------')
    print(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | central pot: {table.central_pot} | split pot: {table.split_pot}')
    for player in table.players_in_hand:
        hand = figure_out_hand(player.cards + table.common_cards)
        if hand is not None:
            player.assign_hand(hand)
        print(
            f"{player.name}'s cards: {''.join(str(c) for c in player.cards) if player.cards else None} | "
            f"hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''} | "
            f"stack: {player.stack} | pot participation: {player.pot_participation}"
        )
    print('--------------------------------------------------\n')


def figure_out_hand(cards: list[pk.Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return pk.Hand(cards)
    
    possible_hands = [pk.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)


def ante_round(table: pk.Table):

    print(f'\n============ PLACING ANTES ============\n')

    for player in table.players:
        player.remove_from_stack(ANTE)
        player.add_to_pot_participation(ANTE)
        table.add_to_central_pot(ANTE)

    display_cards_and_money(table)
    print(f'\n============ ANTES PLACED ============\n')


def preflop(table: pk.Table, open_fold_allowed: bool):

    print(f'\n============ STARTING {PREFLOP.upper()} ============\n')

    betting_round = pk.BettingRound(
        name = PREFLOP,
        table = table,
        smallest_bet_amount = BIG_BLIND,
        starting_player = table.players[2],
        open_fold_allowed = open_fold_allowed
    )

    with betting_round:

        # Place small blind

        small_blind_player = table.players[0]
        small_blind_player.remove_from_stack(SMALL_BLIND)
        small_blind_player.add_to_current_amount(SMALL_BLIND)
        small_blind_player.add_to_pot_participation(SMALL_BLIND)

        print(
            f"{small_blind_player.name} PLACES SMALL BLIND {SMALL_BLIND} "
            f"({small_blind_player.name}'s current amount: {small_blind_player.current_amount} | stack: {small_blind_player.stack})"
            "\n"
        )

        # Place big blind

        big_blind_player = table.players[1]
        big_blind_player.remove_from_stack(BIG_BLIND)
        big_blind_player.add_to_current_amount(BIG_BLIND)
        big_blind_player.add_to_pot_participation(BIG_BLIND)
        table.set_current_level(BIG_BLIND)
        table.set_complete_current_level(BIG_BLIND)

        print(
            f"{big_blind_player.name} PLACES BIG BLIND {BIG_BLIND} "
            f"({big_blind_player.name}'s current amount: {big_blind_player.current_amount} | stack: {big_blind_player.stack})"
        )
        print(f'TABLE CURRENT LEVEL: {table.current_level}\n')

        # Place random big blinds (players who want to enter before waiting for their turn to place the big blind)

        for player in table.players[2:]:

            if random.randint(0, 1):
                player.remove_from_stack(BIG_BLIND)
                player.add_to_current_amount(BIG_BLIND)
                player.add_to_pot_participation(BIG_BLIND)
                print(
                    f"{player.name} PLACES BIG BLIND {BIG_BLIND} TO ENTER THE GAME WITHOUT WAITING "
                    f"({player.name}'s current amount: {player.current_amount} | stack: {player.stack})"
                )
                print(f'TABLE CURRENT LEVEL: {table.current_level}\n')

        # Deal pre-flop

        betting_round.deal_cards_to_players(2)
        print()

        # Let players to play

        for player in betting_round.listen():

            amount_to_full_call = table.current_level - player.current_amount
            if amount_to_full_call == 0:
                print(f'To full bet: {betting_round.table.full_bet} | current amount: {player.current_amount}')
            else:
                print(f'To full call: {amount_to_full_call} | to full raise: {betting_round.table.complete_current_level + betting_round.table.full_raise_increase} | current amount: {player.current_amount}')

            range_by_action = betting_round.get_action_ranges()
            action_name, amount_range = random.choice([
                (name, amount_range) for name, amount_range in range_by_action.items() if amount_range is not None
            ])
            if action_name == pk.ACTION_BET:
                action_amount = random.randint(table.central_pot//2, table.central_pot*2)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            elif action_name == pk.ACTION_RAISE:
                amount_to_call = range_by_action[pk.ACTION_CALL][0]
                smallest_amount = amount_to_call + betting_round.table.full_raise_increase
                action_amount = random.randint(smallest_amount, smallest_amount*3)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            else:
                action_amount = amount_range[0]
            player.request_action(pk.Action(name=action_name, amount=action_amount))

    display_cards_and_money(table)
    print(f'\n============ ENDING {PREFLOP.upper()} ============\n')


def postflop(table: pk.Table, betting_round_name: str, open_fold_allowed: bool):

    # Break before starting if only remains one player
    if len(table.players_in_hand) == 1:
        return False

    print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

    betting_round = pk.BettingRound(
        name = betting_round_name,
        table = table,
        smallest_bet_amount = BIG_BLIND,
        starting_player = table.players[0],
        open_fold_allowed = open_fold_allowed,
    )

    with betting_round:

        # Deal three cards to table if round is flop and one if is turn or river

        if betting_round_name == FLOP:
            betting_round.deal_common_cards(3)        
        else:
            betting_round.deal_common_cards(1)
        print()

        # Let players to play
        for player in betting_round.listen():

            amount_to_full_call = table.current_level - player.current_amount
            if amount_to_full_call == 0:
                print(f'To full bet: {betting_round.table.full_bet} | current amount: {player.current_amount}')
            else:
                print(f'To full call: {amount_to_full_call} | to full raise: {betting_round.table.complete_current_level + betting_round.table.full_raise_increase} | current amount: {player.current_amount}')

            range_by_action = betting_round.get_action_ranges()
            action_name, amount_range = random.choice([
                (name, amount_range) for name, amount_range in range_by_action.items() if amount_range is not None
            ])
            if action_name == pk.ACTION_BET:
                action_amount = random.randint(table.central_pot//2, table.central_pot*2)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            elif action_name == pk.ACTION_RAISE:
                amount_to_call = range_by_action[pk.ACTION_CALL][0]
                smallest_amount = amount_to_call + betting_round.table.full_raise_increase
                action_amount = random.randint(smallest_amount, smallest_amount*3)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            else:
                action_amount = amount_range[0]
            player.request_action(pk.Action(name=action_name, amount=action_amount))


    display_cards_and_money(table)
    print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    return True


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
    ante_round(table)
    preflop(table, open_fold_allowed)

    for betting_round_name in after_preflop_round_names:
        keep_playing = postflop(table, betting_round_name, open_fold_allowed)
        if not keep_playing:
            break

    if len(table.players_in_hand) > 1:
        print(f'\n============ SHOWDOWN! ============\n')
        pk.showdown(table)
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        pk.showdown(table)


def game():

    # Cycle not allowing open fold
    table = pk.Table([pk.Player(name, stack=random.randint(STACK_MIN_SIZE, STACK_MAX_SIZE)) for name in player_names])
    pk.reset_cycle_states(table)
    cycle(table)
    input('\n\n--- ENTER ---\n')

    # Cycle allowing open fold
    table = pk.Table([pk.Player(name, stack=random.randint(STACK_MIN_SIZE, STACK_MAX_SIZE)) for name in player_names])
    pk.reset_cycle_states(table)
    cycle(table, open_fold_allowed=True)
    input('\n\n--- ENTER ---\n')


def main():
    game()

if __name__ == '__main__':
    main()