# PokerPy under development! (Alpha)
Money logic is enhanced by adding blind bets. The parameter "last_aggressive_player" is replaced by "stopping_player". The key difference is that the last aggressive player from previous versions closed the betting round BEFORE taking action, whilst the stopping player introduced in this version closes the round AFTER taking action. This change is helpful to identify who has to act first after placing the blinds, while still considering that not every betting round has blinds. A configurable minimum betting amount is also introduced, as well as a minimum rising amount which is equal to the previous betting/rising amount.

### 0.5.0
- All features are developed to reach the goal.
- Started from version *0.4.1*.

## Upcoming versions
- **0.6 (alpha):** Stacks will no longer be infinite. This implies all-in situations and side-pots will be possible.
- **0.7 (beta):** A basic No limit Texas hold'em framework will be available, making it possible to implement a full cash game. This will include logic regarding moving the button in different situations, such as players leaving or entering the table.
- **1.0 (stable):** This will be the first release. No new features are expected, but they might arise during the final evaluations and tests. 