# PokerPy 0.6-stage-B - alpha (under development)

Development for this version is divided into two stages (A and B).

- Stage A focuses on two main improvements. First, the money logic is enhanced through the introduction of stack sizes, which are tested exclusively in scenarios where all players start with equal stacks. Second, the communication model between instances is redesigned, leading to a cleaner and more solid architecture with clearer responsibilities: Table and Player instances are responsible for holding the game state and exposing simple methods to update it, while BettingRound instances hold no game state; instead, they implement the core game control logic by consuming Table and Player methods.

- Stage B introduces support for side pots and variable stack sizes. Validation functions are developed, replacing verbose and repetitive code. At this point, the BettingRound class logic will be complete and fully usable, though full game logic will have to wait. A basic documentation on the fully powered BettingRound class will also be included.


## License

PokerPy is licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
See the [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.txt`](NOTICE.txt) files for details.

## Disclaimer

This package is a general-purpose game logic tool intended for lawful use only. The author and the contributors make no representation about the legality of online poker or gambling in any given jurisdiction. You are solely responsible for ensuring that your use of this package complies with all applicable laws and regulations. The author and the contributors assume no liability whatsoever for how this software is used.

## Model

A brief documentation is provided on structures and engines. Also, a diagram representing the communication between instances is available. See [`MODEL.md`](MODEL.md) for details.

## Current version

### 0.6.0 (stage A)
- Detached from tag *0.5.0*.
- Stage A features and refactors are implemented.

### 0.6.0 (stage B)
- Detached from tag *0.6.0-stage-A*.
- Stage B features and refactors are implemented.

## Upcoming versions

- **0.7 - alpha:** A context manager will be implemented to run a full hand cycle, composed of multiple betting rounds and the showdow. It will include experimental features that have already been developed in the latest demos.
- **0.8 - beta:** A context manager will be implemented to run a full No Limit Texas Hold'em cash game. This manager will implement the features that occur between hand cycles, such as button movement, players entering and leaving the table, and proper handling of heads-up situations. Also, a basic documentation will be provided to illustrate how to use the high level features.
- **1.0 - stable:** The first stable release. API classes will wrap the core classes, as a separate layer in charge of input validations. Besides this, no new features are planned for this release, though some adjustments or enhancements may arise from final testing and feedback. Also, a full documentation will be provided.