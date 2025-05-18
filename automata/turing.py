from automata.basicautomaton import BasicAutomaton
from automata.checks.typecheck import assert_dictionary_types, TM_TYPES
from automata.checks.valuecheck import TM_VALIDATORS
from collections import defaultdict
from typing import override

class TM(BasicAutomaton):

    # Validates the TM
    # Implements an abstract method from BasicAutomaton
    @override
    def validate_automata(self) -> None:
        # Perform a type check first
        assert_dictionary_types(self.data, TM_TYPES)
        # Then perform a list of value-checking functions
        for check in TM_VALIDATORS:
            check(self.data)
        

    # Puts the TM in its starting state, resetting the tape
    # Implements an abstract method from BasicAutomaton
    @override
    def starting_state(self) -> None:
        # Default tape symbol is a BLANK
        self.tape = defaultdict(lambda: self.data["blank"])
        # Start at the leftmost end of the tape
        self.tape_pointer = 0
        # Start in the initial state
        self.state = self.data["initial"]
        # The machine isn't halted at first
        self.halted = False
        # Strictness = whether we halt when the tape pointer goes to -1
        # By definition, it should be True, but if it's False the resulting
        # model is still equivalent to a TM, except it's easier to program
        self.strict = False


    # Returns True if the automata is in an accepting state
    # Implements an abstract method from BasicAutomaton
    @override
    def accepting(self) -> bool:
        # A Turing machine accepts if it halts in an accepting state
        return self.halted and self.state in self.data["accepting"]
    

    # Changes the states of the automata based on the input and tape
    # Implements an abstract method from BasicAutomaton
    @override
    def action(self, symbol: str) -> None:
        # A halted machine doesn't do anything
        if self.halted:
            return
        
        # Get the current tape symbol
        tape_symbol = self.tape[self.tape_pointer]

        # Check each rule for the current input symbol
        for rule in self.data["ruleset"][symbol]:
            # If any rule matches both the current state and the current tape symbol, we use it
            if rule["from"]["state"] == self.state and rule["from"]["tape"] == tape_symbol:
                # Set the new state
                self.state = rule["to"]["state"]
                # Set the new tape symbol
                self.tape[self.tape_pointer] = rule["to"]["tape"]

                # Move the tape pointer
                # Check against the increment symbol
                if rule["shift"] == self.data["increment"]:
                    self.tape_pointer += 1
                # Check against the decrement symbol
                elif rule["shift"] == self.data["decrement"]:
                    self.tape_pointer -= 1

                # Halt when going out-of-bounds
                if self.strict and self.tape_pointer < 0:
                    self.halted = True

                # No point in searching further
                return
        
        # If we didn't find any rule match, halt
        self.halted = True
    

    # Returns the current tape between two values
    def get_tape(self, front: int, back: int) -> list[str]:
        return [self.tape[position] for position in range(front, back + 1)]


    # Gives the Turing machine a new tape and optionally sets the head's position
    def set_tape(self, tape: list[str], position: int = 0) -> None:
        # Check the input first
        for symbol in tape:
            # If any of the symbols we try to set aren't recognized, throw an exception
            if symbol not in self.data["tape_symbols"]:
                raise ValueError(f"Symbol {symbol} was given to be placed on the tape but is not recognized")
            
        # Clear the old tape
        self.tape = defaultdict(lambda: self.data["blank"])

        # Write the new tape contents
        for pointer, value in enumerate(tape):
            self.tape[pointer] = value

        # Set the head's new position
        self.tape_pointer = position

    
    # Enables the out-of-bounds check for the tape pointer
    def enable_strict(self) -> None:
        self.strict = True
