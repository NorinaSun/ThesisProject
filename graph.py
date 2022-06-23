import numpy as np
import itertools
import random
import torch
import data_collection as data
import mip


class Graph(mip.Mip):
    """
    creating the graph i think i need for this
    n: int, number of variable nodes + constraint nodes
    nodes: set
    edges: set
    A: matrix, adjacency matrix
    U: matrix, feature matrix, nodes as rows
    degrees: array
    neighbours: dict of sets
    d: num dimensions node feature vector

    #todo
    https://stackoverflow.com/questions/55800218/setting-default-empty-attributes-for-user-classes-in-init

    # i think we should include the RHS as one of the nodes

    """
    def __init__(self, num_vars, num_ieq, d):
        super().__init__(num_vars, num_ieq)

        self.num_nodes = len(self.inequalities) + self.num_vars + 1
        self.d = d
        self.adj_matrix = []
        self.feature_matrix = []

        self.generate_adjacency_matrix()
        self.generate_feature_matrix()

    def generate_adjacency_matrix(self):

        #variable nodes
        for idx in range(self.num_vars):
            self.adj_matrix.append([0]*self.num_vars + [ieq['lhs_coef'][idx] for ieq in self.inequalities] + [0])

        #inequality nodes
        self.adj_matrix.extend([ieq['lhs_coef']+[0]*self.num_ieq + [ieq['rhs']] for ieq in self.inequalities])

        #rhs node
        self.adj_matrix.append([0]*self.num_vars + [ieq['rhs'] for ieq in self.inequalities] + [0])

        #replace A_ii with 1
        self.adj_tensor = torch.tensor(self.adj_matrix)

        
    def generate_feature_matrix(self):
        np.zeros((self.num_nodes,self.d))
