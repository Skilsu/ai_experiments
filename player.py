import copy
import random

from ai import Net


class Player:
    names = []

    def __init__(self):
        self.win = 0
        self.name = None
        self.parent = []
        self.first = 0
        self.second = 0
        self.third = 0
        self.top_five = 0
        self.top_ten = 0
        self.top_twenty = 0
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

    def recreate(self):
        pass


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

    def recreate(self,
                 change_layers=True,
                 add_layer=None,  # [] number of new neurons per new layer -> len(add_layer) == amount of new layers
                 del_layer=0,
                 neuron_learn_probability=0.25,
                 neuron_learn_rate=0.25,
                 neuron_learn_rate_possibility=0.05,
                 neuron_change_learn_rate=True,
                 neuron_change_learn_rate_possibility=True,
                 change_neurons=True,
                 del_neurons=None,  # [] number of del neurons for each layer -> del_neurons[idx] == number of layer
                 add_neurons=None  # [] number of added neurons for each layer -> add_neurons[idx] == number of  layer
                 ):
        player = copy.deepcopy(self)
        player.net.recreate(change_layers=change_layers,
                            add_layer=add_layer,
                            del_layer=del_layer,
                            neuron_learn_probability=neuron_learn_probability,
                            neuron_learn_rate=neuron_learn_rate,
                            neuron_learn_rate_possibility=neuron_learn_rate_possibility,
                            neuron_change_learn_rate=neuron_change_learn_rate,
                            neuron_change_learn_rate_possibility=neuron_change_learn_rate_possibility,
                            change_neurons=change_neurons,
                            del_neurons=del_neurons,
                            add_neurons=add_neurons)

        player.win = 0
        player.parent.append(int(player.name[7:]))
        name = player.names[len(player.names) - 1]
        number = int(name[7:])
        player.name = "Player " + str(number + 1)
        player.names.append(player.name)
        return player


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

