% 7.1

% a)

:- op(800, xfy, e).
:- op(950, xfx, entao).
:- op(850, fx, se).
:- op(750, xfx, com).

% R1
se motor=nao e bateria=ma entao problema=bateria com fc=1.
% R2
se luz=fraca entao bateria=ma com fc=0.8.
% R3
se radio=fraco entao bateria=ma com fc=0.8.
% R4
se luz=boa e radio=bom entao bateria=boa com fc=0.8.
% R5
se motor=sim e cheiro_gas=sim entao problema=encharcado com fc=0.8.
% R6
se motor=nao e bateria=boa e indicador_gas=vazio entao problema=sem_gasolina com fc=0.9.
% R7
se motor=nao e bateria=boa e indicador_gas=baixo entao problema=sem_gasolina com fc=0.3.
% R8
se motor=nao e cheiro_gas=nao e ruido_motor=nao_ritmado e bateria=boa entao problema=motor_gripado com fc=0.7.
% R9
se motor=nao e cheiro_gas=nao e bateria=boa entao problema=carburador_entupido com fc=0.9.
% R10
se motor=nao e bateria=boa entao problema=velas_estragadas com fc=0.8.

% b)

:- dynamic(facto/3).
% facto(A, V, FC).

% c)

questionavel(motor, 'O motor funciona?', [sim,nao]).
questionavel(luz, 'Como estao as luzes?', [fraca,razoavel,boa]).
questionavel(radio, 'Como esta o radio?', [fraco,razoavel,bom]).
questionavel(cheiro_gas, 'Sente cheiro a gasolina?', [sim,nao]).
questionavel(indicador_gas, 'Como esta o indicador de gasolina?', [vazio,baixo,meio,cheio]).
questionavel(ruido_motor, 'Que ruido faz o motor?', [ritmado,nao_ritmado]).


verifica(A, V, FC):-
    facto(A, V, FC), !.


verifica(A, V, _):-
    facto(A, V2, _),
    V2 \= V, !, fail.


verifica(A, V, FC):-
    questionavel(A, Perg, LR),
    repeat,
    write(Perg:LR), read(Resp),
    member(Resp, LR),
    write("Certeza[0-1]?"), read(FC),
    assert(facto(A, Resp, FC)),
    !, V=Resp.

verifica(A, V, FC):-
    deduz(A, V, FC).


deduz(A, V, _):-
    se Perms entao A=V com fc=FCRegra,
    prova(Perms, FCPerms),
    FCNovo is FCPerms * FCRegra,
    actualiza(A, V, FCNovo),
    fail.

deduz(A, V, FC):-
    facto(A, V, FC).



prova(A=V, FC):-
    verifica(A, V, FC).

prova(A=V e Ps, FC):-
    verifica(A, V ,FC1),
    prova(Ps, FC2),
    FC is min(FC1, FC2).



actualiza(A, V, FC):-
    (facto(A, V, FCVelho),
    FCNovo is FC + FCVelho*(1-FC),
    retract(facto(A, V, FCVelho)) ; FCNovo is FC),
    assert(facto(A, V, FCNovo)).


go:-
    retractall(facto(_, _, _)),
    verifica(problema, V, FC),
    write(problema=V:FC).
