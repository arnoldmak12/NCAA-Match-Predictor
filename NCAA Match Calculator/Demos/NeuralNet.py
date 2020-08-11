import numpy as np
import copy as copy

class NeuralNet():
    def __init__(self, dimensions):
        self.neural_net = []
        self.dimensions = dimensions
        self.nodes = []

    #will return value between 0 and 1.
    def sigmoid(self, x):
        #boundary check to get rid of potential overflow. Little effect on training
        if x > 100:
            return .99999
        elif x < -100:
            return 0.00001
        return 1/(1 + np.exp(-x))

    #runs sigmoid on a layer of nodes. Used on output layer
    def sigmoid_layer(self, nodes):
        for i in range(len(nodes)):
            nodes[i] = self.sigmoid(nodes[i])
        return nodes

    #generates a randomized neural network according to the dimensions upon creation
    def generate_neural_net(self):
        self.neural_net = []
        for i in range(len(self.dimensions)-1):
            np.random.seed()
            self.neural_net.append(np.random.randn(self.dimensions[i], self.dimensions[i+1]))
        return self.neural_net

    #takes input info and propogates forward through the nn. Returns sigmoided output nodes
    def forward_prop(self, inputs):
        next_layer = inputs
        self.nodes = []
        self.nodes.append(np.array(next_layer))
        for i in range(len(self.dimensions)-1):
            next_layer = np.matmul(next_layer, self.neural_net[i])
            self.nodes.append(next_layer)
        return self.sigmoid_layer(next_layer)

    #takes costs of each output node and propogates backward through the nn
    def backward_prop(self, output_costs, training_rate):
        change = output_costs
        old_change = []
        start = len(self.dimensions)-2
        for i in range(len(self.dimensions)-1):
            #since we calc the next change before adjusting the weights, we need to create a deep copy of the current change
            old_change = copy.deepcopy(change)
            change = np.matmul(change, np.transpose(self.neural_net[start-i]))
            self.adjust_weights(old_change, start-i, training_rate)

    #adjusts weights by a fraction of the desired change
    def adjust_weights(self, change, layer, training_rate):
        for i in range(len(self.neural_net[layer])):
            for k in range(len(change)):
                sign = (-1,1) [self.nodes[layer][i]>0]
                self.neural_net[layer][i][k] = self.neural_net[layer][i][k] + change[k]*training_rate*sign
                
    #calculates cost of each output node based on the expected outcome
    def calculate_costs(self, outputs, expected_outputs):
        costs = []
        for i in range(len(outputs)):
            costs.append(expected_outputs[i] - outputs[i])
        return costs