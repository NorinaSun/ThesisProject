import numpy as np
import itertools
import random
import data_collection as data
import mip

class Graph(mip.Mip):
    """
    creating the graph i think i need for this
    num_nodes: int
    nodes: int
    edges: set
    degrees: array
    neighbours: dict of sets
    d: num dimensions node feature vector

    """
    def __init__(self, num_vars, num_ieq, d):
        super().__init__(num_vars, num_ieq)

        self.num_nodes = len(self.inequalities) + self.num_vars
        self.d = d
        self.adj_matrix = []

        self.generate_adjacency_matrix()
    
    def generate_adjacency_matrix(self):

        #variable nodes
        for idx in range(self.num_vars):
            self.adj_matrix.append([0]*self.num_vars + [ieq['lhs_coef'][idx] for ieq in self.inequalities])

        #inequality nodes
        self.adj_matrix.append([dict['lhs_coef']+[0]*self.num_ieq for dict in self.inequalities])
        
    