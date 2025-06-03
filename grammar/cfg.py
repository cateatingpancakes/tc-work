import json
from collections import defaultdict

class CFG:
    # Loads a CFG from a file
    def load_grammar(self, filename: str) -> None:
        with open(filename, "r+") as file:
            self.data = json.load(file)


    # Saves a CFG to a file
    def save_grammar(self, filename: str) -> None:
        if self.data is not None:
            with open(filename, "w+") as file:
                json.dump(self.data, file, indent=4)


    # Checks whether a string belongs to the CFG, assuming CNF
    def match_string(self, string: str) -> bool:
        # Returns a tuple with the arguments, needed for accessing prod/back
        def at(a: str, b: str, c: str) -> tuple:
            return tuple([a, b, c])

        # Returns the index of the variable V in the variable list
        def var(V: str) -> int:
            return self.data["variables"].index(V) + 1

        # Checks if a production is an unit production
        def is_unit(production) -> bool:
            produced = production["to"]
            # Initial assumption is that it's an unit production
            unit = True
            # Check if it is by checking if it has any variables
            for symbol in produced:
                if symbol in self.data["variables"]:
                    unit = False
            # Return the result
            return unit


        # CYK algorithm implementation
        back, prod, n = defaultdict(list), defaultdict(lambda: False), len(string)

        for s in range(1, n + 1):
            for q in self.data["productions"]:
                if is_unit(q) and q["to"] == string[s - 1]:
                    v = self.data["variables"].index(q["from"]) + 1
                    prod[at(1, s, v)] = True
        

        for l in range(2, n + 1):
            for s in range(1, n - l + 2):
                for p in range(1, l):
                    for q in self.data["productions"]:
                        if not is_unit(q):
                            a, b, c = var(q["from"]), var(q["to"][0]), var(q["to"][1])
                            if prod[at(p, s, b)] and prod[at(l - p, s + p, c)]:
                                prod[at(l, s, a)] = True
                                back[at(l, s, a)].append(at(p, b, c))


        # Final check
        if prod[at(n, 1, 1)]:
            return back
            

    # CFG constructor, can load from a .json file
    def __init__(self, filename: str = None):
        # Load from a .json, if any was given
        if filename is not None:
            self.load_grammar(filename)