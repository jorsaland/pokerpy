# PokerPy 0.8-stage-A - beta (under development)

Development for this version is divided into two stages (A and B).

Development for this version is divided into two stages (A and B).

- Stage A replaces the players yielded by betting rounds with state objects. Each state contains all the information needed to respond to it, such as the available actions and amount ranges, and also provide a method to respond. Likewise, `HandCycle` no longer picks cards itself with `secrets.choice`: it yields a state object and leaves the card choice to the developer using the library. The final usage documentation will recommend `secrets.SystemRandom().sample` for this.

- Stage B will add a context manager that runs a full No Limit Texas Hold'em cash game, handling everything that occurs between hand cycles, such as button movement, players entering and leaving the table, and proper heads-up play.


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

import json
import secrets
from typing import Any


# Implement server

def send_action_await_to_client(await_state: dict[str, Any]):

    print(f"\n>>> Sending await state to client's device...")
    print(f"{json.dumps(await_state)[:80]} ...")

    print("<<< Receiving request from client's device...")
    print("PLAYER CHOSE TO CHECK\n")

    return pk.Action(pk.ACTION_CHECK)


def send_blind_await_to_client(await_state: dict[str, Any]):

    print(f"\n>>> Sending await state to client's device...")
    print(json.dumps(await_state))

    print("<<< Receiving request from client's device...")
    print("PLAYER CHOSE TO PLACE OPTIONAL BLIND\n")

    return True


# Instantiate players and table once

players = [
    pk.Player('Andy', stack=1000),
    pk.Player('Boa', stack=1000),
    pk.Player('Coral', stack=1000),
    pk.Player('Dino', stack=1000),
]

table = pk.Table(players)

table.set_ante(1)
table.set_big_blind(10)

table.set_button_player(players[0])
table.set_big_blind_player(players[1])


# Run Texas Hold'em hand

with pk.HandCycle('hand 1', table=table, open_fold_allowed=True) as hand_cycle:

    for await_state in hand_cycle.listen():

        if isinstance(await_state, (pk.PlayerDealingAwait, pk.CommonDealingAwait)):
            cards = secrets.SystemRandom().sample(await_state.deck, await_state.count)
            await_state.deal_cards(cards)

        elif isinstance(await_state, pk.PlayerBlindAwait):
            place_blind = send_blind_await_to_client(await_state.to_dict())
            if place_blind:
                await_state.place_blind()

        elif isinstance(await_state, pk.PlayerActionAwait):
            action = send_action_await_to_client(await_state.to_dict())
            await_state.request_action(action)

        else:
            raise TypeError(f'unexpected type {type(await_state)}')


# Results

for player in players:
    print(f"{player.name}'s stack {player.stack}")
```

## Current version

### 0.8.0 (stage A)
- Detached from tag *0.7.1*.
- Engines mark themselves as completed at the end of the `run_listener` function, independently of the `close` method.
- Engines do not yield players anymore, but state objects that contain all the information needed and a method to respond.
- Hand cycle no longer picks cards itself with `secrets.choice`, but yields a state object instead, leaving the card choice to the developer (Demo 0.8-A uses `secrets.SystemRandom().sample` for this)

## Upcoming versions

- **0.9 - beta:** Will introduce the API layer between the core logic and the public classes. This layer will handle JSON serialization and deserialization of awaiting-action states and of a new history object, which records the game so far and can replay it from the start up to the exact point at which the history was generated. Histories will record every dealt card and every action, so replays will be exact. The API layer will also support a configurable smallest chip size by converting every amount, in both directions, between the smallest chip size and the core's internal unit, where the smallest chip is always 1. Amounts that are not multiples of the smallest chip will be rejected.

- **1.0 - stable:** The first stable release. The API layer will be finalized as the only public interface, wrapping the core classes. Type validation will move from the core classes to the API layer, so the core will assume its input has the expected types, while rule validation (whether an action or card is legal in the current state) will remain in the core. Core errors will be translated into documented public exceptions. The public interface will be frozen. No new features are planned; adjustments based on final testing and feedback may still occur. Full documentation of every API class will also be provided online.