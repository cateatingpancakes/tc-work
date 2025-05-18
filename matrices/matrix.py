COMMENT_SYMBOLS = ["#"]
PATH = __file__.strip().rsplit("/", maxsplit=1)[0] + "/"

# Check if the matrix dimensions are correct
def valid_dimensions(m: int, n: int, A: list[list[int]]) -> bool:
    if len(A) != m: # Line count mismatch
        return False
    for line in A: # Row count mismatch
        if len(line) != n:
            return False
        
    return True # No problems found


def save_matrix(A: list[list[int]], filename: str) -> None:
    with open(filename, "w+") as file:

        # Obtain the matrix dimensions
        m, n = len(A), len(A[0])

        if not valid_dimensions(m, n, A):
            raise ValueError(f"Dimension mismatch: expected {m} by {n} matrix as argument")
        else:
            # Save dimensions on the first line
            file.write(f"{m} {n}\n")

            # Write the rest of the matrix
            for line in A:
                file.write(" ".join(list(map(str, line))) + "\n")


def load_matrix(filename: str) -> tuple[int, int, list[list[int]]]:

    # Checks for comment lines
    def is_comment(line: str) -> bool:
        for symbol in COMMENT_SYMBOLS:
            if line.strip().startswith(symbol):
                return True
        return False


    # Extract all numbers from a string
    def extract_values(line: str) -> list[int]:
        return list(map(int, line.strip().split()))
    

    A = []
    with open(filename, "r+") as file:
        lines = file.readlines()
        lines = [line for line in lines if not is_comment(line) and # Filter out commented lines
                                           not line.strip() == ""   # Filter out blank lines
        ]

        # First line contains the dimensions
        m, n = extract_values(lines[0])

        # All the other lines have values
        for line in lines[1:]:
            A.append(extract_values(line))

    if valid_dimensions(m, n, A):
        return m, n, A
    else:
        raise ValueError(f"Dimension mismatch: expected {m} by {n} matrix in input file")


if __name__ == "__main__":
    m, n, A = load_matrix(PATH + "matrix.in")
    print(f"Got {m} by {n} matrix: {A}")
