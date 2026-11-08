"""
Game plan:
    Class node:  Take all weights from previous nodes (as inputs)
    Class mlm:   Core functionality
    Class train: Train the aactual MLM
"""

import random
import math

# Sigmoid and ReLu are both functions that are applied to NN nodes

def sigmoid(z):
    """
    Turn any number to a 0-1 number
    The further into the negatives the closer it is to 0
    The further into the positives the closer it is to 1
    """
    
    return 1/(1+(math.e**-z))

def relu(z):
    """
    floors any number to be 0 if in the negatives
    """
    
    return max(z, 0)


class node():
    
    def __init__(self, start_node, previous_nodes=[], method=sigmoid):
        """
        Args:
            start_node: int
                if 0 then not a start node, else index of node
            
            previous_nodes: list
                node obj's of previous layer in index order
                
            method: function
                either sigmoid or ReLu, or a self built function if you're feeling like it
        """
        
        self.state = 0 # What the current state of the node is
        self.prevnodes = previous_nodes
        self.nodeweight = [1 for _ in range (len(previous_nodes))]
        self.func = method
        self.input = start_node
        self.tmpvar = ()
        
    def calculate(self, inputs=[]) -> float:
        if self.input != 0:
            return inputs[self.input-1]
        else:
            sum = 0
            for node in range (len(self.prevnodes)):
                nodeout = self.prevnodes[node].calculate(inputs)
                weightout = nodeout*self.nodeweight[node]
                sum += weightout

        return self.func(sum)