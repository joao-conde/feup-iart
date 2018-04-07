% Game has a minimum of 4 turns and a maximum of 10 turns.
final_state((0, max), 1).
final_state((0, min), 0).

successor((N, max), max, (N1, min)).

% Current state, max, value of play, next play.
minimax(State, max, Value, Play) :-

    % First expand current node with transition function, get successor list.
    findall(S2, successor(State, max, S2), SL),

    % Find the state with highest value from the successor list.
    max_value(SL, Value, Play).

max_value([State], Value, State) :-
    minimax(State, min, Value, _). % Find the value of the current state.

max_value([State|T], Value, BestState) :-
    minimax(State, min, ThisValue, _), % Find the value of the current state.
    max_value(T, Value2, BestState2),

    (ThisValue > Value2, !, Value = ThisValue, BestState = State; 
    Value = Value2, BestState = BestState2).


minimax(State, min, Value, Play) :-
    findall(S2, successor(State, min, S2), SL),
    min_value(SL, Value, Play).

min_value([State], Value, State) :-
    minimax(State, max, Value, _). % Find the value of the current state.

max_value([State|T], Value, BestState) :-
    minimax(State, max, ThisValue, _), % Find the value of the current state.
    min_value(T, Value2, BestState2),

    (ThisValue < Value2, !, Value = ThisValue, BestState = State; 
    Value = Value2, BestState = BestState2).


    