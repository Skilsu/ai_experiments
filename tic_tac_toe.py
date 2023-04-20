import copy
import logging
import random


class TicTacToeBoard:
    """
    Author: guckert
    """

    def __init__(self, *args):
        if len(args) == 0:
            self.board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
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
                        nextmoves.append(TicTacToeBoard(newboard))
        return nextmoves

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



