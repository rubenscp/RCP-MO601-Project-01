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
def save_results(path, result_filename, results, test_name, test_description):
    
    # setting the output filename in csv format 
    output_filename_csv = path + result_filename + '.csv'

    # removing files to save if exists 
    if os.path.exists(output_filename_csv):
        os.remove(output_filename_csv)     

    # creating text file and saving results
    with open(output_filename_csv, 'w') as output_csv_file:
        for result in results:
            output_csv_file.write(result + '\n')

    # closing text file 
    output_csv_file.close()  

    # setting the output filename with test details  
    output_filename_details = path + result_filename + '_details.txt'

    # removing files to save if exists 
    if os.path.exists(output_filename_details):
        os.remove(output_filename_details)     

    # creating text file and saving results
    with open(output_filename_details, 'w') as output_details_file:
        output_details_file.write('Test name   : ' + test_name + '\n')
        output_details_file.write('Description : ' + test_description + '\n')

    # closing text file 
    output_details_file.close()  

# Process all steps of test 
def process_test(test_name, test_path, test_description):

    print()
    print(f'#'*50)
    print(f'Processing "{test_name} - {test_description}"')
    print(f'#'*50)

    # setting subtest path 
    subtest_path = test_path + test_name + '/'

    # 1) checking test files 
    print()
    print(f'1) Checking test files')
    if check_test_files(test_name, subtest_path):
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

    # saving results to "saida" text file 
    save_results(subtest_path, 'saida0', results, test_name, test_description)

    # running simulation with delay = 1
    results = circuit.run_simulation(lst_stimuli, circuit.DELAY_1)

    # saving results to "saida" text file 
    save_results(subtest_path, 'saida1', results, test_name, test_description)


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/"
    test_path = root_path + 'test/'

    # setting possible test folders
    simulate_test_folders = {'test_01' : [False, 'Sample of the Project 1 - one stimulus per line '], 
                             'test_02' : [False, 'Sample of the Project 1 - many stimulus per line '], 
                             'test_03' : [False, 'Sample from website https://www.makerhero.com/blog/circuitos-logicos-logica-booleana-em-cis/ '], 
                             'test_04' : [False, 'Flip-flop circuit - https://blog.pantuza.com/artigos/elementos-de-memoria-o-circuito-logico-flip-flop-d'], 
                             'test_05' : [True, 'Latch-SR tipo D - https://embarcados.com.br/latch/#Flip-Flop'], 
                             'test_06' : [True, 'test_06'], 
                             'test_07' : [True, 'test_07'], 
                             'test_08' : [True, 'test_08'], 
                             'test_09' : [True, 'test_09'], 
                             'test_10' : [True, 'test_10'], 
                             'test_11' : [True, 'test_11'], 
                             'test_12' : [True, 'test_12'], 
                             'test_13' : [True, 'test_13'], 
                             'test_14' : [True, 'test_14 '], 
                             'test_15' : [True, 'test_15 '], 
                             'test_16' : [True, 'test_16 '], 
                             'test_17' : [True, 'test_17 '], 
                             'test_18' : [True, 'test_18 '], 
                             'test_19' : [True, 'test_19 '], 
                             'test_20' : [True, 'test_20']
                            }

    # processing each test case definied in the folder tests 
    tests = [f for f in os.listdir(test_path)]
    for test in tests:
        xxx = test.find('zip')
        if test == 'desktop.ini' or test.find('zip') != -1: continue
        
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
