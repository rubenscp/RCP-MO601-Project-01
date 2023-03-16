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
    df_circuit = pd.read_csv(path + circuit_filename, header=None, delimiter=' ')
    print()    
    print(f'-'*30)
    print(f'circuit \n{df_circuit}')

    # getting the stimuli 
    df_stimuli = pd.read_csv(path + stimuli_filename, header=None, delimiter=' ')
    print() 
    print(f'-'*30)
    print(f'stimuli \n{df_stimuli}')

    # returning logical circuit and stimuli
    return df_circuit, df_stimuli


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/"
    test_path = root_path + 'test/'

    # 1) Reading the input data
    print()
    print(f'*'*50)
    print(f'1) Reading input data')
    print(f'*'*50)
    subtest_path = test_path + 'test_01/'
    df_circuit, df_stimuli = read_input_data(subtest_path, "circuito.hdl", "estimulos.txt")
    
    # 2) Creating circuit object
    print()
    print(f'*'*50)
    print(f'2) Creating the logical circuit')
    print(f'*'*50)
    circuit = Circuit(df_circuit)
    circuit.show_variables()
    circuit.show_components()

    # 3) Simulating the logical circuit 
    print()
    print(f'*'*50)
    print(f'3) Simulation of the logical circuit')
    print(f'*'*50)

    # running simulation 
    circuit.run_simulation(df_stimuli, circuit.DELAY_0)

    # running simulation 
    circuit.run_simulation(df_stimuli, circuit.DELAY_1)

    # 4) Reporting results
    # 
