"""network.py
~~~~~~~~~~~~~~
Stolen and modified from https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/src/network2.py

"""

#### Libraries
# Standard library
import json
import random

# Third-party libraries
import numpy as np

#### Main Network class
class Network():

    def __init__(self, sizes, weights=None):
        """The list ``sizes`` contains the number of neurons in the respective
        layers of the network.  For example, if the list was [2, 3, 1]
        then it would be a three-layer network, with the first layer
        containing 2 neurons, the second layer 3 neurons, and the
        third layer 1 neuron.

        If no ``weights`` are provided they will be generated randomly.

        """
        self.num_layers = len(sizes)
        self.sizes = sizes

        """Initialize each weight using a Gaussian distribution with mean 0
        and standard deviation 1 over the square root of the number of
        weights connecting to the same neuron.  Initialize the biases
        using a Gaussian distribution with mean 0 and standard
        deviation 1.

        Note that the first layer is assumed to be an input layer, and
        by convention we won't set any biases for those neurons, since
        biases are only ever used in computing the outputs from later
        layers.

        """
        # self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]] # omit using a bias for now
        if weights is None:
            self.weights = [np.random.randn(y, x)/np.sqrt(x) 
                            for x, y in zip(self.sizes[:-1], self.sizes[1:])]
        else:
            self.weights = weights

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        # for b, w in zip(self.biases, self.weights): # omit using a bias for now
        #     a = sigmoid_vec(np.dot(w, a)+b)
        for w in self.weights:
            a = sigmoid_vec(np.dot(w, a))
        return a

    def save_to_file(self, filename):
        """Save the neural network to the file ``filename``."""
        data = {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights]}
                # "biases": [b.tolist() for b in self.biases] # omit using a bias for now
        f = open(filename, "w")
        json.dump(data, f)
        f.close()


#### Loading a Network
def load_from_file(filename):
    """Load a neural network from the file ``filename``.  Returns an
    instance of Network.
    """
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    net = Network(data["sizes"])
    net.weights = [np.array(w) for w in data["weights"]]
    # net.biases = [np.array(b) for b in data["biases"]] # omit using a bias for now
    return net


#### Genetic algorithm related
def crossover_breed(mom, dad):
    """ return a new child as breed from parents using crossover """
    if mom.sizes != dad.sizes:
        raise IndexError("Sizes of parents must be the same")

    new_weights = []
    # interate over wegihts between each layer
    for l in range(len(mom.weights)):
        # make a deep copy of the weight matrix between these layers. TODO - find a better way
        new_weights.append(np.empty_like(mom.weights[l]))
        new_weights[l][:] = mom.weights[l]
        # iterate over each weight
        for i, w in np.ndenumerate(dad.weights[l]):
            if random.random() < .02: # 2% chance that we will mutate
                new_weights[l][(i)] = np.random.randn()
            elif random.random() > .5: # 50% chance that we will take a weight from the dad
                new_weights[l][(i)] = w

    return Network(mom.sizes, new_weights)


#### Miscellaneous functions
def sigmoid(z):
    """ The sigmoid function """
    return 1.0/(1.0+np.exp(-z))

sigmoid_vec = np.vectorize(sigmoid)
