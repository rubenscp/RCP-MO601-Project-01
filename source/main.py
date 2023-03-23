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


# Save results of simulation
def save_results(path, result_filename, results):
    
    # removing files to save if exists 
    if os.path.exists(path + result_filename):
        os.remove(path + result_filename)     

    # saving results into csv file 
    df = pd.DataFrame(results)
    print(df)
    # df.to_csv(path + result_filename, index=False, header=False, doublequote=False)
    # df.to_csv(path + result_filename, index=False, header=False, quotechar=" ")
    # df.to_csv(path + result_filename, index=False, header=False, quoting=3, sep=",", escapechar="")
    # df.to_csv(path + result_filename, index=False, header=False, quoting=3, sep=",", escapechar=",")
    x = 0

    # my_file = open(path + result_filename, 'w+', newline = '')
    # with open(path + result_filename, 'w') as output:
    #     output.write(str(results))
        
    with open(path + result_filename, 'w') as output:
        for result in results:
            print(result)
            # lines = df.to_string(header=False, index=False)
            output.write(result + '\n')
    output.close()  

# Process all steps of test 
def process_test(test, test_path, test_name):

    print()
    print(f'#'*50)
    print(f'Processing "{test} - {test_name}"')
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
    results = circuit.run_simulation(lst_stimuli, circuit.DELAY_0)
    save_results(subtest_path, 'saida0.csv', results)
    x = 0

    # running simulation with delay = 1
    results = circuit.run_simulation(lst_stimuli, circuit.DELAY_1)
    save_results(subtest_path, 'saida1.csv', results)
    x = 0


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/"
    test_path = root_path + 'test/'

    # setting possible test folders
    simulate_test_folders = {'test_01' : [True, 'Sample of the Project 1 - one stimulus per line '], 
                             'test_02' : [True, 'Sample of the Project 1 - many stimulus per line '], 
                             'test_03' : [True, 'Sample from website https://www.makerhero.com/blog/circuitos-logicos-logica-booleana-em-cis/ '], 
                             'test_04' : [True, 'Flip-flop circuit - https://blog.pantuza.com/artigos/elementos-de-memoria-o-circuito-logico-flip-flop-d'], 
                             'test_05' : [False, 'test '], 
                             'test_06' : [False, 'test '], 
                             'test_07' : [False, 'test '], 
                             'test_08' : [False, 'test '], 
                             'test_09' : [False, 'test '], 
                             'test_10' : [False, 'test '], 
                             'test_11' : [False, 'test '], 
                             'test_12' : [False, 'test '], 
                             'test_13' : [False, 'test '], 
                             'test_14' : [False, 'test '], 
                             'test_15' : [False, 'test '], 
                             'test_16' : [False, 'test '], 
                             'test_17' : [False, 'test '], 
                             'test_18' : [False, 'test '], 
                             'test_19' : [False, 'test '], 
                             'test_20' : ['test ', False ]
                            }

    # processing each test case definied in the folder tests 
    tests = [f for f in os.listdir(test_path)]
    for test in tests:
        if test == 'desktop.ini': continue
        
        if not simulate_test_folders[test][0]: 
            print()
            print(f'{test} - {simulate_test_folders[test][1].strip()} isn\'t able to simulate.')
            print()            
            continue

        # processing test 
        test_name = simulate_test_folders[test][1].strip()
        process_test(test, test_path, test_name)


    print()
    print(f'End of Simulation')
    print()
