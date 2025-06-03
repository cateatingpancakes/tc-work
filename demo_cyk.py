from grammar.cfg import CFG

# Get the Python file's path in order to address relative to it
PATH = __file__.strip().rsplit("/", maxsplit=1)[0] + "/"

# Create a CFG (assuming it's in CNF here)
# This CFG is equivalent to the RegEx b*ab
cfg = CFG(PATH + "tests/cfg/cfg.json")

# Test the CYK algorithm
# Should match, i.e. output True
print(cfg.match_string("bbbab") is not None)
# Should fail, i.e output False
print(cfg.match_string("bbabb") is not None)
