This repository contains all my lab work for the TC/LFA course at UB.
# How it works
The work is divided into three main parts: code for the first lab (which was unrelated to automata), a mini-library (or at least a collection of classes) that enable running automata with some examples stored as `.json` files, and a script that turns a description of a game into a DFA engine that runs it.
## The automata library
Currently supported automata are DFAs, NFAs and Turing machines. Class code may be found in `/automata`, a good part of which involves type- and value-checking that may be found in `/automata/checks`. To run an automaton, the bare minimum needed is a `.json` file in the appropriate format (samples may be found in `/tests`) and some code to construct the right kind of object from it. The automaton may then be run using the `action()` method. A DFA and/or NFA runner like so can be found in `demo_automata.py`, while `demo_turing.py` runs a Turing mahcine.
## DFA games
The `/gamedescribe` directory contains `.json` files that describe a room-based game with items and actions; a player might want to interact in a certain room, the outcome of this depending on the items they have, or a room might be entered only by players possessing a certain item (such as a key). `demo_game.py` loads a file in this format, constructs a DFA for this game, then feeds user input to this DFA, following a terminal prompt (telling the player what the DFA's state currently is).
## Matrices
The `/matrices` directory contains code (`matrix.py`) to load a matrix from a file in a comment-supporting format, an example of which may be found in `matrix.in`.
## Bonus
There's now a class for context-free grammars with a CYK algorithm implementation that decides whether a certain string is in the CFG. A demo may be found in `demo_cyk.py`.