"""Pentago against a depth-2 EasyAI opponent."""

from easyAI import AI_Player, Human_Player, Negamax, TwoPlayerGame

from terminal_pentago import (
    BLACK,
    EMPTY,
    WHITE,
    board_is_full,
    create_board,
    has_five,
    place_marble,
    print_board,
    rotate,
)


class PentagoGame(TwoPlayerGame):
    """Small adapter that gives EasyAI the Pentago rules."""

    def __init__(self, players):
        """Create a new game for the given players.

        Parameters:
        players (list): The human and AI players used by EasyAI.

        Returns:
        None: This method initializes the game object.
        """
        self.players = players
        self.board = create_board()
        self.current_player = 1

    def possible_moves(self):
        """Create all possible complete Pentago moves.

        Returns:
        list: Moves containing a placement, quadrant, and direction.
        """
        moves = []

        for row in range(6):
            for column in range(6):
                if self.board[row][column] == EMPTY:
                    for quadrant in ("TL", "TR", "BL", "BR"):
                        for direction in ("L", "R"):
                            move = (
                                str(row + 1)
                                + str(column + 1)
                                + " "
                                + quadrant
                                + " "
                                + direction
                            )
                            moves.append(move)
        return moves

    def make_move(self, move):
        """Place a marble and rotate a quadrant.

        Parameters:
        move (str): A move such as "24 TR R".

        Returns:
        None: This method changes the board.
        """
        parts = move.split()
        position = parts[0]
        row = int(position[0]) - 1
        column = int(position[1]) - 1
        quadrant = parts[1]
        direction = parts[2]

        if self.current_player == 1:
            player = BLACK
        else:
            player = WHITE

        place_marble(self.board, player, row, column)
        rotate(self.board, quadrant, direction)

    def win(self):
        """Check whether either player has won.

        Returns:
        bool: True if either player has five in a row.
        """
        black_wins = has_five(self.board, BLACK)
        white_wins = has_five(self.board, WHITE)
        return black_wins or white_wins

    def is_over(self):
        """Check whether the game should stop.

        Returns:
        bool: True if there is a winner or the board is full.
        """
        return self.win() or board_is_full(self.board)

    def scoring(self):
        """Give EasyAI a score for the current board.

        Returns:
        int: A positive score for a good position and a negative score
            for a bad position.
        """
        if has_five(self.board, WHITE):
            return 100 if self.current_player == 2 else -100
        if has_five(self.board, BLACK):
            return 100 if self.current_player == 1 else -100
        return 0

    def show(self):
        """Print the board and whose turn it is."""
        print_board(self.board)

        if self.current_player == 1:
            print("Your turn. Enter a move like: 24 TR R")
        else:
            print("The AI is thinking...")


def main():
    """Start a terminal game against the depth-2 AI."""
    ai = Negamax(2)
    game = PentagoGame([Human_Player(), AI_Player(ai)])
    game.play()


if __name__ == "__main__":
    main()
