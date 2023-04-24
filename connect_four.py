import logging

from boards import Board


class ConnectFourBoard(Board):
    """
    Author: guckert
    """

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) == 0:
            self.board = [['_', '_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_', '_']
                          ]
        else:
            self.board = args[0]

    def is_winning(self):
        b = self.board
        res = False
        for i in range(len(b)):
            for j in range(len(b[0])):
                if j < len(b[0]) - 3:
                    if b[i][j] == b[i][j + 1] == b[i][j + 2] == b[i][j + 3] == b[i][3] != '_':
                        if b[i][j] == 'X':
                            self.isWinningBoardValue = 1
                        else:
                            self.isWinningBoardValue = -1
                        res = True
                if i < len(b) - 3:
                    if b[i][j] == b[i + 1][j] == b[i + 2][j] == b[i + 3][j] == b[2][j] == b[3][j] != '_':
                        if b[i][j] == 'X':
                            self.isWinningBoardValue = 1
                        else:
                            self.isWinningBoardValue = -1
                        res = True
                if i < len(b) - 3 and j < len(b[0]) - 3:
                    if b[i][j] == b[i + 1][j + 1] == b[i + 2][j + 2] == b[i + 3][j + 3] != '_' and 0 < i < 3 and 0 < j < 4:
                        if b[i][j] == 'X':
                            self.isWinningBoardValue = 1
                        else:
                            self.isWinningBoardValue = -1
                        res = True
                    if b[i][j + 3] == b[i + 1][j + 2] == b[i + 2][j + 1] == b[i + 3][j] != '_' and 0 < i < 3 and 0 < j < 4:
                        if b[i][j + 3] == 'X':
                            self.isWinningBoardValue = 1
                        else:
                            self.isWinningBoardValue = -1
                        res = True
            if res:
                self.isWinningBoard = True
        return res

    def set_board(self, value_list):
        for idx, _ in enumerate(self.board):
            for jdx, _ in enumerate(self.board[idx]):
                if value_list[(idx * 7) + jdx] == 1:
                    self.board[idx][jdx] = "X"
                elif value_list[(idx * 7) + jdx] == -1:
                    self.board[idx][jdx] = "O"
                elif value_list[(idx * 7) + jdx] == 0:
                    self.board[idx][jdx] = "_"
                else:
                    logging.log(logging.ERROR, "invalid board!")

    def move_vector(self, vector, value):
        for idx, i in enumerate(vector):
            if i != 0:
                self.move(idx, value)
                break

    def move(self, position, value):
        i = 0
        for idx, column in enumerate(self.board):
            if column[position] != "_":
                break
            i = idx
        if value == 1:
            value = "X"
        elif value == -1:
            value = "O"
        else:
            raise ValueError(f"Expected 1 or -1 but got {value}")
        self.board[i][position] = value

    def get_closed_positions(self):
        closed_positions = []
        for i in self.board[0]:
            if i == "_":
                closed_positions.append(0)
            else:
                closed_positions.append(1)
        print(closed_positions)
        return closed_positions
