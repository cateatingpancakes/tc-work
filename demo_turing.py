from automata.turing import TM

# Get the Python file's path in order to address relative to it
PATH = __file__.strip().rsplit("/", maxsplit=1)[0] + "/"

# Create a TM that copies a string around
tm = TM(PATH + "tests/turing/beaver.json")

# Let's run it until it halts, and count how many steps it took
steps = 0
while not tm.accepting():
    steps += 1
    tm.action()

# Print the result
print(f"The busy beaver finished in {steps} steps")