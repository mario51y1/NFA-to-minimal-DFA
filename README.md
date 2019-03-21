# NFA-to-minimal-DFA
Step-by-step conversion from NFA to DFA

Optional project done for an university subject, in order to practice about conversion from NFA to minimal DFA. 
This application provides a step by step transformation.

To begin, edit file.txt in order to tell the program about the automaton.

1-. Q = ... are the states

2-. A = ... is the alphabet (empty tag is reserved to empty transitions)

3-. Initial = ... sets the initial state

4-. Final = ... sets the final state

Next lines are the transitions between states written in the syntax:

SI ; a1 a2 ... = SF

Where 
- SI is the initial state
- a1 a1 ... stands for the elements of the alphabet which you use for the transition
- SF is the final state
