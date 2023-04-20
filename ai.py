import logging
import math
import random


def rlu_activation(input_nr):
    if input_nr > 0:
        return input_nr
    else:
        return 0


def rlu_activation_back(input_nr):
    if input_nr > 0:
        return 1
    else:
        return 0


def reshape(input_vector):
    output_vector = [0 for _ in range(len(input_vector))]
    output_vector[input_vector.index(max(input_vector))] = 1
    return output_vector


def reshape_secured(input_vector, closed_position):
    output_vector = [0 for _ in range(len(input_vector))]
    if len(input_vector) is not len(closed_position):
        logging.log(logging.ERROR, "Wrong input")
    for idx, closed in enumerate(closed_position):
        if closed is not 0:
            input_vector[idx] = - math.inf
    output_vector[input_vector.index(max(input_vector))] = 1
    return output_vector


class Neuron:

    def __init__(self, pre_neurons=0):
        self.w = [random.uniform(-1, 1) for _ in range(pre_neurons + 1)]
        self.learn_rate = None
        self.last_input = None
        self.last_output = None
        self.learn_rate_possibility = None

    def forward(self, input_vector):
        self.last_input = [1]
        for i in input_vector:
            self.last_input.append(i)

        self.last_output = 0
        self.last_output = self.w[0] * self.last_input[0]
        for idx, i in enumerate(input_vector):
            self.last_output += i * self.w[idx + 1]
        self.last_output = self.last_output / (len(self.w) + 1)

        return rlu_activation(self.last_output)

    def recreate(self, learn_rate=0.05, learn_rate_possibility=0.1):
        self.learn_rate = learn_rate
        self.learn_rate_possibility = learn_rate_possibility

        for idx, _ in enumerate(self.w):
            if random.uniform(0, 1) < self.learn_rate_possibility:
                self.w[idx] += random.uniform(-self.learn_rate, self.learn_rate) * self.w[idx]

    def return_json(self):
        return {"w": self.w,
                "learn_rate": self.learn_rate,
                "last_input": self.last_input,
                "last_output": self.last_output,
                "learn_rate_possibility": self.learn_rate_possibility
                }

    def read_json(self, neuron_dict):
        self.w = neuron_dict["w"]
        self.learn_rate = neuron_dict["learn_rate"]
        self.last_input = neuron_dict["last_input"]
        self.last_output = neuron_dict["last_output"]
        self.learn_rate_possibility = neuron_dict["learn_rate_possibility"]

    """
    def backwards(self, results):
        delta = 0
        for i in results:
            j = (self.last_output - i) ** 2
            j = rlu_activation_back(j) * j
            delta += j
        delta /= len(self.w)
        for idx, i in enumerate(self.last_input):
            self.w[idx + 1] = self.w[idx + 1] + self.learn_rate * delta * i
    """


class Layer:

    def __init__(self, number_of_pre_neurons=0, number_of_neurons=0):
        self.number_of_pre_neurons = number_of_pre_neurons
        self.neurons = []
        while number_of_neurons > 0:
            self.neurons.append(Neuron(number_of_pre_neurons))
            number_of_neurons -= 1

    def forward(self, input_vector):
        output = []
        for neuron in self.neurons:
            output.append(neuron.forward(input_vector=input_vector))
        return output

    def recreate(self,
                 neuron_learn_rate=0.05,
                 neuron_learn_rate_possibility=0.1,
                 change_neurons=True,
                 add_neurons=0,
                 del_neurons=0):

        if change_neurons:
            for idx, _ in enumerate(self.neurons):
                self.neurons[idx].recreate(learn_rate=neuron_learn_rate,
                                           learn_rate_possibility=neuron_learn_rate_possibility)
        if add_neurons > 0:  # TODO extract as method and give position back or take only position
            for _ in range(add_neurons):
                self.neurons.append(Neuron(self.number_of_pre_neurons))

        elif del_neurons > 0:  # TODO extract as method and give position back or take only position
            for _ in range(del_neurons):
                del self.neurons[random.randint(0, len(self.neurons))]

    def reshape(self, number_of_pre_neurons):  # TODO implement
        pass

    def return_json(self):
        neurons = []
        for neuron in self.neurons:
            neurons.append(neuron.return_json())
        return {"number_of_pre_neurons": self.number_of_pre_neurons,
                "neurons": neurons}

    def read_json(self, layer_dict):
        self.number_of_pre_neurons = layer_dict["number_of_pre_neurons"]
        neurons = layer_dict["neurons"]
        for idx, neuron in enumerate(neurons):
            self.neurons.append(Neuron())
            self.neurons[idx].read_json(neuron)

    """
    def backwards(self, results):
        for neuron in self.neurons:
            neuron.backwards(results=results)
    """

    def print_layer(self):
        print("    " + str(self))
        print(len(self.neurons))
        for neuron in self.neurons:
            print("        " + str(neuron))


class Net:

    def __init__(self, input_layout=0, layout=None):
        self.layers = []
        self.connector_layout = [input_layout]
        if layout is not None:
            self.connector_layout.append([i for i in range(len(layout))])
            self.layers.append(Layer(input_layout, layout[0]))
            for idx, i in enumerate(layout[:-1]):
                if idx == 0:
                    self.layers.append(Layer(input_layout, layout[idx + 1]))
                else:
                    self.layers.append(Layer(layout[idx], layout[idx + 1]))

    def forward(self, input_vector):
        previous_board = input_vector
        for layer in self.layers:
            input_vector = layer.forward(input_vector)
        input_vector = reshape_secured(input_vector, previous_board)
        return input_vector

    def recreate(self,
                 change_layers=True,
                 add_layer=0,
                 del_layer=0,
                 neuron_learn_rate=0.05,
                 neuron_learn_rate_possibility=0.01,
                 change_neurons=True,
                 add_neurons=0,
                 del_neurons=0):

        if change_layers:
            for idx, _ in enumerate(self.layers):
                self.layers[idx].recreate(neuron_learn_rate=neuron_learn_rate,
                                          neuron_learn_rate_possibility=neuron_learn_rate_possibility,
                                          change_neurons=change_neurons,
                                          add_neurons=add_neurons,
                                          del_neurons=del_neurons)

        if add_layer > 0:
            for _ in range(add_layer):
                self.add_layer(random.randint(0, len(self.layers) - 1), 0)  # TODO adjust number

        elif del_layer > 0:
            for _ in range(del_layer):
                self.del_layer(random.randint(0, len(self.layers) - 1))

    def add_layer(self, position, number_of_neurons):
        self.layers.insert(position, Layer(number_of_pre_neurons=self.layers[position].number_of_pre_neurons,
                                           number_of_neurons=number_of_neurons))
        self.layers[position + 1].reshape(number_of_pre_neurons=number_of_neurons)  # TODO adjustfunction

    def del_layer(self, psoition):
        del self.layers[random.randint(0, len(self.layers))]  # TODO implement del

    def return_json(self):
        layers = []
        for layer in self.layers:
            layers.append(layer.return_json())
        return {"layers": layers,
                "connector_layout": self.connector_layout
                }

    def read_json(self, layer_dict):
        self.connector_layout = layer_dict["connector_layout"]
        layers = layer_dict["layers"]
        for idx, layer in enumerate(layers):
            self.layers.append(Layer())
            self.layers[idx].read_json(layer)

    def print_net(self):
        for layer in self.layers:
            print(layer)
            for neuron in layer.neurons:
                print("    " + str(neuron))
