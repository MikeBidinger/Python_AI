# Backtracking algorithm using recursion:
def solve(board):
    # Find empty position
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find
    # Check if number 1 to 9 is valid for empty position
    for num in range(1, 10):
        if valid(board, num, (row, col)):
            board[row][col] = num
            # Check next empty position
            if solve(board):
                return True
            # If there is no valid solution for position, set position to empty
            board[row][col] = 0
    # Backtrack
    return False


def valid(board, num, pos):
    # Check row
    for row in range(len(board[0])):
        if board[pos[0]][row] == num and pos[1] != row:
            return False
    # Check column
    for col in range(len(board)):
        if board[col][pos[1]] == num and pos[0] != col:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for row in range(box_y * 3, box_y * 3 + 3):
        for col in range(box_x * 3, box_x * 3 + 3):
            if board[row][col] == num and (row, col) != pos:
                return False

    return True


def print_board(board):
    print("")
    for row in range(len(board)):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - -")
        for col in range(len(board[0])):
            if col % 3 == 0 and col != 0:
                print("| ", end="")
            if col == 8:
                print(board[row][col])
            else:
                print(str(board[row][col]) + " ", end="")
    print("")


def find_empty(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)

    return None
    