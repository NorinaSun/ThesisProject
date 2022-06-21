import numpy as np
import itertools
import random
import data_collection as data

class Mip:
    mip_id = itertools.count().next

    def __init__(self, num_vars, num_ieq):
        self.id = Mip.mip_id()
        self.num_vars = num_vars
        self.num_ieq = num_ieq 
        
        self.gen_objective_functions()
        self.gen_inequalities()

    def gen_lessthan_inequality(self):
        """
        Generates inequalities given a the number of variables to consider.

        Returns the lhs coefficients and rhs value.
        """
        sum_lhs = 0
        lhs_coef = []

        for i in range(1,self.num_vars+1):
                
            rand_integer = random.randint(1,11)
            sum_lhs += rand_integer
            lhs_coef.extend([rand_integer])
        
        rhs = round(sum_lhs*random.uniform(0.95,1.5))

        return (lhs_coef, rhs)

    def gen_inequalities(self):

        inequalities = []
        
        for ieq in range(self.num_ieq):
            inequality = {}
            lhs_coef, rhs = self.gen_lessthan_inequality()
            inequality['lhs_coef'] = lhs_coef
            inequality['rhs'] = rhs

        inequalities.append(inequality)

        self.inequalities = inequalities

    def gen_objective_functions(self, num_obj_functions=10, max_val = 15):
        """
        Generates a list of values the length of the given number of variables

        Optional parameter to specify the max value of 
        """
        obj_functions = []
        for i in range(num_obj_functions):
            obj_functions.append(random.choices(range(max_val),k=self.num_vars))
        
        self.obj_functions = obj_functions
    
    def write_mip(self):
        
        original_constraints = data.get_tbl('original_constraints','csv')
        objective_functions = data.get_tbl('objective_functions','csv')

        for ieq in self.inequalities:
            

    #     if __name__ == '__main__':
    # filename = 'items.csv'
    # items = [Items(100, 'iPhone 10', 'Mobiles'), Items(200, 'Lenovo', 'Laptops')
    #     , Items(300, 'Java in Action', 'Books'), Items(400, 'Python', 'Books')]
    # try:
    #     with open(filename, 'w', newline='') as f:
    #         writer = csv.writer(f)
    #         for item in items:
    #             writer.writerow([item.id, item.name, item.category])
    # except BaseException as e:
    #     print('BaseException:', filename)
    # else:
    #     print('Data has been loaded successfully !')

class Graph(Mip):
    """
    creating the graph i think i need for this

    num_nodes: int
    nodes: int
    edges: set
    degrees: array
    neighbours: dict of sets
    d: num dimensions node feature vector

    """
    def __init__(self,num_nodes,nodes,edges,d):


        self.num_nodes = num_nodes
        self.v = nodes
        self.e = edges
        self.a = np.zeros((nodes,nodes)) #adjacency matrix
        self.features = d
        
        
        #define dimensional feature vector


#lets try making a graph object



# class Graph:
#     """
#     Create a graph representation of a generate knapsack problem

#     """

#     def __init__(self, number_of_nodes, edges, degrees, neighbors):
#         self.number_of_nodes = number_of_nodes
#         self.edges = edges
#         #In graph theory, the degree (or valency) of a vertex of a graph is the number of edges that are incident to the vertex
#         self.degrees = degrees
#         self.neighbors = neighbors

    
#     def __len__(self):
#         return self.number_of_nodes

#     @staticmethod
#     def barbasi_albert(number_of_nodes, affinity, random):

#         """
#         diff between this and erdos_renyi is this creates a few nodes and then the rest are connected to those,
#         erdos_renyi create them all at once with equal prob of edge. Given our problem, I think this one makes more
#         sense bc the variable nodes will be highly connected to the constraints, but the constraints themselves are
#         not connected to each other.

#         Generate a Barabási-Albert random graph with a given edge probability.

#         Parameters
#         ----------
#         number_of_nodes : int
#             The number of nodes in the graph.
#         affinity : integer >= 1
#             The number of nodes each new node will be attached to, in the sampling scheme.
#         random : numpy.random.RandomState
#             A random number generator.

#         Returns
#         -------
#         Graph
#             The generated graph.

#         """

#         assert affinity >= 1 and affinity < number_of_nodes

#         edges = set()
#         degrees = np.zeros(number_of_nodes, dtype=int)
#         neighbors = {node: set() for node in range(number_of_nodes)}
#         for new_node in range(affinity, number_of_nodes):
#             # first node is connected to all previous ones (star-shape)
#             if new_node == affinity:
#                 neighborhood = np.arange(new_node)
#             # remaining nodes are picked stochastically
#             else:
#                 neighbor_prob = degrees[:new_node] / (2*len(edges))
#                 neighborhood = random.choice(new_node, affinity, replace=False, p=neighbor_prob)
#             for node in neighborhood:
#                 edges.add((node, new_node))
#                 degrees[node] += 1
#                 degrees[new_node] += 1
#                 neighbors[node].add(new_node)
#                 neighbors[new_node].add(node)

#         graph = Graph(number_of_nodes, edges, degrees, neighbors)
#         return graph

# testing the graph object
# rng = np.random.RandomState(0)
# test_obj = gen.Graph(5,10,2,3).barbasi_albert(5,2,rng)
        
