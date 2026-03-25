# PokerPy 0.6 - alpha (under development)
Money logic is improved with the introduction of stack sizes and all-in scenarios. The communication model between betting round, table and player instances is simplified by exchanging some responsibilities between them. Once the communication model is stable, the logic to handle side pots will be coded.

## License

PokerPy is licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
See the [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.txt`](NOTICE.txt) files for details.

## Disclaimer

This package is a general-purpose game logic tool intended for lawful use only. The author and the contributors make no representation about the legality of online poker or gambling in any given jurisdiction. You are solely responsible for ensuring that your use of this package complies with all applicable laws and regulations. The author and the contributors assume no liability whatsoever for how this software is used.

## Current version

### 0.6.0
- Detached from tag *0.5.0*.
- Under development...

## Upcoming versions

- **0.7 - alpha:** A context manager will be implemented to run a full hand cycle, composed of multiple betting rounds and the showdow. The hand cycle will include a feature to report what actions are available for the current player, before actually having to parse the action.
- **0.8 - beta:** A context manager will be implemented to run a full No Limit Texas Hold'em cash game. This manager will implement the features that occur between hand cycles, such as button movement, players entering and leaving the table, and proper handling of heads-up situations. Also, a basic documentation will be provided to illustrate how to use the high level features.
- **1.0 - stable:** The first stable release. No new features are planned for this release, though some adjustments or enhancements may arise from final testing and feedback. Some important refactors may occur in internal code, however. Also, a full documentation will be provided along with some usage demos.