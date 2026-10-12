import math, random

class mlm:
    def __init__(self, name, inputs, outputs):
        """
        Initialise the MLM
        """
        self.name = name
        self.network = []
        self.inputs = inputs
        self.outputs = outputs
    
    def gen(self, hidden_layers, nodes_per_layer, random_per_node=False):
        """
        generates a neural network for the MLM
        """
        self.network = [[random.randint(-1000, 1000)/1000 if random_per_node else 0 for _ in range (nodes_per_layer)] for _ in range (hidden_layers)]
        
        self.network.insert(0, [0 for _ in range (self.inputs)])
        self.network.append([0 for _ in range (self.outputs)])
        
        self.connect = [[[random.randint(500, 2000)/1000 if random_per_node else 1 for _ in range (nodes_per_layer)] for _ in range (nodes_per_layer)] for _ in range (hidden_layers+1)]
        #                                                                                                                                                             First dimension is start layer
        #                                                                                                                           Second Dimension is start node
        #                                                                                        Third dimension is end node
                
    def run(self, args):
        """
        run the MLM
        """
        
        x = 0
        for i in args:
            self.network[0][x] = min(max(i, -1), 1)
            x += 1
        
        for layer in range (self.network.__len__()):
            start = self.network[layer]
            end = self.network[layer+1]
            
            cnct = []
            for sl in self.network[layer]:
                for sn in sl:
                    cnct.append([])
                    for en in sl:
                        cnct[-1].append()