import itertools
import random
import data_collection as data
import logging

class Mip:
    mip_id = itertools.count().__next__

    def __init__(self, num_vars, num_ieq=2):
        self.id = Mip.mip_id()
        self.num_vars = num_vars
        self.num_ieq = num_ieq 
        self.inequalities = []
        self.obj_functions = []
        
        self.gen_objective_functions()
        self.gen_inequalities()
        self.write_mip()

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
        
        for ieq in range(self.num_ieq):
            inequality = {}
            lhs_coef, rhs = self.gen_lessthan_inequality()
            inequality['lhs_coef'] = lhs_coef
            inequality['rhs'] = rhs
            self.inequalities.append(inequality)
        
        return self.inequalities

    def gen_objective_functions(self, num_obj_functions=10, max_val = 15):
        """
        Generates a list of values the length of the given number of variables

        Optional parameter to specify the max value of 
        """
        for i in range(num_obj_functions):
            self.obj_functions.append(random.choices(range(max_val),k=self.num_vars))
        
        return self.obj_functions
    
    
    def write_mip(self):

        for idx, ieq in enumerate(self.inequalities):
            try:
                data.write_row('original_constraints', [self.id, idx, ieq['lhs_coef'], ieq['rhs'],"<="])
            except Exception as e:
                logging.error("Unable to write MIP to original_constraints file")
        
        for idx, obj in enumerate(self.obj_functions):
            try:
                data.write_row('objective_functions', [idx, self.num_vars, obj])
            except Exception as e:
                logging.error("Unable to write MIP to objective_functions file")

