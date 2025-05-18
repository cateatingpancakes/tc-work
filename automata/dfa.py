from automata.basicautomaton import BasicAutomaton
from automata.checks.typecheck import assert_dictionary_types, DFA_TYPES
from automata.checks.valuecheck import DFA_VALIDATORS
from typing import override

class DFA(BasicAutomaton):

    # Validates the DFA
    # Implements an abstract method from BasicAutomaton
    @override
    def validate_automata(self) -> None:
        # Perform a type check first
        assert_dictionary_types(self.data, DFA_TYPES)
        # Then perform a list of value-checking functions
        for check in DFA_VALIDATORS:
            check(self.data)


    # Puts the DFA in its starting state
    # Implements an abstract method from BasicAutomaton
    @override
    def starting_state(self) -> None:
        self.state = self.data["initial"]
        

    # Returns True if the automata is in an accepting state
    # Implements an abstract method from BasicAutomaton
    @override
    def accepting(self) -> bool:
        return self.state in self.data["accepting"]
    

    # Changes the state of the automata based on the input symbol
    # If no rule matches the state and the symbol, nothing happens
    # Implements an abstract method from BasicAutomaton
    @override
    def action(self, symbol: str) -> None:
        # Validate the received symbol
        if symbol not in self.data["symbols"]:
            raise ValueError(f"Symbol {symbol} not recognized")

        # If the transition function has an entry for (self.state, symbol) -> new_state
        if symbol in self.data["ruleset"][self.state].keys():
            # Perform the state change
            self.state = self.data["ruleset"][self.state][symbol]
        
