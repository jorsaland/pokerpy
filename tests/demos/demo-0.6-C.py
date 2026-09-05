"""
Demo 0.6-B

This demo is made from Demo 0.6-B. At least one player is forced to start with less than an ante 
and at least one of the blinds starts with less of the blind amount.
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

ANTE = 10
SMALL_BLIND = 50
BIG_BLIND = 100

STACK_MIN_SIZE = 1
STACK_MAX_SIZE = 100_000

player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']


def display_cards_and_money(table: pk.Table):
    print('\n--------------------------------------------------')
    print(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | pot: {table.pot} | divided pot: {list(table.central_pot)}')
    for player in table.live_players:
        hand = figure_out_hand(player.cards + table.common_cards)
        if hand is not None:
            player.assign_hand(hand)
        print(
            f"{player.name}'s cards: {''.join(str(c) for c in player.cards) if player.cards else None} | "
            f"hand: {f'{str(player.hand)} ({player.hand.category})' if player.hand is not None else None} | "
            f"stack: {player.stack} | bet level: {player.bet_level}"
        )
    print('--------------------------------------------------\n')


def build_players():

    players: list[pk.Player] = []

    if random.randint(0, 1):
        players.append(pk.Player(player_names[0], random.randrange(STACK_MIN_SIZE, SMALL_BLIND)))
        players.append(pk.Player(player_names[1], random.randrange(STACK_MIN_SIZE, STACK_MAX_SIZE)))
    else:
        players.append(pk.Player(player_names[0], random.randrange(STACK_MIN_SIZE, STACK_MAX_SIZE)))
        players.append(pk.Player(player_names[1], random.randrange(STACK_MIN_SIZE, BIG_BLIND)))

    nerfed_ante_name, nerfed_blind_name = random.sample(player_names[2:], k=2)
    for name in player_names[2:]:
        if name == nerfed_ante_name:
            stack = random.randrange(STACK_MIN_SIZE, ANTE)
        elif name == nerfed_blind_name:
            stack = random.randrange(STACK_MIN_SIZE, BIG_BLIND)
        else:
            stack = random.randint(STACK_MIN_SIZE, STACK_MAX_SIZE)
        players.append(pk.Player(name, stack))

    return players


def figure_out_hand(cards: list[pk.Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return pk.Hand(cards)
    
    possible_hands = [pk.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)


def ante_round(table: pk.Table):

    print(f'\n============ PLACING ANTES ============\n')

    print(f'Ante size: {ANTE}')
    for player in table.players:
        amount = ANTE if player.stack > ANTE else player.stack
        player.decrease_stack(amount)
        player.increase_bet_level(amount)

    pk.engines.gather_pot(table)
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

        if not small_blind_player.stack:
            print(f"{small_blind_player.name} IS ALL-IN, CANNOT PLACE SMALL BLIND\n")
        if small_blind_player.stack:
            amount = SMALL_BLIND if small_blind_player.stack > SMALL_BLIND else small_blind_player.stack
            small_blind_player.decrease_stack(amount)
            small_blind_player.increase_bet_level(amount)
            print(
                f"{small_blind_player.name} PLACES SMALL BLIND {amount} "
                f"({small_blind_player.name}'s bet level: {small_blind_player.bet_level} | stack: {small_blind_player.stack})"
                "\n"
            )

        # Place big blind

        big_blind_player = table.players[1]

        if not big_blind_player.stack:
            print(f"{big_blind_player.name} IS ALL-IN, CANNOT PLACE BIG BLIND\n")
        else:
            amount = BIG_BLIND if big_blind_player.stack > BIG_BLIND else big_blind_player.stack
            big_blind_player.decrease_stack(amount)
            big_blind_player.increase_bet_level(amount)
            print(
                f"{big_blind_player.name} PLACES BIG BLIND {amount} "
                f"({big_blind_player.name}'s bet level: {big_blind_player.bet_level} | stack: {big_blind_player.stack})\n"
            )

        table.set_bet_level(BIG_BLIND)
        table.set_full_bet_level(BIG_BLIND)
        print(f'TABLE CURRENT LEVEL: {table.bet_level}\n')

        # Place random big blinds (players who want to enter before waiting for their turn to place the big blind)

        for player in table.players[2:]:

            if player.stack and not random.randint(0, 3):
                amount = BIG_BLIND if player.stack > BIG_BLIND else player.stack
                player.decrease_stack(amount)
                player.increase_bet_level(amount)
                print(
                    f"{player.name} PLACES BIG BLIND {amount} TO ENTER THE GAME WITHOUT WAITING "
                    f"({player.name}'s bet level: {player.bet_level} | stack: {player.stack})"
                )
                print(f'TABLE CURRENT LEVEL: {table.bet_level}\n')

        # Deal pre-flop

        betting_round.deal_cards_to_players(2)
        print()

        # Let players to play

        for player in betting_round.listen():

            amount_to_full_call = table.bet_level - player.bet_level
            if amount_to_full_call == 0:
                print(f'To full bet: {betting_round.table.min_bet} | bet level: {player.bet_level}')
            else:
                print(f'To full call: {amount_to_full_call} | to full raise: {betting_round.table.full_bet_level + betting_round.table.min_raise_increase} | bet level: {player.bet_level}')

            range_by_action = betting_round.get_action_ranges()
            action_name, amount_range = random.choice([
                (name, amount_range) for name, amount_range in range_by_action.items() if amount_range is not None
            ])
            if action_name == pk.ACTION_BET:
                action_amount = random.randint(table.pot//2, table.pot*2)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            elif action_name == pk.ACTION_RAISE:
                amount_to_call = range_by_action[pk.ACTION_CALL][0]
                smallest_amount = amount_to_call + betting_round.table.min_raise_increase
                action_amount = random.randint(smallest_amount, smallest_amount*3)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            else:
                action_amount = amount_range[0]
            player.request_action(pk.Action(category=action_name, amount=action_amount))

    display_cards_and_money(table)
    print(f'\n============ ENDING {PREFLOP.upper()} ============\n')


def postflop(table: pk.Table, betting_round_name: str, open_fold_allowed: bool):

    # Break before starting if only remains one player
    if len(table.live_players) == 1:
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

            amount_to_full_call = table.bet_level - player.bet_level
            if amount_to_full_call == 0:
                print(f'To full bet: {betting_round.table.min_bet} | bet level: {player.bet_level}')
            else:
                print(f'To full call: {amount_to_full_call} | to full raise: {betting_round.table.full_bet_level + betting_round.table.min_raise_increase} | bet level: {player.bet_level}')

            range_by_action = betting_round.get_action_ranges()
            action_name, amount_range = random.choice([
                (name, amount_range) for name, amount_range in range_by_action.items() if amount_range is not None
            ])
            if action_name == pk.ACTION_BET:
                action_amount = random.randint(table.pot//2, table.pot*2)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            elif action_name == pk.ACTION_RAISE:
                amount_to_call = range_by_action[pk.ACTION_CALL][0]
                smallest_amount = amount_to_call + betting_round.table.min_raise_increase
                action_amount = random.randint(smallest_amount, smallest_amount*3)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            else:
                action_amount = amount_range[0]
            player.request_action(pk.Action(category=action_name, amount=action_amount))


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

    if len(table.live_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')
        pk.showdown(table)
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        pk.showdown(table)


def game():

    # Cycle not allowing open fold
    table = pk.Table(build_players())
    pk.reset_cycle_states(table)
    cycle(table)
    input('\n\n--- ENTER ---\n')

    # Cycle allowing open fold
    table = pk.Table(build_players())
    pk.reset_cycle_states(table)
    cycle(table, open_fold_allowed=True)
    input('\n\n--- ENTER ---\n')


def main():
    game()


if __name__ == '__main__':
    main()