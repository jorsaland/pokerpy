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
- All version features are implemented.

## Upcoming versions

- **1.0 - stable:** The first stable release. API classes will wrap the core classes, as a separate layer in charge of input validations. Besides this, no new features are planned for this release, though some adjustments or enhancements may arise from final testing and feedback. Also, a full documentation will be provided.