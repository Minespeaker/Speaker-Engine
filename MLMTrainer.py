"""
Game plan:
    Class node:  Take all weights from previous nodes (as inputs)
    Class mlm:   Core functionality
    Class train: Train the actual MLM
"""

import random
import math
import copy

"""
The actual NN: 90%
NN Container:  100%
NN Trainer:    0%
"""

# Sigmoid and ReLu are both functions that are applied to NN nodes

def sigmoid(z):
    """
    Turn any number to a 0-1 number
    The further into the negatives the closer it is to 0
    The further into the positives the closer it is to 1
    """
    try:
        out = 1/(1+(math.e**-z))
    except OverflowError: # Breaks at -710  or lower
        out = 0
    return out

def relu(z):
    """
    floors any number to be 0 if in the negatives
    """
    
    return max(z, 0)


class node:
    
    def __init__(self, start_node, previous_nodes, method=sigmoid):
        # There may be issues if incompatible variables are handed off
        # But thats what the mlm class is for, keeping things in check
        """
        Args:
            start_node: int/None
                if None then not a start node, else index of node (0-based)
            
            previous_nodes: list
                node obj's of previous layer in index order
                
            method: function
                either sigmoid or ReLu, or a self built function if you're feeling like it
        """
        
        if start_node is None:
            self.prevnodes = previous_nodes
            self.nodeweight = [random.gauss(0, 0.5) for _ in range (len(previous_nodes))]
            self.bias = random.gauss(0, 0.5)
        else:
            self.prevnodes = [] # No prevnodes to prevent issues arising with mlm giving prevnodes to input nodes
            self.nodeweight = []
            self.bias = 0
        self.func = method
        self.input = start_node
        self.reset()
        
    def calculate(self, inputs) -> float:
        if self.input is not None:
            return inputs[self.input]
        if self.tmpvar[0] == inputs:
            return self.tmpvar[1]
        tot = 0
        for innode in range (len(self.prevnodes)):
            nodeout = self.prevnodes[innode].calculate(inputs)
            weightout = nodeout*self.nodeweight[innode]
            tot += weightout
        
        out = self.func(tot+self.bias)
        self.tmpvar = [inputs, out]
        
        return out
    
    def reset(self):
        self.tmpvar = [None, 0] # So if multiple nodes in the next layer call theres only 1 calculation
    
class mlm:
    def __init__(self, hidden_layers, layer_nodes, inputs, outputs, method=sigmoid):
        self.nodearray = [] # NN Array
        self.nodearray.append([node(i, [], method) for i in range (inputs)]) # Input nodes
        self.hiddenlayercount = hidden_layers
        self.nodesperlayer = layer_nodes
        for _ in range (self.hiddenlayercount):
            self.nodearray.append([node(None, self.nodearray[-1], method) for _ in range (self.nodesperlayer)]) # Hidden nodes
        self.nodearray.append([node(None, self.nodearray[-1], method) for _ in range (outputs)]) # Output nodes
        
    def reset(self):
        """
        Empty NN cache
        """
        
        for layer in self.nodearray:
            for n in layer:
                n.reset()
        
    def forward(self, inputs):
        outputs = []
        for n in self.nodearray[-1]:
            outputs.append(n.calculate(inputs))
            
        self.reset()
        
        return outputs
    
    def copy(self):
        return copy.deepcopy(self)




class train:
    def from_nn(neural_network, population, testing_quantity, survivors, generations, accuracy, training_data):
        """
        Args:
            _: stand-in for self
            
            neural_network: mlm class to train from
            
            population: how many mutations per generation
            
            testing_quantity: how many points from the dataset to test the mlm on. more means better mlm judgement, lower means faster mlm running
            
            survivors: how many mlms can survive each generation. too low means not enough mutation variety and won't train properly, too high means bad mutations will survive and contaminate the next generation.
            
            generations: how many generations to train for. Set to -1 to use accuracy
            
            accuracy: what percent acurate the mlm must be on avarage to finish training
            
            training_data: the data to train the mlm off of. form must be list of tuples, first item in tuple list of inputs, second a list of outputs. must be all floats or ints
        """
        
        nn = neural_network
        
        gen = [nn.copy()]
        
        training = True
        while training:
            # create a new population
            
            for _ in range(population-1):
                gen.append(gen[0].copy())
                ran1 = random.randint(1, gen[-1].hiddenlayercount+1)
                ran2 = random.randint(0, len(gen[-1].nodearray[ran1])-1)
                tmp = gen[-1].nodearray[ran1][ran2].nodeweight
                ran3 = random.randint(0, len(tmp)-1)
                tmp[ran3] += random.gauss(0, 0.25)
                
            # Run all the mlms
            
            outputs = []
            for _ in range (testing_quantity):
                random_data = training_data[random.randint(0, len(training_data)-1)]
                
                inputs, expected_outputs = random_data
                
                outputs.append(([mutation.forward(inputs) for mutation in gen], expected_outputs))
            
            # Evaluate error
            
            err = []
            firstloop = True
            for trueOut, wantOut in outputs:
                for loop, mutationOutput in enumerate(trueOut):
                    diff = []
                    for idx in range (len(mutationOutput)):
                        diff.append(abs(mutationOutput[idx]-wantOut[idx]))
                    if firstloop:
                        err.append([sum(diff)])
                    else:
                        err[loop].append(sum(diff))
                        
                firstloop = False
                
            # Filter for survivors
            
            err = [(tmp, n) for n, tmp in enumerate(err)]
            
            sort = []
            for _ in err:
                sort.append((-1, 0))
                for error, source in err:
                    error2, _ = sort[-1]
                    if sum(error) < error2 or error2 == -1:
                        sort[-1] = (sum(error), source)