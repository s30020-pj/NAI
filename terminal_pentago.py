"""
A small and simple terminal version of Pentago.
Authors: Nikifor Koseda, Mateusz Aftanas

Rules o f pentago: https://www.tactic.net/site/rules/UK/12609.pdf

To run download libraries from requirements.txt and run the script in terminal with python3.

terminal_pentago.py is a simple two-player game that can be played in the terminal.
easyai_pentago.py is a small adapter that allows the EasyAI library to play Pentago against a human player.

If you want to play against human, run terminal_pentago.py. If you want to play against an AI, run easyai_pentago.py.
"""

SIZE = 6
EMPTY = "."
BLACK = "X"
WHITE = "O"


def create_board():
    """Create an empty 6x6 Pentago board.

    Returns:
    list: A board containing empty spaces.
    """
    board = []
    for row in range(SIZE):
        board.append([EMPTY] * SIZE)
    return board


def print_board(board):
    """Print the board in a readable format.

    Parameters:
    board (list): The board to print.

    Returns:
    None: This function only prints the board.
    """
    print()
    print("  1 2 3 | 4 5 6")
    for row in range(SIZE):
        text = " ".join(board[row][0:3])
        text += " | "
        text += " ".join(board[row][3:6])
        print(str(row + 1) + " " + text)
        if row == 2:
            print("  ------+------")


def place_marble(board, player, row, column):
    """Place a player's marble on an empty board space.

    Parameters:
    board (list): The board to change.
    player (str): The marble to place, either X or O.
    row (int): The zero-based row number.
    column (int): The zero-based column number.

    Returns:
    bool: True if the marble was placed, otherwise False.
    """
    if row < 0 or row >= SIZE or column < 0 or column >= SIZE:
        return False
    if board[row][column] != EMPTY:
        return False

    board[row][column] = player
    return True


def rotate(board, quadrant, direction):
    """Rotate one 3x3 quadrant of the board.

    Parameters:
    board (list): The board to change.
    quadrant (str): The quadrant to rotate: TL, TR, BL, or BR.
    direction (str): L for left or R for right.

    Returns:
    bool: True if the rotation was valid, otherwise False.
    """
    # Find the top-left corner of the selected 3x3 quadrant.
    if quadrant == "TL":
        top, left = 0, 0
    elif quadrant == "TR":
        top, left = 0, 3
    elif quadrant == "BL":
        top, left = 3, 0
    elif quadrant == "BR":
        top, left = 3, 3
    else:
        return False

    # Copy the quadrant before changing it.
    old = []
    for row in range(3):
        old.append(board[top + row][left:left + 3])

    # Put each old cell into its new position.
    for row in range(3):
        for column in range(3):
            if direction == "R":
                board[top + row][left + column] = old[2 - column][row]
            else:
                board[top + row][left + column] = old[column][2 - row]
    return True


def has_five(board, player):
    """Check whether a player has five marbles in a row.

    Parameters:
    board (list): The board to check.
    player (str): The player to check, either X or O.

    Returns:
    bool: True if the player has five in a row, otherwise False.
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for row in range(SIZE):
        for column in range(SIZE):
            for row_step, column_step in directions:
                count = 0
                for number in range(5):
                    new_row = row + number * row_step
                    new_column = column + number * column_step
                    if (0 <= new_row < SIZE
                            and 0 <= new_column < SIZE
                            and board[new_row][new_column] == player):
                        count += 1
                if count == 5:
                    return True
    return False


def board_is_full(board):
    """Check whether every space on the board is occupied.

    Parameters:
    board (list): The board to check.

    Returns:
    bool: True if the board is full, otherwise False.
    """
    for row in board:
        if EMPTY in row:
            return False
    return True


def main():
    """Run a local two-player terminal game."""
    board = create_board()
    player = BLACK

    print("Simple Pentago")
    print("Enter moves like: 2 4 or 24")
    print("Then rotate like: TR R")
    print("Use TL, TR, BL, or BR and L or R.")

    while True:
        print()
        print_board(board)
        print()
        print("Player " + player + ": place a marble.")

        while True:
            text = input("Row and column (or q): ").upper().split()
            if text == ["Q"]:
                return
            if len(text) == 1 and len(text[0]) == 2 and text[0].isdigit():
                text = [text[0][0], text[0][1]]
            if len(text) != 2:
                print("Please enter two numbers, for example: 2 4 or 24")
                continue
            try:
                row = int(text[0]) - 1
                column = int(text[1]) - 1
            except ValueError:
                print("Rows and columns must be numbers.")
                continue
            if place_marble(board, player, row, column):
                break
            print("That space is not available.")

        print_board(board)

        while True:
            text = input("Quadrant and direction (TL/TR/BL/BR L/R): ").upper().split()
            if len(text) == 2 and text[1] in ("L", "R"):
                if rotate(board, text[0], text[1]):
                    break
            print("Example: TR R")

        black_wins = has_five(board, BLACK)
        white_wins = has_five(board, WHITE)
        print_board(board)

        if black_wins and white_wins:
            print("Draw: both players have five in a row.")
            return
        if black_wins:
            print("Player X wins!")
            return
        if white_wins:
            print("Player O wins!")
            return
        if board_is_full(board):
            print("Draw: the board is full.")
            return

        if player == BLACK:
            player = WHITE
        else:
            player = BLACK


if __name__ == "__main__":
    main()
