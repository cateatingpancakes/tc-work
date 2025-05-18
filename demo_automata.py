from automata.dfa import DFA
from automata.nfa import NFA
from copy import deepcopy

# Get the Python file's path in order to address relative to it
PATH = __file__.strip().rsplit("/", maxsplit=1)[0] + "/"

# Some tests for the automata
TESTS = [
    map(str, [0, 1, 0, 0, 1, 0, 1, 1, 0, 1]),
    map(str, [1, 0, 0, 1, 0, 0, 1, 0, 1, 1]),
    map(str, [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]),
    map(str, [0, 0, 1, 1, 0, 0, 1, 1, 1, 0]),
    map(str, [0, 1, 1, 0, 1, 0, 0, 0, 0, 0])
]

# Create a DFA and a NFA
dfa = DFA(PATH + "tests/dfa/dfa_example.json")
nfa = NFA(PATH + "tests/nfa/nfa_example.json")

# Now we will test both automata
# Note that due to how Python effectively has call-by-sharing
# for non-primitive argument types, the tests will be mangled by
# action_sequence calls, i.e. they need to be copied beforehand,
# if reusing them is needed; this is why we must (deep)copy here

print("DFA tests:")
for test in deepcopy(TESTS):
    dfa.starting_state()
    result = dfa.action_sequence(test)
    print(f"Final state: {dfa.state}, accepting: {result}")

print("NFA tests:")
for test in deepcopy(TESTS):
    nfa.starting_state()
    result = nfa.action_sequence(test)
    print(f"Final state: {nfa.state}, accepting: {result}")