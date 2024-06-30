# PokerPy under development! (Alpha)
Basic money logic is implemented, including a smallest chip value and validations on action amounts. By now, the smallest betting or raising amount is the smallest chip, no matter if there were previous aggressive actions. Stacks are infinite, making it impossible to go all-in and creating side pots.

### 0.4.0
- All features are developed to reach the goal.
- Started from version *0.3.1* and received feature updates from versions *0.0.1*, *0.1.3*, *0.2.2* and *0.3.2*, including unit tests, features and deprecations.

## Upcoming versions
- **0.5 (alpha):** Blind bet options will be added (including antes), as well as minimum betting and raising amounts.
- **0.6 (alpha):** Stacks will no longer be infinite. This implies all-in situations and side-pots will be possible.
- **0.7 (beta):** A basic No limit Texas hold'em framework will be available, making it possible to implement a full cash game. This will include logic regarding moving the button in different situations, such as players leaving or entering the table.
- **1.0 (stable):** This will be the first release. No new features are expected, but they might arise during the final evaluations and tests. 