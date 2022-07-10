import graph
import data_collection as data
import mip


def run_program(min_vars, max_vars, num_models, num_obj_func):

    #init the data files
    data.init_tables()

    #generate the mips
    for num_vars in range(min_vars, max_vars+1):
        for model in range(num_models):
            mip.Mip(num_vars)



if __name__ == "__main__":

    min_vars = int(input("Enter the minimum number of variables you want in your models:  "))

    max_vars = int(input("Enter the maximum number of variables you want in your models:  "))

    num_models = int(input("Enter the number of models you would like to generate per variable number:  "))

    num_obj_func = int(input("Enter the number of objective functions you would like to test each model with:  "))

    run_program(min_vars, max_vars, num_models, num_obj_func)