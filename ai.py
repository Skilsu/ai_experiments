import logging
import math
import random

# from numba import jit


# @jit
def rlu_activation(input_nr):
    if input_nr > 0:
        return input_nr
    else:
        return 0


# @jit
def rlu_activation_back(input_nr):
    if input_nr > 0:
        return 1
    else:
        return 0


def reshape(input_vector):
    output_vector = [0 for _ in range(len(input_vector))]
    output_vector[input_vector.index(max(input_vector))] = 1
    return output_vector


# @jit
def reshape_secured(input_vector, closed_position):
    output_vector = [0 for _ in range(len(input_vector))]
    if len(input_vector) != len(closed_position):
        logging.log(logging.ERROR, "Wrong input")
    for idx, closed in enumerate(closed_position):
        if closed != 0:
            input_vector[idx] = - math.inf
    output_vector[input_vector.index(max(input_vector))] = 1
    return output_vector


class Neuron:

    def __init__(self, pre_neurons=0):
        self.pre_neurons = pre_neurons
        self.w = [random.uniform(-1, 1) for _ in range(self.pre_neurons + 1)]
        self.learn_rate = None
        self.learn_rate_possibility = None
        self.last_input = None
        self.last_output = 0.0
        self.cummulated_output = 0

    # @jit
    def forward(self, input_vector):
        if len(input_vector) != self.pre_neurons:
            raise ValueError(f"Expected a input_vector of length {self.pre_neurons=}"
                                 f", but got a list of length {len(input_vector)=}.\n"
                                 f"{len(self.w)=}\n{len(input_vector)=}\n{self.pre_neurons=}")
        self.last_input = [1]
        for i in input_vector:
            self.last_input.append(i)
            
        for idx, i in enumerate(self.last_input):
            try:
                self.last_output += i * self.w[idx]  # TODO still error from time to time (list index out of range)
            except IndexError as e:
                print(f"{len(self.w)=}\n{self.w=}\n{idx=}\n{i=}\n{len(input_vector)=}\n{input_vector=}\n{self.pre_neurons=}")
                raise e
        self.last_output = self.last_output / (len(self.w))
        output = rlu_activation(self.last_output)
        self.cummulated_output += output
        return output

    def recreate(self,
                 learn_rate,
                 learn_rate_possibility,
                 change_learn_rate=True,
                 change_learn_rate_possibility=True):

        if change_learn_rate:
            self.learn_rate = learn_rate
        if change_learn_rate_possibility:
            self.learn_rate_possibility = learn_rate_possibility

        for idx, _ in enumerate(self.w):
            if random.uniform(0, 1) < self.learn_rate_possibility:
                self.w[idx] += random.uniform(-self.learn_rate, self.learn_rate) * self.w[idx]

    def reshape(self, number_of_pre_neurons):
        if number_of_pre_neurons < self.pre_neurons:
            while number_of_pre_neurons < self.pre_neurons:
                del self.w[random.randint(0, len(self.w) - 1)]
                self.pre_neurons -= 1
                
        elif number_of_pre_neurons > self.pre_neurons:
            while number_of_pre_neurons > self.pre_neurons:
                self.w.append(random.uniform(-1, 1))
                self.pre_neurons += 1

    def insert_weight(self, position):
        self.w.insert(position + 1, random.uniform(-1, 1))

    def delete_weight(self, position):
        del self.w[position + 1]

    def return_json(self):
        return {"w": self.w,
                "pre_neurons": self.pre_neurons,
                "learn_rate": self.learn_rate,
                "last_input": self.last_input,
                "last_output": self.last_output,
                "learn_rate_possibility": self.learn_rate_possibility,
                "cummulated_output": self.cummulated_output
                }

    def read_json(self, neuron_dict):
        self.w = neuron_dict["w"]
        self.pre_neurons = neuron_dict["pre_neurons"]
        self.learn_rate = neuron_dict["learn_rate"]
        self.last_input = neuron_dict["last_input"]
        self.last_output = neuron_dict["last_output"]
        self.learn_rate_possibility = neuron_dict["learn_rate_possibility"]
        self.cummulated_output = neuron_dict["cummulated_output"]

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

    # @jit
    def forward(self, input_vector):
        output = []
        for neuron in self.neurons:
            output.append(neuron.forward(input_vector=input_vector))
        return output

    def recreate(self,
                 neuron_learn_probability=0.25,
                 neuron_learn_rate=0.05,
                 neuron_learn_rate_possibility=0.1,
                 neuron_change_learn_rate=True,
                 neuron_change_learn_rate_possibility=True,
                 change_neurons=True,
                 del_neurons=None,  # list of positions to delete
                 add_neuron=None,  # list of positions to delete
                 prev_del_neurons=None,  # list of positions to delete
                 prev_add_neurons=None  # list of positions to delete
                 ):

        if change_neurons:
            for idx, _ in enumerate(self.neurons):
                if random.uniform(0, 1) <= neuron_learn_probability:
                    self.neurons[idx].recreate(learn_rate=neuron_learn_rate,
                                               learn_rate_possibility=neuron_learn_rate_possibility,
                                               change_learn_rate=neuron_change_learn_rate,
                                               change_learn_rate_possibility=neuron_change_learn_rate_possibility)

        if del_neurons is not None:  # TODO extract as method
            for position in del_neurons:
                del self.neurons[position]
        if add_neuron is not None:  # TODO extract as method
            for position in add_neuron:
                self.neurons.insert(position, Neuron(self.number_of_pre_neurons))

        if prev_del_neurons is not None:
            for position in prev_del_neurons:
                for idx, _ in enumerate(self.neurons):
                    self.neurons[idx].delete_weight(position)
        if prev_add_neurons is not None:
            for position in prev_add_neurons:
                for idx, _ in enumerate(self.neurons):
                    self.neurons[idx].insert_weight(position)

    def reshape_neurons(self, number_of_pre_neurons):
        for idx, _ in enumerate(self.neurons):
            self.neurons[idx].reshape(number_of_pre_neurons)
        self.number_of_pre_neurons = number_of_pre_neurons

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
            self.connector_layout.extend(i for i in layout)
            self.layers.append(Layer(input_layout, layout[0]))
            for idx, i in enumerate(layout[:-1]):
                self.layers.append(Layer(layout[idx], layout[idx + 1]))

    # @jit
    def forward(self, input_vector, closed_positions):
        output_vector = input_vector
        for layer in self.layers:
            output_vector = layer.forward(output_vector)
        output_vector = reshape_secured(output_vector, closed_positions)
        return output_vector

    def recreate(self,
                 change_layers=True,
                 add_layer=None,  # [] number of new neurons per new layer -> len(add_layer) == amount of new layers
                 del_layer=0,
                 neuron_learn_probability=0.25,
                 neuron_learn_rate=0.05,
                 neuron_learn_rate_possibility=0.01,
                 neuron_change_learn_rate=True,
                 neuron_change_learn_rate_possibility=True,
                 change_neurons=True,
                 del_neurons=None,  # [] number of del neurons for each layer -> del_neurons[idx] == number of layer
                 add_neurons=None  # [] number of added neurons for each layer -> add_neurons[idx] == number of  layer
                 ):

        if change_layers:
            if del_neurons is None:
                del_neurons = [None for _ in self.layers]
            elif len(del_neurons) != len(self.layers):
                logging.log(logging.ERROR, "del_neurons input is invalid!")
                raise ValueError(f"Expected a list of length {len(self.layers)=}"
                                 f", but got a list of length {len(del_neurons)}.")
            else:
                for idx, neuron_number in enumerate(del_neurons):
                    if neuron_number is not None:
                        self.connector_layout[idx + 1] -= len(neuron_number)

            if add_neurons is None:
                add_neurons = [None for _ in self.layers]
            elif len(add_neurons) != len(self.layers) - 1:  # Bc. last layer shouldnt be changed bc outputlayer
                logging.log(logging.ERROR, "add_neurons input is invalid!")
                raise ValueError(f"Expected a list of length {len(self.layers)=}"
                                 f", but got a list of length {len(add_neurons)}.")
            else:
                for idx, neuron_number in enumerate(add_neurons):
                    if neuron_number is not None:
                        self.connector_layout[idx + 1] += len(neuron_number)
                        if len(self.layers) - 1 > idx:
                            self.layers[idx + 1].number_of_pre_neurons += len(neuron_number)

            del_neurons.insert(0, None)
            add_neurons.insert(0, None)
            
            for idx, _ in enumerate(self.layers[:-1]):
                self.layers[idx].recreate(neuron_learn_probability=neuron_learn_probability,
                                          neuron_learn_rate=neuron_learn_rate,
                                          neuron_learn_rate_possibility=neuron_learn_rate_possibility,
                                          neuron_change_learn_rate=neuron_change_learn_rate,
                                          neuron_change_learn_rate_possibility=neuron_change_learn_rate_possibility,
                                          change_neurons=change_neurons,
                                          del_neurons=del_neurons[idx + 1],
                                          add_neuron=add_neurons[idx + 1],
                                          prev_del_neurons=del_neurons[idx],
                                          prev_add_neurons=add_neurons[idx])

        if add_layer is not None:
            for neurons in add_layer:
                self.add_layer(random.randint(0, len(self.layers) - 1), neurons)  # should only change the hidden layers
        
        elif del_layer > 0:
            for _ in range(del_layer):
                self.del_layer(random.randint(0, len(self.layers) - 2))  # should only change the hidden layers

    def add_layer(self, position, number_of_neurons):
        number_of_pre_neurons = self.layers[position].number_of_pre_neurons
        self.layers[position].reshape_neurons(number_of_pre_neurons=number_of_neurons)
        self.layers.insert(position, Layer(number_of_pre_neurons=number_of_pre_neurons,
                                           number_of_neurons=number_of_neurons))
        self.connector_layout.insert(position + 1, number_of_neurons)

    def del_layer(self, position):
        number_of_pre_neurons = self.layers[position].number_of_pre_neurons
        del self.layers[position]
        del self.connector_layout[position + 1]
        self.layers[position].reshape_neurons(number_of_pre_neurons=number_of_pre_neurons)

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
