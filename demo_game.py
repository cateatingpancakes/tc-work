import json
from automata.dfa import DFA

INVENTORY_DELIMITER = "__"
ITEM_DELIMITER = "%"

# Loads JSON data from a gamedescribe file
def load_description(filename: str) -> dict:
    with open(filename, "r+") as file:
        return json.load(file)


# Creates a DFA from gamedescribe data
def make_DFA(data: dict) -> DFA:

    # Returns all subsets of a set
    def powerset(seq: list):
        if len(seq) <= 1:
            yield seq
            yield []
        else:
            for item in powerset(seq[1:]):
                yield [seq[0]] + item
                yield item


    # Returns all subsets of a set that each contain some required elements
    def filtered_powerset(seq: list, required: list):
        for subset in powerset(seq):
            # Check all the requirements are met
            if set(required) <= set(subset):
                yield subset


    # Returns the label of a state with a given inventory
    def state_name(state: str, inventory: list[str]) -> str:
        # On an empty inventory, return just the state
        if inventory == []:
            return state
        
        # Otherwise, sort and format
        inventory.sort()
        return state + INVENTORY_DELIMITER + ITEM_DELIMITER.join(inventory)
    

    # We want to construct a DFA that runs the described game
    game = DFA()
    # We start with no data in the dictionary that tells it how to run
    game.data = dict()

    # First, we find all possible states a player can be in
    states = []

    # A player can be in any room
    for room in data["rooms"]:
        # In each room, the player could have any inventory
        for inventory in powerset(data["items"]):
            states.append(state_name(room, inventory))

    # Add the states we found to the game-DFA
    game.data["states"] = states

    # We now find the accepting states
    # Naturally, the win states are accepting
    # States in winning rooms, but with items, are also accepting
    accepting = []
    for state in data["win"]:
        for inventory in powerset(data["items"]):
            accepting.append(state_name(state, inventory))
    

    # Add the accepting states
    game.data["accepting"] = accepting

    # Set the starting state
    game.data["initial"] = data["start"]
    # Also put the automata in this starting state
    game.state = data["start"]

    # Set the alphabet/symbols
    game.data["symbols"] = data["actions"]

    # Constructing the transition function
    # First we represent a list of all transitions
    # Then we convert this list into our DFA's format
    ruleset = []
    for move in data["moves"]:
        for inventory in filtered_powerset(data["items"], move["if"]):
            ruleset.append({
                "from": state_name(move["from"], inventory),
                "to": state_name(move["to"], inventory),
                "on": move["on"]
            })
    
    # Add the "get" action
    for get in data["gets"]:
        for inventory in filtered_powerset(data["items"], get["if"]):
            # Remove any items lost through the get action
            # Add any items gained through the get action
            new_inventory = list(set(inventory)
                                 .difference(set(get["loses"]))
                                 .union(set(get["gains"])))
            ruleset.append({
                "from": state_name(get["where"], inventory),
                "to": state_name(get["where"], new_inventory),
                "on": data["bind"]
            })

    # Convert the ruleset to the DFA format
    dfa_ruleset = dict()
    for rule in ruleset:
        # Create the key if it doesn't exist already
        if rule["from"] not in dfa_ruleset.keys():
            dfa_ruleset[rule["from"]] = dict()

        # Then add the rule
        dfa_ruleset[rule["from"]][rule["on"]] = rule["to"]

    # Finally, add the converted ruleset
    game.data["ruleset"] = dfa_ruleset
    
    return game


# Get the Python file's path in order to address relative to it
PATH = __file__.strip().rsplit("/", maxsplit=1)[0] + "/"
# Get the data from a gamedescribe .json file
data = load_description("gamedescribe/small_game.json")
# Make the DFA for the described game
game = make_DFA(data)
# Save it to the DFA tests directory for later use
game.save_automata("tests/dfa/small_game.json")

# Now let's play!
while not game.accepting():
    symbol = input("What to do: ").strip()
    game.action(symbol)
    print(f"State: {game.state}")
