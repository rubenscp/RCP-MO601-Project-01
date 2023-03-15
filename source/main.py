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

    print()
    print(f'Reading input data')

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

# Simulating run of the logical circuit 
def run_simulation(circuit, df_stimuli, delay):
    
    # runing the stimuli input 
    stimuli = df_stimuli.values.tolist()
    for stimulus in stimuli:       
        print(stimulus)
        token = stimulus[0]
        if circuit.isVariable(token):
            circuit.set_input_signal(token, int(stimulus[2]))
            circuit.set_output_signal(token, int(stimulus[2]))
            continue
        else:
            # getting time indicator
            time_indicator = circuit.get_time(token)

            # run cycles of the circuit 
            circuit.run_cycles(time_indicator)
            x = 0      

        # show current configuration of the circuit variables 
        circuit.show_variables()


    # run cycles of the circuit for the last time
    circuit.run_cycles(time_indicator)
    x = 0      
    
    # printing execution output 
    circuit.show_final_output()


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/"
    test_path = root_path + 'test/'

    # 1) Reading the input data
    subtest_path = test_path + 'test_01/'
    df_circuit, df_stimuli = read_input_data(subtest_path, "circuito.hdl", "estimulos.txt")
    
    # 2) Creating circuit object
    circuit = Circuit(df_circuit)
    circuit.show_variables()
    circuit.show_components()

    # circuit.set_input_signal('C', circuit.ONE)
    # circuit.set_output_signal('D', circuit.ONE)

    # result = circuit.get_variable_signal('A', 'output')
    # result1 = circuit.get_variable_signal('C', 'input')
    # x = 0

    # circuit.set_output_signal('B', circuit.ONE)
    # circuit.set_output_signal('C', circuit.ONE)
    # circuit.show()
    # result3 = circuit.operation_AND(circuit.get_variable_signal('B', 'output'), circuit.get_variable_signal('C', 'output'))
    # print(f'-'*30)
    # result3 = circuit.operation_OR(circuit.get_variable_signal('B', 'output'), circuit.get_variable_signal('C', 'output'))
    # print(f'-'*30)
    # result3 = circuit.operation_NOT(circuit.get_variable_signal('B', 'output'))
    # print(f'-'*30)
    # result3 = circuit.operation_NAND(circuit.get_variable_signal('B', 'output'), circuit.get_variable_signal('C', 'output'))
    # print(f'-'*30)
    # result3 = circuit.operation_NOR(circuit.get_variable_signal('B', 'output'), circuit.get_variable_signal('C', 'output'))
    # print(f'-'*30)
    # result3 = circuit.operation_XOR(circuit.get_variable_signal('B', 'output'), circuit.get_variable_signal('C', 'output'))
    # print(f'-'*30)
    # x = 0

    # 3) Simulating circuit with input data 
    run_simulation(circuit, df_stimuli, circuit.DELAY_0)

    # 4) Reporting results

    x = 0

    # inst = HelloWorld()
    # inst.run_sim(3000)

    # a = intbv(24)
    # print(f'-'*30)
    # print(a)
    # print(a.min)
    # print(a.max)
    # print(f'-'*30)