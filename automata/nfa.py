from copy import deepcopy
from automata.basicautomaton import BasicAutomaton
from automata.checks.typecheck import assert_dictionary_types, NFA_TYPES
from automata.checks.valuecheck import NFA_VALIDATORS
from typing import override

class NFA(BasicAutomaton):

    # Preprocessing step, adds EPSILON symbol to the symbols list
    # Implements an abstract method from BasicAutomaton
    @override
    def preprocess(self) -> None:
        self.data["symbols"].append("EPSILON")


    # Validates the NFA
    # Implements an abstract method from BasicAutomaton
    @override
    def validate_automata(self) -> None:
        # Perform a type check first
        assert_dictionary_types(self.data, NFA_TYPES)
        # Then perform a list of value-checking functions
        for check in NFA_VALIDATORS:
            check(self.data)


    # Puts the NFA in its starting state
    # Implements an abstract method from BasicAutomaton
    @override
    def starting_state(self) -> None:
        # NFA state is represented as a list of simultaneous states
        # Start by initializing the states list with an empty list
        self.state = []
        # Then start filling it, by entering the starting state
        self.enter_state(self.data["initial"])


    # Helper method to move the automata into a state
    # Any EPSILON transitions will be resolved along the way
    def enter_state(self, new_state: str) -> None:
        # Add the new state, if not already in it from some other branch
        if new_state not in self.state:
            self.state.append(new_state)
        # Perform epsilon transitions, if the new state has them
        if "EPSILON" in self.data["ruleset"][new_state].keys():
            for other_state in self.data["ruleset"][new_state]["EPSILON"]:
                self.enter_state(other_state)


    # Returns True if the automata is in an accepting state
    # Implements an abstract method from BasicAutomaton
    @override
    def accepting(self) -> bool:
        # Go through every current state to find at least one that accepts
        for current_state in self.state:
            if current_state in self.data["accepting"]:
                return True
        # If no accepting state was found, the automaton is rejecting
        return False


    # Changes the states of the automata based on the input symbol
    # If no rule matches the states and the symbol, nothing happens
    # Implements an abstract method from BasicAutomaton
    @override
    def action(self, symbol: str) -> None:
        # Validate the symbol first
        if symbol not in self.data["symbols"]:
            raise ValueError(f"Symbol {symbol} not recognized")

        # We save the list of states that have to be parsed
        # A simple copy would work, but a deepcopy is safer, in case the 
        # states list will ever be made to contain non-primitive elements
        parse_list = deepcopy(self.state)
        
        # First, we remove all the states that will be abandoned
        # We can't remove them "as we go" as it might alter behavior
        for current_state in parse_list:
            # If there will be something to do in the current state
            if symbol in self.data["ruleset"][current_state].keys():
                # Then that state will be abandoned, so remove it
                self.state.remove(current_state)

        # Go through the state list and perform transitions
        # States that weren't abandoned will simply not change anything when parsed
        for current_state in parse_list:
            # If the transition function has an entry for (current_state, symbol) -> [new_states]
            if symbol in self.data["ruleset"][current_state].keys():
                # For every new state the automaton can transition into
                for new_state in self.data["ruleset"][current_state][symbol]:
                    # Enter the new state, resolving any EPSILON transitions
                    self.enter_state(new_state)
    
