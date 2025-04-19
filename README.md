# PokerPy under development! (Alpha)
Money logic is improved with the introduction of blind bets. The previous `last_aggressive_player` parameter has been replaced by `stopping_player`. The key difference is that in earlier versions, the last aggressive player ended the betting round BEFORE playing, whereas now the stopping player ends the round AFTER taking action. This change helps clarify who acts first after blinds are posted, while still supporting betting rounds without blinds (flop, turn and river). Additionally, this version introduces a configurable minimum bet amount, along with a minimum raise amount equal to the size of the previous bet or raise.

### 0.5.0
- All features are developed to reach the goal.
- Started from version *0.4.1*.

## Upcoming versions
- **0.6 (alpha):** Stack sizes will be finite for the first time. This change introduces support for all-in scenarios and the creation of side pots. At this point, users will be able to implement realistic betting rounds.
- **0.7 (beta):** A fully functional framework for No Limit Texas Hold'em cash games will be introduced. This includes game dynamics such as button movement logic, support for players entering and leaving the table, and proper handling of heads-up situations.
- **1.0 (stable):** The first stable release. No major features are planned beyond this point, though minor adjustments or enhancements may arise from final testing and feedback.