import json

from ai import Net
from connect_four import ConnectFourBoard
from player import Player, PlayerRandom, PlayerAiTicTacToe, PlayerAiConnectFour, PlayerRandomConnectFour, \
    PlayerTrainerConnectFour
from tic_tac_toe import TicTacToeBoard


def save_players(filename, player):
    filename = filename + ".json"
    with open(filename, "w") as outfile:
        json.dump(player, outfile)


def read_players(filename):
    filename = filename + ".json"
    with open(filename, "r") as infile:
        player_json = json.load(infile)
    #  TODO operate with player_json


def tic_tac_toe_game(player1, player2, log=False):
    current_game = TicTacToeBoard()
    turn = True
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


def connect_four_game(player1, player2, log=False):
    current_game = ConnectFourBoard()
    turn = True
    while not current_game.isWinningBoard:
        if turn:
            current_game.move_vector(player1.play(current_game.get_list()), 1)
        else:
            current_game.move_vector(player2.play(current_game.get_list(), p1=False), -1)
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


def tic_tac_toe_learning():
    player = [Player()]
    player.clear()
    player.extend([PlayerAiTicTacToe(9, [9, 12, 9, 9]) for _ in range(10)])
    player.extend(PlayerAiTicTacToe(9, [9, 12, 12, 9]) for _ in range(10))
    player.extend(PlayerAiTicTacToe(9, [9, 9, 9, 9]) for _ in range(10))
    player.extend(PlayerAiTicTacToe(9, [9, 12, 9]) for _ in range(10))
    player.extend(PlayerAiTicTacToe(9, [9, 6, 6, 9]) for _ in range(10))
    player.extend(PlayerAiTicTacToe(9, [6, 12, 6, 9]) for _ in range(10))
    player.extend(PlayerAiTicTacToe(9, [6, 6, 9]) for _ in range(10))
    player.extend(PlayerAiTicTacToe(9, [9, 9]) for _ in range(10))
    player.extend(PlayerRandom() for _ in range(20))
    print("Top Ten of the Players:")
    while True:
        for player1 in player:
            for player2 in player:
                tic_tac_toe_game(player1, player2)
        sorted_players = sorted(player, key=lambda x: x.win, reverse=True)
        sorted_players[0].first += 1
        sorted_players[1].second += 1
        sorted_players[2].third += 1
        for idx, i in enumerate(sorted_players[:5]):
            sorted_players[idx].top_five += 1
        for idx, i in enumerate(sorted_players[:10]):
            sorted_players[idx].top_ten += 1
        for idx, i in enumerate(sorted_players[:20]):
            sorted_players[idx].top_twenty += 1
        for idx, i in enumerate(sorted_players):
            print(idx, i.name, i.win, i.parent)
        print(f"Newest Player: {player[len(player) - 1].name}")
        print("Press any key to continue...")
        input()
        print("Continuing...")
        player = sorted_players[:25]
        for idx, _ in enumerate(player):
            player[idx].win = 0
        player.extend([PlayerAiTicTacToe(9, [9, 12, 9, 9]) for _ in range(5)])
        player.extend(PlayerAiTicTacToe(9, [9, 12, 12, 9]) for _ in range(5))
        player.extend(PlayerAiTicTacToe(9, [9, 9, 9, 9]) for _ in range(5))
        player.extend(PlayerAiTicTacToe(9, [9, 12, 9]) for _ in range(5))
        player.extend(PlayerAiTicTacToe(9, [9, 6, 6, 9]) for _ in range(5))
        player.extend(PlayerAiTicTacToe(9, [6, 12, 6, 9]) for _ in range(5))
        player.extend(PlayerAiTicTacToe(9, [6, 6, 9]) for _ in range(5))
        player.extend(PlayerAiTicTacToe(9, [9, 9]) for _ in range(5))
        player.extend(player[0].recreate() for _ in range(10))
        player.extend(player[1].recreate() for _ in range(9))
        player.extend(player[2].recreate() for _ in range(8))
        player.extend(player[3].recreate() for _ in range(7))
        player.extend(player[4].recreate() for _ in range(6))
        player.extend(player[5].recreate() for _ in range(5))
        player.extend(player[6].recreate() for _ in range(4))
        player.extend(player[7].recreate() for _ in range(3))
        player.extend(player[8].recreate() for _ in range(2))
        player.extend(player[9].recreate() for _ in range(1))
        print(f"There are now {len(player)}")
        print(f"Current top Ten:")


def connect_four_learning():
    player = [Player()]
    player[0].names.clear()
    player.clear()
    player.extend([PlayerAiConnectFour([42, 20, 20, 15]) for _ in range(10)])
    player.extend(PlayerAiConnectFour([30, 20, 30, 10]) for _ in range(10))
    player.extend(PlayerAiConnectFour([25, 25, 25]) for _ in range(10))
    player.extend(PlayerAiConnectFour([15, 20, 10]) for _ in range(10))
    player.extend(PlayerAiConnectFour([25, 10, 10, 25]) for _ in range(10))
    player.extend(PlayerAiConnectFour([40, 40, 40, 40]) for _ in range(10))
    player.extend(PlayerAiConnectFour([20, 20, 20]) for _ in range(10))
    player.extend(PlayerAiConnectFour([10, 10]) for _ in range(10))
    player.extend(PlayerRandomConnectFour() for _ in range(20))
    trainer = [PlayerTrainerConnectFour(repeat_random=True) for _ in range(10)]
    trainer.extend([PlayerTrainerConnectFour(fill_columns=True) for _ in range(10)])
    while True:
        for player1 in player:
            print(f"Playing {player1.name}")
            for player2 in player:
                connect_four_game(player1, player2)
        print("Training...")
        for player1 in player:
            for trainer1 in trainer:
                connect_four_game(player1, trainer1)
        sorted_players = sorted(player, key=lambda x: x.win, reverse=True)
        sorted_players[0].first += 1
        sorted_players[1].second += 1
        sorted_players[2].third += 1
        print(f"Current top Ten:")
        for idx, i in enumerate(sorted_players[:5]):
            sorted_players[idx].top_five += 1
        for idx, i in enumerate(sorted_players[:10]):
            sorted_players[idx].top_ten += 1
        for idx, i in enumerate(sorted_players[:20]):
            sorted_players[idx].top_twenty += 1
        for idx, i in enumerate(sorted_players[:20]):
            print(idx, i.name, i.win, i.parent)
        print(f"Current last Player:")
        for idx, i in enumerate(sorted_players[100:]):
            print(idx, i.name, i.win, i.parent)
        print(f"Newest Player: {player[len(player) - 1].name}")
        print(f"Game of the best Players {sorted_players[0].name} and {sorted_players[1].name}")
        connect_four_game(sorted_players[0], sorted_players[1], log=True)
        print(f"Rematch!")
        connect_four_game(sorted_players[1], sorted_players[0], log=True)
        print("Press any key to continue...")
        input()
        print("Continuing...")
        player = sorted_players[:25]
        for idx, _ in enumerate(player):
            player[idx].win = 0
        player.extend([PlayerAiConnectFour([42, 20, 20, 15]) for _ in range(5)])
        player.extend(PlayerAiConnectFour([30, 20, 30, 10]) for _ in range(5))
        player.extend(PlayerAiConnectFour([25, 25, 25]) for _ in range(5))
        player.extend(PlayerAiConnectFour([15, 20, 10]) for _ in range(5))
        player.extend(PlayerAiConnectFour([25, 10, 10, 25]) for _ in range(5))
        player.extend(PlayerAiConnectFour([40, 40, 40, 40]) for _ in range(5))
        player.extend(PlayerAiConnectFour([20, 20, 20]) for _ in range(5))
        player.extend(PlayerAiConnectFour([10, 10]) for _ in range(5))
        player.extend(player[0].recreate() for _ in range(5))
        player.extend(player[1].recreate() for _ in range(5))
        player.extend(player[2].recreate() for _ in range(5))
        player.extend(player[3].recreate() for _ in range(3))
        player.extend(player[4].recreate() for _ in range(3))
        player.extend(player[5].recreate() for _ in range(3))
        player.extend(player[6].recreate() for _ in range(2))
        player.extend(player[7].recreate() for _ in range(2))
        player.extend(player[8].recreate() for _ in range(2))
        player.extend(PlayerRandomConnectFour() for _ in range(20))
        print(f"There are now {len(player)}")


def test_reshape():
    n = Net(3, [3, 4, 5, 6, 7])
    n.recreate(change_layers=True,
               neuron_learn_rate=0.5,
               change_neurons=True,
               del_neurons=None,
               add_neurons=[[1, 2, 4], [], [], [], []])
    print(n.connector_layout)
    # n.print_net()


def main():
    # connect_four_game(PlayerTrainerConnectFour(fill_columns=True), PlayerTrainerConnectFour(repeat_random=True), True)
    connect_four_learning()


if __name__ == '__main__':
    main()
