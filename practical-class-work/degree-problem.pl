incompat(D1, D2, NA) :-
    disciplina(D1, LA1),
    disciplina(D2, LA2),
    findall(A, (member(A, LA1), member(A, LA2)), LA12),
    length(LA12, NA).