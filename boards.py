import copy


class Board:
    def __init__(self, *args):
        if len(args) == 0:
            self.board = []
        else:
            self.board = args[0]
        self.isWinningBoard = False
        self.isWinningBoardValue = 0
        self.symbol = ' '
        self.symmetry_id = -1
        self.minimax = 0
        self.alpha = 0
        self.beta = 0

    def print_board(self):
        for i in self.board:
            print(i)

    def expand(self, symbol):
        self.symbol = symbol
        nextmoves = []
        if not self.is_winning():
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == "_":
                        newboard = copy.deepcopy(self.board)
                        newboard[i][j] = symbol
                        nextmoves.append(Board(newboard))
        return nextmoves

    def is_winning(self):
        pass

    def get_list(self):
        board = []
        for i in self.board:
            board.extend(i)
        for idx, pos in enumerate(board):
            if pos == "_":
                board[idx] = 0
            elif pos == "X":
                board[idx] = 1
            elif pos == "O":
                board[idx] = -1
        return board

    def set_board(self, value_list):
        pass
