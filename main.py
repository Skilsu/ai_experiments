import json
import logging
import random
from ai import Net
from tic_tac_toe import TicTacToeBoard


class Player:
    names = []

    def __init__(self):
        self.win = 0
        self.name = None
        if not self.names:
            self.name = "Player 1"
        else:
            name = self.names[len(self.names) - 1]
            number = int(name[7:])
            self.name = "Player " + str(number + 1)

        self.names.append(self.name)

    def play(self, board, p1=True):
        pass

    def won(self):
        self.win += 1

    def lost(self):
        self.win -= 1


class PlayerAi(Player):
    def __init__(self, input_layout, layout):
        super().__init__()
        self.net = Net(input_layout, layout)

    def play(self, input_vector, p1=True):
        output_vector = self.net.forward(input_vector=input_vector)

        if not p1:
            for idx, _ in enumerate(output_vector):
                if output_vector[idx] == 1:
                    output_vector[idx] = -1

        for idx, _ in enumerate(output_vector):
            if input_vector[idx] != 0:
                output_vector[idx] = input_vector[idx]
        return output_vector


class PlayerRandom(Player):
    def __init__(self):
        super().__init__()

    def play(self, board, p1=True):
        empty_position = []
        for idx, i in enumerate(board):
            if i == 0:
                empty_position.append(idx)
        if p1:
            res = 1
        else:
            res = -1
        board[empty_position[random.randint(0, len(empty_position) - 1)]] = res
        return board


def game(player1, player2, log=False):
    current_game = TicTacToeBoard()
    turn = True
    res = 0
    while not current_game.isWinningBoard:
        if turn:
            current_game.set_board(player1.play(current_game.get_list()))
        else:
            current_game.set_board(player2.play(current_game.get_list(), p1=False))
        turn = not turn
        if log:
            print("")
            current_game.print_board()
        if not current_game.is_winning():
            if 0 not in current_game.get_list():
                break
    if current_game.isWinningBoardValue < 0:
        player2.won()
        player1.lost()
    elif current_game.isWinningBoardValue > 0:
        player1.won()
        player2.lost()


def learning():
    player = [Player()]
    player.clear()
    player.extend([PlayerAi(9, [9, 12, 9, 9]) for _ in range(10)])
    player.extend(PlayerAi(9, [9, 12, 12, 9]) for _ in range(10))
    player.extend(PlayerAi(9, [9, 9, 9, 9]) for _ in range(10))
    player.extend(PlayerAi(9, [9, 12, 9]) for _ in range(10))
    player.extend(PlayerAi(9, [9, 6, 6, 9]) for _ in range(10))
    player.extend(PlayerAi(9, [6, 12, 6, 9]) for _ in range(10))
    player.extend(PlayerAi(9, [6, 6, 9]) for _ in range(10))
    player.extend(PlayerAi(9, [9, 9]) for _ in range(10))
    player.extend(PlayerRandom() for _ in range(20))
    print("Top Ten of the Players:")
    player[0].net.print_net()
    print(player[0].net.connector_layout)
    while True:
        for player1 in player:
            for player2 in player:
                game(player1, player2)
        sorted_players = sorted(player, key=lambda x: x.win, reverse=True)
        for idx, i in enumerate(sorted_players[:10]):
            print(idx, i.name)
        print("Press any key to continue...")
        input()
        print("Continuing...")
        player = sorted_players[:10]
        for idx, _ in enumerate(player):
            player[idx].win = 0
        player.extend([PlayerAi(9, [9, 12, 9, 9]) for _ in range(9)])
        player.extend(PlayerAi(9, [9, 12, 12, 9]) for _ in range(9))
        player.extend(PlayerAi(9, [9, 9, 9, 9]) for _ in range(9))
        player.extend(PlayerAi(9, [9, 12, 9]) for _ in range(9))
        player.extend(PlayerAi(9, [9, 6, 6, 9]) for _ in range(9))
        player.extend(PlayerAi(9, [6, 12, 6, 9]) for _ in range(9))
        player.extend(PlayerAi(9, [6, 6, 9]) for _ in range(9))
        player.extend(PlayerAi(9, [9, 9]) for _ in range(9))
        player.extend(PlayerRandom() for _ in range(18))
        print(f"There are now {len(player)}")
        print(f"Current top Ten:")


def main():
    learning()


if __name__ == '__main__':
    main()
