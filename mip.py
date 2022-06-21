import numpy as np
import itertools
import random
import data_collection as data

class Mip:
    mip_id = itertools.count().__next__

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

        for idx, ieq in enumerate(self.inequalities):
            data.write_row('original_constraints', [self.id, idx, ieq['lhs_coef'], ieq['rhs'],"<="])
        
        for idx, obj in enumerate(self.obj_functions):
            data.write_row('objective_functions', [idx, self.num_vars, obj])

