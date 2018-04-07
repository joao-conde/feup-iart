% Cost of diagram is the amount of water transferred

initial_state(b(0,0)). % Initial state
final_state(b(2,0)). % Final state (assumed the right bucket has 0 liters)

% Transitions
successor(b(X,Y), b(4,Y), Cost) :-
    X<4, Cost is 4-X.

successor(b(X,Y), b(X,3), Cost) :- 
    Y<3, Cost is 3-Y.

successor(b(X,Y), b(0,Y), Cost) :-
    X>0, Cost is 0.

successor(b(X,Y), b(X,0), Cost) :-
    Y>0, Cost is 0.

successor(b(X,Y), b(4,Y1), Cost) :-
    X+Y>=4, X<4, Y1 is Y-(4-X), Cost is 4-X.

successor(b(X,Y), b(X1,3)) :-
	X+Y>=3, Y<3, X1 is X-(3-Y), Cost is 3-Y.

successor(b(X,Y), b(X1,0)) :-
    X+Y<4, Y>0, X1 is X+Y, Cost is 0.

successor(b(X,Y), b(0,Y1)) :-
	X+Y<3, X>0, Y1 is X+Y, Cost is 0.

% Heuristic function, which must be optimistic (A* will find the most optimal solution).
% Minimal value doesn't overestimates either, but h(x) must be as close to the real value as possible.
heuristic(b(X,Y), H) :-
    final_state(b(Xf, Yf)),
    H is max(abs(X-Xf), abs(Y-Yf)).

% A*: f(x) = g(x) + h(x)
% Tuple represented by (Value of f(x), Value of g(x), Node) so findall sorts by f(x)
astar([(_, _, [E|Road])|_], [E|Road]) :- 
    final_state(E).

astar([(_, G, [E|Road])|T], S) :-
    findall((F2, G2, [E2|[E|Road]]), (successor(E, E2, C), h(E2, H2),
    G2 is G+C, F2 is G2+H2), LS),

    append(R, LS, L2), sort(L2, L2_Ordered), astar(L2_Ordered, S).

solve_astar(S) :-
    initial_state(Ei), h(Ei, H), 
    astar([(H, 0, [Ei])], S).


