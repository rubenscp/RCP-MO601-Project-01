import string
import numpy as np
import math 

class Circuit:

    def __init__(self, df_circuit):
        # constants values 
        self.ONE = 1
        self.ZERO = 0
        self.DELAY_0 = 0
        self.DELAY_1 = 1

        # class attributes - variables
        self.variables = {}
        self.components = {}
        self.components_execution_sequence = []
        self.outputs = []
        self.last_output = ''
        self.penultimate_output = ''

        # variables list of the circuit
        for letter in string.ascii_uppercase:
            self.variables[letter] = [{'actual' : 0, 'future' : 0}]
        
        # building circuit components
        list = df_circuit.values.tolist()
        for item in list:
            self.components[item[0]] = [{'operation' : item[2], 
                                         'first_variable' : item[3], 
                                         'second_variable' : item[4],
                                         'priority' : 0}
                                         ]


        # setting components priority to run
        self.define_priority_of_components()

    # initializing working circuit objects 
    def initialize_working_circuit_objects(self):
        self.outputs = []
        self.last_output = ''
        self.penultimate_output = ''
        for variable in self.variables:
            self.set_actual_signal(variable, 0)
            self.set_future_signal(variable, 0)

    # defining the priority of the circuit components
    def define_priority_of_components(self):
        # initializing priority indicator 
        priority_indicator = 0

        # defining priority of the circuit components
        end = False
        while not end:

            set_priority = False 

            for component, component_value in self.components.items():
                # checking if item already priority 
                if component_value[0]['priority'] > 0:
                    continue

                first_variable = component_value[0].get('first_variable')
                if (self.is_future_of_component(first_variable)     and 
                    not self.has_priority(first_variable)
                    ):
                    end = False
                    continue

                second_variable = component_value[0].get('second_variable')
                if (second_variable != None                         and
                    self.is_future_of_component(second_variable)    and 
                    not self.has_priority(second_variable)
                    ):
                    end = False
                    continue

                # setting priority indicator in the component
                priority_indicator = priority_indicator + 1
                component_value[0].update({'priority' : priority_indicator})
                set_priority = True             
             
            if not set_priority:
                end = True 

        # defining the execution sequence of the components
        list = []
        for component, component_value in self.components.items():
            list.append([component_value[0].get('priority'), component])
               
        self.components_execution_sequence.clear
        # self.components_execution_sequence = sorted(list)
        self.components_execution_sequence = list
        x = 0

    # checking if the varibale is future of some of circuit component
    def has_priority(self, variable):
        return True if self.components.get(variable)[0].get('priority') > 0 else False
        
    # checking if component has setted priority
    def is_future_of_component(self, variable):
        return True if self.components.get(variable) != None else False

    # getting the signal value of the variable actual 
    def get_variable_signal(self, variable, actual_or_future): 
        if variable is np.nan:
            return None
        return self.variables.get(variable)[0].get(actual_or_future)
    
    # setting signal value in the variable actual 
    def set_actual_signal(self, variable, signal_value):
        (self.variables[variable])[0].update({'actual' : signal_value})
        
    # setting signal value in the variable future 
    def set_future_signal(self, variable, signal_value):
        (self.variables[variable])[0].update({'future' : signal_value})
        
    # checking if is variable or time indicator 
    def isVariable(self, token):
        return True if token in string.ascii_uppercase else False
     
    # getting the time value 
    def get_time(self, token):
        return int(token[1:])
    
    # Simulating of the logical circuit 
    def run_simulation(self, df_stimuli, delay):
        
        print()        
        print(f'-'*30)
        print(f'Running Simulation')
        print(f'Delay: {delay}')
        print(f'-'*30)
        print()

        # initializing auxiliary objects 
        self.initialize_working_circuit_objects()

        # setting simulation time 
        simulation_time = -1 

        # setting indicator of cycles delta time to do 
        has_cycles_delta_time_to_do = False

        # setting indicator of finished stimulus 
        finished_stimulus = False

        # setting end of simulation indicator
        end_simulation_indicator = False   
        
        # running simulation of logical circuit 
        while not end_simulation_indicator:

            # evaluating stimuli to process 
            if not finished_stimulus: 

                # runing the stimuli input             
                stimuli = df_stimuli.values.tolist()
                for stimulus in stimuli:       
                    print(f'Stimulus: {stimulus}')
                    token = stimulus[0]
                    if self.isVariable(token):
                        self.set_actual_signal(token, int(stimulus[2]))
                        self.set_future_signal(token, int(stimulus[2]))

                        # setting indicator of cycles delta time to do 
                        has_cycles_delta_time_to_do = True 

                        # next stimulus 
                        continue
                    else:
                        # setting new simulation time 
                        simulation_time = simulation_time + 1
                        
                        # getting time indicator
                        time_indicator = self.get_time(token)

                        # run cycles of the circuit 
                        self.run_cycles_of_delta_time(delay, simulation_time, time_indicator)

                        # setting indicator of cycles delta time as nothing to do 
                        has_cycles_delta_time_to_do = False

                        x = 0      

                    # show current configuration of the circuit variables 
                    # self.show_variables()

                # setting finished stimulus 
                finished_stimulus = True 


            # checking if has cycles delta time to run
            if has_cycles_delta_time_to_do:
                # setting new simulation time 
                simulation_time = simulation_time + 1

                # getting time indicator
                time_indicator = 1

                # run cycles of the circuit 
                self.run_cycles_of_delta_time(delay, simulation_time, time_indicator)

            # checking if last two outputs are equals 
            if self.last_output == self.penultimate_output:
                # setting end of simulation indicator
                end_simulation_indicator = True   

            x = 0
        
        # printing execution output 
        self.show_final_output(delay)

        x = 0

    # running the circuit cycles according to the time indicator 
    def run_cycles_of_delta_time(self, delay, simulation_time, time_indicator):

        # setting end of delta time
        end_delta_time = False   
        
        # running simulation of logical circuit while delta time is active 
        while not end_delta_time:

            # execute all component operations
            for component_sequence in self.components_execution_sequence:

                # getting parameters to execute operation
                variable_output = component_sequence[1]

                component = self.components[variable_output]
                operation = component[0].get('operation')
                first_variable = component[0].get('first_variable')
                second_variable = component[0].get('second_variable')

                # getting current values in the variables actual 
                first_variable_value = self.get_variable_signal(first_variable, 'actual')
                second_variable_value = self.get_variable_signal(second_variable, 'actual')
                
                # calculating the operation 
                result = self.calculate_operation_result(operation, first_variable_value, second_variable_value)
                
                # setting result into the variables future
                self.set_future_signal(variable_output, result)

            # evaluating conditions to finished when delay is 0
            if delay == self.DELAY_0:
                if not self.has_variable_with_actual_and_future_values_different():
                    # setting end of delta time because need to run at least one more cycle
                    end_delta_time = True 

                # move all future values to actual values 
                self.move_future_to_actual_values()

            # evaluating conditions to finished when delay is 1
            if delay == self.DELAY_1:
                # setting end of delta time because need to run at least one more cycle
                end_delta_time = True 

        # adding variables future to final future 
        self.add_actual_values_to_output(simulation_time)

        # when delay is 1 we must to move future to actual values after all 
        if delay == self.DELAY_1:
            # move all future values to actual values 
            self.move_future_to_actual_values()


    # calculating result of operation 
    def calculate_operation_result(self, operation, first_variable_value, second_variable_value):
        # initializing rsult 
        result = 0

        # calculation operation 
        if operation == 'AND':
            result = self.operation_AND(first_variable_value, second_variable_value) 
        if operation == 'OR':
            result = self.operation_OR(first_variable_value, second_variable_value) 
        if operation == 'NOT':
            result = self.operation_NOT(first_variable_value) 
        if operation == 'NAND':
            result = self.operation_NAND(first_variable_value, second_variable_value) 
        if operation == 'NOR':
            result = self.operation_NOR(first_variable_value, second_variable_value) 
        if operation == 'XOR':
            result = self.operation_XOR(first_variable_value, second_variable_value) 

        # resturning the result of operation
        return result 

    # calculating the AND operation 
    def operation_AND(self, first_operator, second_operator):
        # print(f'{first_operator} and {second_operator} = {first_operator and second_operator}')
        return first_operator and second_operator
    
    # calculating the OR operation 
    def operation_OR(self, first_operator, second_operator):
        # print(f'{first_operator} or {second_operator} = {first_operator or second_operator}')
        return first_operator or second_operator
    
    # calculating the NOT operation 
    def operation_NOT(self, operator):
        # print(f'not {operator} = {~operator+2}')
        return ~operator+2
        # return not(operator)
    
    # calculating the NAND operation 
    def operation_NAND(self, first_operator, second_operator):
        # print(f'> {first_operator} nand {second_operator} = {self.operation_NOT(self.operation_AND(first_operator, second_operator))}')
        return self.operation_NOT(self.operation_AND(first_operator, second_operator))
 
    # calculating the NOR operation   
    def operation_NOR(self, first_operator, second_operator):
        # print(f'> {first_operator} nor {second_operator} = {self.operation_NOT(self.operation_OR(first_operator, second_operator))}')
        return self.operation_NOT(self.operation_OR(first_operator, second_operator))
    
    # calculating the XOR operation 
    def operation_XOR(self, first_operator, second_operator):
        # print(f'{first_operator} xor {second_operator} = {first_operator ^ second_operator}')
        return first_operator ^ second_operator
  
    # check if each variable has different values of actual and future
    def has_variable_with_actual_and_future_values_different(self):
        for variable, variable_value in self.variables.items():
            if self.get_variable_signal(variable, 'actual') != self.get_variable_signal(variable, 'future'):
                # there are no variables with actual and future values different
                return True
        
        # has some variable with actual and future values are different 
        return False
    
    # move the future value to actual value of all variables
    def move_future_to_actual_values(self) -> str:
        for variable, variable_value in self.variables.items():
            self.move_future_to_actual_variable(variable)

    # move the future value to actual value of the one variable 
    def move_future_to_actual_variable(self, variable) -> str:
        self.set_actual_signal(variable, self.get_variable_signal(variable, 'future'))

    #  show variable values 
    def show_variables(self) -> str:
        print()        
        print(f'-'*30)
        print(f'Circuit Variables: {len(self.variables)}')
        print()
        for variable in self.variables:
            if variable <= 'H':
                print(f'{variable} - {self.variables.get(variable)} ')
            # print(f'variable: {self.variables[variable]}  actual:  ')
            # print(variable['actual'])
            # print(f'variable: {variable}  actual: {variable['actual']}   future: {variable['future']} ')
  
    def show_components(self) -> str:
        print()        
        print(f'-'*30)
        print(f'Circuit Components: {len(self.components)}')
        print()
        for component in self.components:
            print(f'{component} - {self.components.get(component)} ')

        print()
        print(f'Execution sequence of the Components')
        print()
        for component in self.components_execution_sequence:
            print(f'{component[0]} - {component[1]} ')

    def add_actual_values_to_output(self, time) -> str:
        output_string = str(time) 
        self.penultimate_output = self.last_output
        self.last_output = ''
        for variable in self.variables:
            if variable <= 'H':
                output_string = output_string + ',' + str(self.get_variable_signal(variable, 'actual'))
                self.last_output = self.last_output + str(self.get_variable_signal(variable, 'actual'))

        # ATTENTION: IMPLEMENTS THIS HARDCODE ACCORDING BY THE VARIABLES LIST
        # adding header 
        if len(self.outputs) == 0:
            self.outputs.append('Tempo A B C D E F G H')

        # printing future 
        self.outputs.append(output_string)
        print(output_string)

    def show_final_output(self, delay) -> str:
        print()
        print(f'-'*30)
        print(f'Simulation with delay: {delay}')
        print()
        print(f'Final output: {len(self.outputs)}')
        print()
        for output in self.outputs:
            print(output)

        print()
