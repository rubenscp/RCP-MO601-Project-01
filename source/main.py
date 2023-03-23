"""
Project: 01 - A super basic simulator of logical circuits 
Professor: Rodolfo Jardim de Azevedo
Student: Rubens de Castro Pereira
Date: 09/03/2023
Version: 1.0
"""

# ###########################################
# Importing Libraries
# ###########################################
import os
import pandas as pd
import csv 

from Circuit import Circuit


# ###########################################
# Defining variables, constants and objects
# ###########################################


# ###########################################
# Application Methods
# ###########################################

# Read the input data: logical circuit and its stimuli
def read_input_data(path, circuit_filename, stimuli_filename):

    # getting the logical circuit 
    df_circuit = pd.read_csv(path + circuit_filename, header=None, delimiter=' ', names=range(5))
    print()    
    print(f'circuit \n{df_circuit}')

    # getting the stimuli 
    df_stimuli = pd.read_csv(path + stimuli_filename, header=None, delimiter=' ', dtype=str)
    
    # preprocessing stimulus lines 
    lst_stimuli = df_stimuli.values.tolist()
    lst_stimuli_detailed = []
    for stimulus in lst_stimuli:
        if len(stimulus[0]) == 1:
            lst_stimuli_detailed.append(stimulus)
        else:
            if stimulus[0][:1] == '+':
                lst_stimuli_detailed.append(stimulus)
            else: 
                left = stimulus[0]
                right = stimulus[2]
                for i in range(len(stimulus[0])):
                    new_stimulus = [left[i], '=', right[i]]
                    lst_stimuli_detailed.append(new_stimulus)
                
    print() 
    print(f'stimuli \n{df_stimuli}')

    # returning logical circuit and stimuli
    return df_circuit, lst_stimuli_detailed

# Check if test has all necessary files to simulating the logical circuit 
def check_test_files(test, subtest_path):
    error = False 

    file = 'circuito.hdl'
    if not os.path.isfile(subtest_path + file):
        print(f'ERROR: File "{file}" does not exist in "{test}"')
        error = True 

    file = 'estimulos.txt'
    if not os.path.isfile(subtest_path + file):
        print(f'ERROR: File "{file}" does not exist in "{test}"')
        error = True 

    file = 'esperado0.csv'
    if not os.path.isfile(subtest_path + file):
        print(f'ERROR: File "{file}" does not exist in "{test}"')
        error = True 

    file = 'esperado1.csv'
    if not os.path.isfile(subtest_path + file):
        print(f'ERROR: File "{file}" does not exist in "{test}"')
        error = True 

    # printing result
    if not error:
        print(f'> Test files are ok.')
    # returning checking result 
    return error


# Process all steps of test 
def process_test(test, test_path):

    print()
    print(f'#'*50)
    print(f'Processing test "{test}"')
    print(f'#'*50)

    # setting subtest path 
    subtest_path = test_path + test + '/'

    # 1) checking test files 
    print()
    print(f'1) Checking test files')
    if check_test_files(test, subtest_path):
        return 

    x = 0

    # 2) Reading the input data
    print()
    print(f'2) Reading input data')
    df_circuit, lst_stimuli = read_input_data(subtest_path, "circuito.hdl", "estimulos.txt")
        
    # 3) Creating circuit object
    print()
    print(f'3) Creating logical circuit')
    circuit = Circuit(df_circuit)
    # circuit.show_variables()
    # circuit.show_components()

    # 4) Simulating the logical circuit 
    print()
    print(f'4) Simulating logical circuit')

    # running simulation with delay = 0
    circuit.run_simulation(lst_stimuli, circuit.DELAY_0)

    # running simulation with delay = 1
    # circuit.run_simulation(lst_stimuli, circuit.DELAY_1)


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/"
    test_path = root_path + 'test/'

    # processing each test case definied in the folder tests 
    tests = [f for f in os.listdir(test_path)]
    for test in tests:
        if test == 'desktop.ini': continue

        # processing test 
        process_test(test, test_path)


    print()
    print(f'End of Simulation')
