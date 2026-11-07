# Version history 0.x

### 0.8

Adds a context manager that runs a full No Limit Hold'em cash game, including button movement, players entering and leaving, and heads-up play. Generators now yield state objects instead of players, and `HandCycle` leaves card choice to the developer.

### 0.7

Adds a context manager for a full Texas Hold'em hand cycle (betting rounds plus showdown), introducing the first demos of button rotation. Betting rounds no longer take minimum bet, starting player, or stopping player as input; those are set through `Table` methods. Players cannot enter or leave the table.

### 0.6

Reverts the smallest chip feature, to be reintroduced in a later version. Stack sizes are now finite, and responsibilities between structure and engine classes are well defined: structures like `Player` and `Table` only hold state and provide methods to update it, while engines like `BettingRound` hold no state and use those methods to drive the game.

### 0.5

Adds blind bets and a configurable minimum bet and a minimum raise equal to the previous bet or raise amount.

### 0.4

Adds basic money logic, including a smallest chip value and validation of action amounts. The minimum bet or raise is the smallest chip, and stacks are infinite, so all-ins and side pots are impossible.

### 0.3

Adds cards and hands, and winners are chosen by best hand.

### 0.2

Betting rounds now last until the last aggressive action is responded.

### 0.1

Adds action constraints in betting rounds, including players leaving by folding. The `BettingRound` context manager is implemented with a core design decision: the game flow is driven by Python generators, which yield control to a player whenever an action is required and resume once it is received. Rounds end once every player has acted once, even if someone was aggressive.

### 0.0

Adds base sketch `Player` and `Table` classes that only print messages. There is no money and no real logic. Every player acts once per betting round, and the winner is chosen randomly. A very basic hand cycle demo is introduced, to be enriched in later versions.
