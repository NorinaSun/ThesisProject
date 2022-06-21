from xml.dom.minicompat import NodeList
import numpy as np
import itertools
import random



class Mip:
    mip_id = itertools.count().next

    def __init__(self, num_vars, num_ieq):
        self.id = Mip.mip_id()
        self.num_vars = num_vars
        self.num_ieq = num_ieq

    def set

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

    def gen_objective_functions(self, max_val = 15):
        """
        Generates a list of values the length of the given number of variables

        Optional parameter to specify the max value of 
        """
        

        return random.choices(range(max_val),k=self.num_vars)
    
    def gen_inequalities(self):

        inequalities = []
        
        for ieq in range(self.num_ieq):
            inequality = {}
            lhs_coef, rhs = self.gen_lessthan_inequality()
            inequality['lhs_coef'] = lhs_coef
            inequality['rhs'] = rhs

        inequalities.append(inequality)

        self.inequalities = inequalities

class PortaMip(Mip):

    def __init__(self):
        self.filename
        self.file
        self.file_num

    def init_ieq_file(self):

        ieq_f = open('ieq_%s.ieq' % self.id,"w")

        ieq_f.write("DIM = %s \n \n" % self.num_vars)
        ieq_f.write("VALID \n")
        valid = self.num_vars*'0 '
        ieq_f.write("%s \n \n" % valid)
        ieq_f.write("LOWER_BOUNDS \n")
        lower_bound = self.num_vars*'0 '
        ieq_f.write("%s \n \n" % lower_bound)
        ieq_f.write("UPPER_BOUNDS \n")
        upper_bound = self.num_vars*'1 '
        ieq_f.write("%s \n \n" % upper_bound)
        ieq_f.write("INEQUALITIES_SECTION \n")
        
        return ieq_f
    
    def add_ieq_inequalities(self,file,inequality):

        file.write(f"{inequality}" + "\n")
    
    def end_ieq_file(self, file):
    
        for i in range(1,self.num_vars+1):
            file.write('x%s <= 1 \n' % i)
            file.write('x%s >= 0 \n' % i)

        file.write("\nEND \n")
        file.close()

    def create_poi_file(self, file_num, int_points):

        poi_f = open('poi_%s.poi' % file_num,"w+")
        
        poi_f.write("DIM = %s \n \n" % self.num_vars)
        poi_f.write("CONV_SECTION \n")
        
        for point in int_points:
            print(*point, sep =' ', file = poi_f)

        poi_f.write("\nEND \n")
        poi_f.write("DIMENSION OF THE POLYHEDRON : %s \n \n" % self.num_vars )

        poi_f.close()
    
    def get_porta_constraints(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        
        list_results = []

        for i in lines:

            #take inequality columns only
            if "(" in i:
                #extract string values
                value_str  = i.translate(str.maketrans("","", "()\n"))
                value_list = list(value_str.split())[1:]
                
                #check if vars were sticky
                for val in value_list:
                    if val.count("x") > 1:

                        split_list = re.split(r'([+-])',val)
                        split_list.remove('')

                        i = 0
                        while i <= val.count("x"): #2
                            split_var = split_list[i] + split_list[i+1]
                            value_list.insert(int(i/2),split_var)
                            i += 2

                        value_list.remove(val)

                #extract the coefficients
                rhs_list = [ x for x in value_list if "x" in x ]
                coefficient_list = []

                for var in range(1,self.num_vars+1):
                    coefficient = 0

                    for val in rhs_list:
                        if f'x{var}' in val:
                            coefficient = int(float(val.replace(f'-x{var}', '-1').replace(f'+x{var}', '1').replace(f'x{var}', '')))
                            break
                    
                    coefficient_list.append(coefficient)

                for val in value_list:

                    if '<=' in val:
                        inequality = '<='
                    elif 'x' not in val and '=' not in val:
                        rhs = val

                inequality_dict = {'coef': coefficient_list, 'rhs': rhs, 'inequality': inequality}

                list_results.append(inequality_dict)

        return list_results
    
    def get_integer_points(self, filename):

        with open('%s.poi' % filename) as f:
            lines = f.readlines()

        list_results = []

        for i in lines:

            if "(" in i and "/" not in i:

                value_str  = i.translate(str.maketrans("","", "()\n"))
                value_list = list(value_str.split())
                list_results.append(value_list[1:])

        return list_results
            


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
        
