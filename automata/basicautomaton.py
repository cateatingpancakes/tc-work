import json
from abc import abstractmethod

# Base class for all automata
class BasicAutomaton:

    # Loads an automaton from a file
    def load_automata(self, filename: str) -> None:
        with open(filename, "r+") as file:
            self.data = json.load(file)
        
        # Do pre-validation processing
        self.preprocess()

        # Check if the data is valid
        self.validate_automata()

        # If it is, put the automaton in its starting state
        self.starting_state()


    # Saves an automaton to a file
    def save_automata(self, filename: str) -> None:
        if self.data is not None:
            with open(filename, "w+") as file:
                json.dump(self.data, file, indent=4)

    
    # Performs preprocessing actions immediately after loading, 
    # but before validating the automaton
    @abstractmethod
    def preprocess(self) -> None:
        pass


    # Check an automaton's validity
    @abstractmethod
    def validate_automata(self) -> bool:
        return True
            

    # Puts an automaton in its starting state
    @abstractmethod
    def starting_state(self) -> None:
        pass


    # Returns true if the automaton is in an accepting state
    @abstractmethod
    def accepting(self) -> bool:
        pass


    # Performs an action with the automaton when it receives a symbol
    @abstractmethod
    def action(self, symbol: str) -> bool:
        pass

    
    # Utility function, performs a sequence of actions
    # Returns the final state of the automaton (accepting or not)
    def action_sequence(self, symbols: list[str]) -> bool:
        # Perform the actions
        for symbol in symbols:
            self.action(symbol)

        # Check if the final state is accepting
        return self.accepting()


    # Automaton constructor, can load from a .json file
    def __init__(self, filename: str = None):
        # Load from a .json, if any was given
        if filename is not None:
            self.load_automata(filename)

    