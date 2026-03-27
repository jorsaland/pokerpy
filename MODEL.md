# Communication model

```mermaid
flowchart LR

    %% Classes and methods

    C(Controller)@{ shape: cloud }

    P(Player)@{ shape: circle }
    P.request_action(request_action)@{ shape: text }
    P.reset_action(reset_action)@{ shape: text }
    P.deal_card(deal_card)@{ shape: text }
    P.add_to_current_amount(add_to_current_amount)@{ shape: text }
    P.remove_from_stack(remove_from_stack)@{ shape: text }
    P.fold(fold)@{ shape: text }
    P.reset_betting_round_states(reset_betting_round_states)@{ shape: text }
    P.assign_hand(assign_hand)@{ shape: text }
    P.add_to_stack(add_to_stack)@{ shape: text }
    P.reset_cycle_states(reset_cycle_states)@{ shape: text }

    T(Table)@{ shape: circle }
    T.remove_card_from_deck(remove_card_from_deck)@{ shape: text }
    T.deal_common_card(deal_common_card)@{ shape: text }
    T.add_to_current_amount(add_to_current_amount)@{ shape: text }
    T.add_to_central_pot(add_to_central_pot)@{ shape: text }
    T.get_previous_player(get_previous_player)@{ shape: text }
    T.get_next_player(get_next_player)@{ shape: text }
    T.iter_players(iter_players)@{ shape: text }
    T.get_previous_active_player(get_previous_active_player)@{ shape: text }
    T.reset_betting_round_states(reset_betting_round_states)@{ shape: text }

    BR(BettingRound)@{ shape: circle }
    BR.listen(listen)@{ shape: text }
    BR.close(listen)@{ shape: text }
    BR.increase_counter(increase_counter)@{ shape: text }
    BR.set_stopping_player(set_stopping_player)@{ shape: text }
    BR.overwrite_smallest_raise_amount(overwrite_smallest_raise_amount)@{ shape: text }
    BR.deal_cards_to_players(deal_cards_to_players)@{ shape: text }
    BR.deal_common_cards(deal_common_cards)@{ shape: text }

    HC(HandCycle)@{ shape: circle }

    %% Class-method relations

    P.request_action --> P
    P.reset_action --> P
    P.deal_card --> P
    P.add_to_current_amount --> P
    P.remove_from_stack --> P
    P.fold --> P
    P.reset_betting_round_states --> P
    P.assign_hand --> P
    P.add_to_stack --> P
    P.reset_cycle_states --> P

    T.remove_card_from_deck --> T
    T.deal_common_card --> T
    T.add_to_current_amount --> T
    T.add_to_central_pot --> T
    T.get_previous_player --> T
    T.get_next_player --> T
    T.iter_players --> T
    T.get_previous_active_player --> T
    T.reset_betting_round_states --> T

    BR.listen --> BR
    BR.close --> BR
    BR.increase_counter --> BR
    BR.set_stopping_player --> BR
    BR.overwrite_smallest_raise_amount --> BR
    BR.deal_cards_to_players --> BR
    BR.deal_common_cards --> BR

    %% Method access relations

    C -----> P.request_action
    C -----> P.reset_action

    BR ----> P.reset_action
    BR ----> P.deal_card
    BR ----> P.add_to_current_amount
    BR ----> P.remove_from_stack
    BR ----> P.fold
    BR ----> P.reset_betting_round_states

    BR ----> T.remove_card_from_deck
    BR ----> T.deal_common_card
    BR ----> T.add_to_current_amount
    BR ----> T.add_to_central_pot
    BR ----> T.get_previous_player
    BR ----> T.iter_players
    BR ----> T.get_previous_active_player
    BR ----> T.reset_betting_round_states

    HC ----> P.assign_hand
    HC ----> P.add_to_stack
    HC ----> P.reset_cycle_states

    HC ----> BR.listen
    HC ----> BR.close
    HC ----> BR.deal_cards_to_players
    HC ----> BR.deal_common_cards

    %% Helper method relations

    P.reset_cycle_states -.-> P.reset_betting_round_states

    T.iter_players -.-> T.get_previous_player
    T.iter_players -.-> T.get_next_player

    BR.listen -.-> BR.increase_counter
    BR.listen -.-> BR.set_stopping_player
    BR.listen -.-> BR.overwrite_smallest_raise_amount
```