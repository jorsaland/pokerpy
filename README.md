# PokerPy 0.7 - alpha (under development)

A new context manager is implemented to run a full hand cycle, composed of multiple betting rounds and the showdow with the structure of a Texas Hold'em game. This will feed the version demos which for the first time will attempt to simulate the button rotation logic. This is expected to be the last alpha version.


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
    # Send to client player and options
    print(f'{player.name = }')
    print(f'{available_actions = }\n')
    # Receive from client the requested action
    action_name = random.choice(list(available_actions.keys()))
    amount = random.choice(available_actions[action_name])
    return pk.Action(action_name, amount)

# Instantiate players once
players = [
    pk.Player('Andy', stack=1000),
    pk.Player('Boa', stack=1000),
    pk.Player('Coral', stack=1000),
    pk.Player('Dino', stack=1000),
]

# Instantiate table
table = pk.Table(players)

# Run betting round
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

### 0.7.0
- Detached from tag *0.6.0*.
- All version features are implemented.

## Upcoming versions

- **0.8 - beta:** A context manager will be implemented to run a full No Limit Texas Hold'em cash game. This manager will implement the features that occur between hand cycles, such as button movement, players entering and leaving the table, and proper handling of heads-up situations. Also, a basic documentation will be provided to illustrate how to use the high level features.
- **1.0 - stable:** The first stable release. API classes will wrap the core classes, as a separate layer in charge of input validations. Besides this, no new features are planned for this release, though some adjustments or enhancements may arise from final testing and feedback. Also, a full documentation will be provided.