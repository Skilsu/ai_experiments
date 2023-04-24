import copy
import logging
from boards import Board


class TicTacToeBoard(Board):

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) == 0:
            self.board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        else:
            self.board = args[0]

    def is_winning(self):
        b = self.board
        res = False
        for i in range(len(b)):
            if b[i][0] == b[i][1] and b[i][0] == b[i][2] and b[i][0] != '_':
                if b[i][0] == 'X':
                    self.isWinningBoardValue = 1
                else:
                    self.isWinningBoardValue = -1
                res = True
            if b[0][i] == b[1][i] and b[0][i] == b[2][i] and b[0][i] != '_':
                if b[0][i] == 'X':
                    self.isWinningBoardValue = 1
                else:
                    self.isWinningBoardValue = -1
                res = True
        if b[0][0] == b[1][1] and b[0][0] == b[2][2] and b[0][0] != '_':
            if b[0][0] == 'X':
                self.isWinningBoardValue = 1
            else:
                self.isWinningBoardValue = -1
            res = True
        if b[0][2] == b[1][1] and b[0][2] == b[2][0] and b[0][2] != '_':
            if b[0][2] == 'X':
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
                if value_list[(idx * 3) + jdx] == 1:
                    self.board[idx][jdx] = "X"
                elif value_list[(idx * 3) + jdx] == -1:
                    self.board[idx][jdx] = "O"
                elif value_list[(idx * 3) + jdx] == 0:
                    self.board[idx][jdx] = "_"
                else:
                    logging.log(logging.ERROR, "invalid board!")



