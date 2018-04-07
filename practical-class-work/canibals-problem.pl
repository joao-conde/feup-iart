% 2.2

initial_state(state(3,3,1)). % Initial state
final_state(state(0,0,0)). % Final state

% State transitions
successor(state(NM,NC,1), NewState)