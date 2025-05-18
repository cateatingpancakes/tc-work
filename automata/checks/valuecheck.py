# Asserts the validity of the initial state
# (i.e. found in the list of possible states)
def assert_initial(data: dict) -> None:
    if data["initial"] not in data["states"]:
            raise ValueError(f"Initial state {data["initial"]} is not in the state list")
    

# Asserts that every accepting state is valid
def assert_accepting(data: dict) -> None:
    for state in data["accepting"]:
        if state not in data["states"]:
            raise ValueError(f"Accepting state {state} is not in the state list")
    

# Asserts that all starting states in the transition function are valid
def assert_starting(data: dict) -> None:
    for state, _ in data["ruleset"].items():
        if state not in data["states"]:
            raise ValueError(f"A rule was given for {state}, which is not in the state list")


# Asserts that there is exactly one entry for the each symbol 
# in the transition from each state
def assert_unique(data: dict) -> None:
    for state, action in data["ruleset"].items():
        if len(action.keys()) != len(set(action.keys())):
            # This part should not be normally reached
            # Python's JSON parser has built-in duplicate key handling
            raise ValueError(f"Duplicate symbols were found in the ruleset for {state}")


# Asserts the validity of a DFA's transition function
def assert_transition_dfa(data: dict) -> None:
    for state, action in data["ruleset"].items():
        for symbol, next_state in action.items():
            # The transition function entry is (state, symbol) --> next_state
            if symbol not in data["symbols"]:
                raise ValueError(f"A rule for {state} contains {symbol}, which is not in the symbol list")
            
            if next_state not in data["states"]:
                raise ValueError(f"A rule for {state} points to {next_state}, which is not in the state list")
            

# Asserts the validity of a NFA's transition function
def assert_transition_nfa(data: dict) -> None:
    for state, action in data["ruleset"].items():
        for symbol, next_states in action.items():
            # The transition function entry is (state, symbol) --> [next_states]

            if symbol not in data["symbols"]:
                raise ValueError(f"A rule for {state} contains {symbol}, which is not in the symbol list")
                
            for next_state in next_states:
                if next_state not in data["states"]:
                    raise ValueError(f"A rule for {state} points to {next_state}, which is not in the state list")


# Asserts the validity of a TM's transition function
def assert_transition_tm(data: dict) -> None:
    # The transition is given as dictionaries containing 5 values, grouped by input symbol
    for input_symbol, rules in data["ruleset"].items():
        if input_symbol not in data["input_symbols"]:
            raise ValueError(f"Input symbol {input_symbol} has rules defined, but is not in the input symbols list")
        else:
            for rule in rules:
                # Check all required keys in a rule
                for key in ["from", "to", "shift"]:
                    if key not in rule.keys():
                        raise ValueError(f"A rule for {input_symbol} does not contain the required key {key}")
            
                # Check all the states involved in a rule
                if rule["from"]["state"] not in data["states"] or rule["to"]["state"] not in data["states"]:
                    raise ValueError(f"A rule for {input_symbol} contains a state not in the states list")
                
                # Check all the tape symbols involved in the rule
                if rule["from"]["tape"] not in data["tape_symbols"] or rule["to"]["tape"] not in data["tape_symbols"]:
                    raise ValueError(f"A rule for {input_symbol} contains a tape symbol not in the tape symbols list")

                
# Asserts the validity of a TM's blank state
def assert_blank(data: dict) -> None:
    if data["blank"] not in data["tape_symbols"]:
        raise ValueError(f"Blank symbol {data["blank"]} is not in the tape symbols list")
    

DFA_VALIDATORS = [assert_initial, assert_accepting, assert_starting, assert_unique, assert_transition_dfa]
NFA_VALIDATORS = [assert_initial, assert_accepting, assert_starting, assert_unique, assert_transition_nfa]
TM_VALIDATORS = [assert_initial, assert_accepting, assert_transition_tm]