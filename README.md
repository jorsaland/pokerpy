# PokerPy 0.8 - beta (under development)

Added a context manager that runs a full No Limit Texas Hold'em cash game, handling everything that occurs between hand cycles, such as button movement, players entering and leaving the table, and proper heads-up play. The engine generators no longer yield players. Instead, they yield a state object containing all the information needed to choose an action. Likewise, `HandCycle` no longer picks cards itself with `secrets.choice`. It now yields a state object and leaves the card choice to the developer using the library, although `secrets.choice` will be suggested in the final usage documentation.

## License

PokerPy is licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
See the [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.txt`](NOTICE.txt) files for details.

## Disclaimer

This package is a general-purpose game logic tool intended for lawful use only. The author and the contributors make no representation about the legality of online poker or gambling in any given jurisdiction. You are solely responsible for ensuring that your use of this package complies with all applicable laws and regulations. The author and the contributors assume no liability whatsoever for how this software is used.

## Model

A brief documentation is provided on structures and engines. Also, a diagram representing the communication between instances is available. See [`MODEL.md`](MODEL.md) for details.

## Usage example

```python
import pokerpy as pk
import random


# Implement server

def await_client_device(player: pk.Player, available_actions: dict[str, range]):

    # Send current player and options to the client's device
    print(f'{player.name = }')
    print(f'{available_actions = }\n')

    # Receive the requested action from client's device
    action_name = random.choice(list(available_actions.keys()))
    amount = random.choice(available_actions[action_name])
    return pk.Action(action_name, amount)


# Instantiate players and table once

players = [
    pk.Player('Andy', stack=1000),
    pk.Player('Boa', stack=1000),
    pk.Player('Coral', stack=1000),
    pk.Player('Dino', stack=1000),
]

table = pk.Table(players)


# Run Texas Hold'em hand

with pk.HandCycle('hand 1', table=table) as hand_cycle:
    for player in hand_cycle.listen():
        action_ranges = hand_cycle.betting_round.get_action_ranges()
        action = await_client_device(player, action_ranges)
        player.request_action(action)


# Or run a single betting round

with pk.BettingRound('flop', table=table) as betting_round:
    for player in betting_round.listen():
        action = await_client_device(player, betting_round.get_action_ranges())
        player.request_action(action)


# Results

print(f'POT: {table.pot}')
for player in players:
    print(f"{player.name}'s stack {player.stack}")
```

## Current version

### 0.8.0
- Detached from tag *0.7.1*.
- Engines mark themselves as completed at the end of the `run_listener` function, independently of the `close` method.

## Upcoming versions

- **0.9 - beta:** Will introduce the API layer between the core logic and the public classes. This layer will handle JSON serialization and deserialization of awaiting-action states and of a new history object, which records the game so far and can replay it from the start up to the exact point at which the history was generated. Histories will record every dealt card and every action, so replays will be exact. The API layer will also support a configurable smallest chip size by converting every amount, in both directions, between the smallest chip size and the core's internal unit, where the smallest chip is always 1. Amounts that are not multiples of the smallest chip will be rejected.

- **1.0 - stable:** The first stable release. The API layer will be finalized as the only public interface, wrapping the core classes. Type validation will move from the core classes to the API layer, so the core will assume its input has the expected types, while rule validation (whether an action or card is legal in the current state) will remain in the core. Core errors will be translated into documented public exceptions. The public interface will be frozen. No new features are planned; adjustments based on final testing and feedback may still occur. Full documentation of every API class will also be provided online.