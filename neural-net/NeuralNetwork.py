from enum import auto, Enum, unique
import pickle

import numpy as np


@unique
class ActFuncs(Enum):
    SIGMOID = auto()
    TANH = auto()
    RELU = auto()

    @staticmethod
    def _gen_sigmoid():
        sig = lambda x: 1 / (1.0 + np.exp(-x))
        def sig_deriv(x):
            k = 1 / (1.0 + np.exp(-x))
            return k * (1 - k)
        return sig, sig_deriv

    @staticmethod
    def _gen_tanh():
        tn_deriv = lambda x: 1.0 - np.tanh(x) ** 2
        return np.tanh, tn_deriv

    @staticmethod
    def _gen_relu():
        rl = lambda x: x * (x > 0)
        rl_deriv = lambda x: 1.0 * (x > 0)
        return rl, rl_deriv

    @staticmethod
    def get_act_funcs(act):
        return {
            self.SIGMOID: self._gen_sigmoid,
            self.TANH: self._gen_tanh,
            self.RELU: self._gen_relu,
        }[act]()


class NeuralNetwork:

    def __init__(self, input_size, output_size, hidden_layers, act=ActFuncs.SIGMOID):
        self.num_layers = len(hidden_layers) + 2
        self.layer_sizes = [input_size] + hidden_layers + [output_size]
        self.act = act
        self.f_act, self.f_act_diff = ActFuncs.get_act_funcs(self.act)
        self.weights = [
            np.random.randn(i, j)
            for i, j in
            zip(self.layer_sizes, self.layer_sizes[1:])
        ]

    def __str__(self):
        print("+--------- Neural Net Info -----------+")
        print("+ Layer Sizes:", self.layer_sizes)
        print("+ Activation Func:", self.act)
        print(
            "+ Total Layer Count:", self.num_layers,
            " |  Total Neuron Count:", sum(self.layer_sizes[1:]),
        )
        print("+-------------------------------------+")

    def save(self, name):
        with open(name, "wb") as f:
            pickle.dump(self, f, -1)

    @staticmethod
    def load(name):
        with open(name, "rb") as f:
            return pickle.load(f)

    def feed_forward(self, x)
        for W in self.weights:
            z = np.dot(x, W)
            x = self.f_act(z)
        return x

    def cost_func(self, x, expected_output):
        output = self.feed_forward(x)
        return 0.5 * np.sum((expected_output - output) ** 2)

    def backprop(self, x, expected_output, learn_rate):
        a = [x]


        err = output - expected_output
        for i in self.layer_sizes[1 : -1]:
            delta = err * self.f_act_diff()

    def backprop(self, trainingInput, trainingOutput, learn_rate):
        output = self.feedForward(trainingInput)
        err = output - trainingOutput
        dJdW = []
        for k in range(1, self.hiddenLayerCount + 1):
            delta = err * self.activationFuncDeriv(self.z[-k])
            dJdW.append(np.dot(self.a[-k - 1].T, delta))
            err = np.dot(delta, self.synapseWeights[-k].T)
        for k in range(1, self.hiddenLayerCount + 1):
            self.synapseWeights[-k] -= learn_rate * dJdW[k - 1]
        return self.costFunction(trainingInput, trainingOutput)

    def train(
        self, trainingInput, trainingOutput, learn_rate, iterations, callback=None
    ):
        costs = [self.costFunction(trainingInput, trainingOutput)]
        for i in range(iterations):
            cost = self.backprop(trainingInput, trainingOutput, learn_rate)
            if callback:
                callback(cost, self)
            costs.append(cost)
        return costs


"""
class GeneticNetworkPool:

    def __init__(self, neural_network, gene_pool_size, evaluator):
        self.nn = neural_network
        self.pool_size = gene_pool_size
        self.pool = []
        self.evaluator = evaluator
        self.scores = []

        self.randomize_pool()

    def randomize_pool(self):
        allLayers = np.concatenate(([self.nn.inputLayerSize], self.nn.hiddenLayersSizes, [self.nn.outputLayerSize]))
        self.pool = []
        for i in range(self.pool_size):
            weights = []
            for i in range(self.nn.hiddenLayerCount + 1):
                weights.append(
                    1 * np.random.randn(allLayers[i], allLayers[i + 1]) + 0
                )
            self.pool.append(weights)

    def evaluate_all(self):
        self.scores = []
        for gene in self.pool:
            self.nn.synapseWeights = gene
            self.scores.append(self.evaluator(self.nn))
        return self.scores

    def feed_forward_all(self, input_array):
        outputs = []
        for gene in self.pool:
            self.nn.synapseWeights = gene
            outputs.append(self.nn.feedForward(input_array))
        return outputs
"""