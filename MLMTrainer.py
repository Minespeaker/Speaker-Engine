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
NN Container:  1%
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
        
        out = self.func(tot)
        self.tmpvar = [inputs, out]
        
        return out
    
    def reset(self):
        self.tmpvar = [None, 0] # So if multiple nodes in the next layer call theres only 1 calculation
    
class mlm:
    # I'm gonna cry the node class was so easy this is insane
    def __init__(self, hidden_layers, layer_nodes, inputs, outputs, method=sigmoid):
        self.nodearray = []
        self.nodearray.append([node(i, [], method) for i in range (inputs)])
        for _ in range (hidden_layers):
            self.nodearray.append([node(None, self.nodearray[-1], method) for _ in range (layer_nodes)])
        self.nodearray.append([node(None, self.nodearray[-1], method) for _ in range (outputs)])
        
    def reset(self):
        for layer in self.nodearray:
            for n in layer:
                n.reset()