# PokerPy 0.6-stage-A - alpha (under development)

Development for this version is divided into two stages (A and B).

- Stage A focuses on two main improvements. First, the money logic is enhanced through the introduction of stack sizes, which are tested exclusively in scenarios where all players start with equal stacks. Second, the communication model between instances is redesigned, leading to a cleaner and more solid architecture with clearer responsibilities: Table and Player instances are responsible for holding the game state and exposing simple methods to update it, while BettingRound instances hold no game state; instead, they implement the core game control logic by consuming Table and Player methods.

- Stage B will introduce support for side pots and variable stack sizes. At this point, the BettingRound class logic will be complete and fully usable, though full game logic will have to wait. A basic documentation on the fully powered BettingRound class will also be included.


## License

PokerPy is licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
See the [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.txt`](NOTICE.txt) files for details.

## Disclaimer

This package is a general-purpose game logic tool intended for lawful use only. The author and the contributors make no representation about the legality of online poker or gambling in any given jurisdiction. You are solely responsible for ensuring that your use of this package complies with all applicable laws and regulations. The author and the contributors assume no liability whatsoever for how this software is used.

## Communication model

A diagram representing the communication between instances is available. See [`MODEL.md`](MODEL.md) for details.

## Current version

### 0.6.0 (stage A)
- Detached from tag *0.5.0*.
- Stage A features and refactors are implemented.

## Upcoming versions

- **0.7 - alpha:** A context manager will be implemented to run a full hand cycle, composed of multiple betting rounds and the showdow. The hand cycle will include a feature to report what actions are available for the current player, before actually having to parse the action.
- **0.8 - beta:** A context manager will be implemented to run a full No Limit Texas Hold'em cash game. This manager will implement the features that occur between hand cycles, such as button movement, players entering and leaving the table, and proper handling of heads-up situations. Also, a basic documentation will be provided to illustrate how to use the high level features.
- **1.0 - stable:** The first stable release. No new features are planned for this release, though some adjustments or enhancements may arise from final testing and feedback. Some important refactors may occur in internal code, however. Also, a full documentation will be provided along with some usage demos.