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
    Basically floors any number to be 0 if in the negatives
    """
    
    return max(z, 0)


class node():
    
    def __init__(self, start_node=bool, previous_nodes=[]):
        self.state = 0 # What the current state of the node is
        self.eff = 0.5 # How much it effects the state when passed on
        self.prevnodes = previous_nodes