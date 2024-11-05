
def printSolution(board, n):
    for i in range(n):
        for j in range(n):
            if board[i][j]:
                print("Q ", end="")
            else:
                print("- ", end="")
        print()
    print("\n\n")


def isSafe(board, row, col, n):
    # Check left side of the current row
    i = row
    j = col
    while j >= 0:
        if board[i][j]:
            return False
        j -= 1

    # Check upper diagonal on the left side
    i = row
    j = col
    while i >= 0 and j >= 0:
        if board[i][j]:
            return False
        i -= 1
        j -= 1

    # Check lower diagonal on the left side
    i = row
    j = col
    while i < n and j >= 0:
        if board[i][j]:
            return False
        i += 1
        j -= 1

    return True

def solve(board, n, col):
    if col >= n:
        printSolution(board, n)
        return
    for row in range(n):
        if isSafe(board, row, col, n):
            board[row][col] = 1
            solve(board, n, col + 1)
            board[row][col] = 0

if __name__ == "__main__":
    n = int(input("Enter number of queens: "))
    board = []
    for i in range(n):
        row = [0] * n  
        board.append(row)  # Append this row to the board
    solve(board, n, 0)
