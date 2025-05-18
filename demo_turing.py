from automata.turing import TM

# Get the Python file's path in order to address relative to it
PATH = __file__.strip().rsplit("/", maxsplit=1)[0] + "/"

# Create a TM that copies a string around
tm = TM(PATH + "tests/turing/string_copies.json")

# Give it a testing input tape and a pointer to start with
tm.set_tape(["$", "0", "1", "1"], 1)

# While it is fed the input symbol 1, it will move along and start
# copying the string repeatedly, to the (blank) right of its tape
for _ in range(ONES := 125):
    tm.action("1")

# While it is fed the input symbol 0, it cleans up after itself until it halts
# This would theoretically be a problem (we can't know if an arbitrary TM is
# going to halt) but from the way we've constructed ours, it eventually will
while not tm.halted:
    tm.action("0")

# Show whether the TM accepted or not
print(f"Accepting: {tm.accepting()}, current state: {tm.state}, halted: {tm.halted}")

# Show the tape using a window and ignoring all blank symbols on the ends
print("".join(tm.get_tape(FRONT := 0, BACK := 25)).strip(tm.data["blank"]))
