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
            self.variables[letter] = [{'last_input' : 0, 
                                       'penultimate_input' : 0,
                                       'simulation_time' : 0,
                                       'used' : False}
                                       ]
        
        # building circuit components
        list = df_circuit.values.tolist()
        for item in list:
            self.components[item[0]] = [{'operation' : item[2], 
                                         'first_variable' : item[3], 
                                         'second_variable' : item[4],
                                         'priority' : 0, 
                                         'simulation_time' : -1}
                                         ]    
            self.set_variable_as_used(item[0])        
            self.set_variable_as_used(item[3])        
            self.set_variable_as_used(item[4])        

        # setting components priority to run
        self.define_priority_of_components()

    # initializing working circuit objects 
    def initialize_working_circuit_objects(self):
        self.outputs = []
        self.last_output = ''
        self.penultimate_output = ''
        for variable in self.variables:
            self.set_last_input_signal(variable, 0)
            self.set_penultimate_input_signal(variable, 0)
            self.variables[variable][0].update({'simulation_time' : 0})


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

    # # getting the actual signal value of the variable
    # def get_actual_signal(self, variable): 
    #     return self.variables.get(variable)[0].get('actual')
    
    # # setting signal value in the variable actual 
    # def set_actual_signal(self, variable, signal_value):
    #     (self.variables[variable])[0].update({'actual' : signal_value})

    # getting the last input of the variable
    def get_last_input_signal(self, variable): 
        if variable is np.nan:
            return None
        return self.variables.get(variable)[0].get('last_input')
    
    # setting the last input of the variable
    def set_last_input_signal(self, variable, signal_value):
        (self.variables[variable])[0].update({'last_input' : signal_value})

    # getting the penultimate input of the variable
    def get_penultimate_input_signal(self, variable):
        if variable is np.nan:
            return None
        return self.variables.get(variable)[0].get('penultimate_input')
    
    # setting the penultimate input of the variable
    def set_penultimate_input_signal(self, variable, signal_value):
        (self.variables[variable])[0].update({'penultimate_input' : signal_value})

    # getting indicator as used for variable
    def get_variable_used(self, variable): 
        if variable is np.nan:
            return None
        return self.variables.get(variable)[0].get('used')
    
    # setting variable as used
    def set_variable_as_used(self, variable):
        if variable is np.nan:
            return None
        (self.variables[variable])[0].update({'used' : True})

    # # getting the signal value of the variable actual 
    # def get_variable_signal(self, variable, actual_or_future): 
    #     if variable is np.nan:
    #         return None
    #     return self.variables.get(variable)[0].get(actual_or_future)
    
    # # setting signal value in the variable actual 
    # def set_actual_signal(self, variable, signal_value):
    #     (self.variables[variable])[0].update({'actual' : signal_value})
        
    # # setting signal value in the variable future 
    # def set_future_signal(self, variable, signal_value):
    #     (self.variables[variable])[0].update({'future' : signal_value})
        
    # checking if is variable or time indicator 
    def isVariable(self, token):
        return True if token in string.ascii_uppercase else False
     
    # getting the time value 
    def get_time(self, token):
        return int(token[1:])
    
    # Simulating of the logical circuit 
    def run_simulation(self, lst_stimuli, delay):
        
        print()        
        print(f'Running Simulation')
        print(f'Delay: {delay}')
        print()

        # initializing auxiliary objects 
        self.initialize_working_circuit_objects()

        # setting simulation time 
        simulation_time = 0

        # setting indicator of cycles delta time to do 
        has_cycles_delta_time_to_do = False

        # setting indicator of finished stimulus 
        finished_stimulus = False

        # setting end of simulation indicator
        end_simulation_indicator = False   

        # setting initial conditions for components 
        self.set_simulation_time_of_components(simulation_time, delay)
        
        loop_counter = 0
        timeout = 100

        # running simulation of logical circuit 
        while not end_simulation_indicator  and  loop_counter < timeout:

            # evaluating stimuli to process 
            if not finished_stimulus: 

                # runing the stimuli input             
                # stimuli = df_stimuli.values.tolist()
                for stimulus in lst_stimuli:       
                    print(f'run_simulation 01')
                    print(f'Stimulus: {stimulus}')
                    token = stimulus[0]
                    if self.isVariable(token):
                        #  setting input signal to last input signal 
                        self.move_last_to_penultimate_input_signal_of_variable(token)
                        self.set_last_input_signal(token, int(stimulus[2]))
                        if delay == self.DELAY_0:
                            self.move_last_to_penultimate_input_signal_of_variable(token)                       

                        # setting indicator of cycles delta time to do 
                        has_cycles_delta_time_to_do = True 

                        # next stimulus 
                        continue

                    else:

                        print(f'run_simulation 02')

                        # setting initial conditions of stimulus 
                        if simulation_time == 0:
                            self.move_last_to_penultimate_input_signal_of_variables()

                        # getting time indicator
                        time_indicator_value = self.get_time(token)
                        for i in range(time_indicator_value):
                         
                            print(f'run_simulation 03')

                            # calculate the logical gates
                            self.calculate_logical_gates(simulation_time, delay)

                            # move last input to penultimate input signal
                            self.move_last_to_penultimate_input_signal_of_variables()

                            # setting new simulation time 
                            simulation_time = simulation_time + 1

                            # setting the simulation time of the components according by delay
                            self.set_simulation_time_of_components(simulation_time, delay)

                        # setting indicator of cycles delta time as nothing to do 
                        has_cycles_delta_time_to_do = False

                # setting finished stimulus 
                finished_stimulus = True 

                print(f'run_simulation 04')


            # checking if has cycles delta time to run
            if has_cycles_delta_time_to_do:

                print(f'run_simulation 05')

                # calculate the logical gates
                self.calculate_logical_gates(simulation_time, delay)

                # move last input to penultimate input signal
                self.move_last_to_penultimate_input_signal_of_variables()

                # setting new simulation time 
                simulation_time = simulation_time + 1

                # setting the simulation time of the components according by delay
                self.set_simulation_time_of_components(simulation_time, delay)


            print(f'run_simulation 06')

            # checking if last two outputs are equals 
            if self.last_output == self.penultimate_output:
                # setting end of simulation indicator
                end_simulation_indicator = True
            else:   
                has_cycles_delta_time_to_do = True

            loop_counter = loop_counter + 1
        
        # printing execution output 
        self.show_final_output(delay)

        if loop_counter >= timeout:
            print(f'ATENÇÃO: A simulação foi encerrada com \'timeout\' de {timeout} repetições sem estabilizar a saída do circuito!')

        print(f'run_simulation 07')



    # setting the simulation time of the variable according by delay
    def set_simulation_time_of_variable(self, variable, simulation_time, delay):
        # self.variables[variable][0].update({'simulation_time' : simulation_time})
        if simulation_time == 0:
            self.variables[variable][0].update({'simulation_time' : 0})
        else:
            self.variables[variable][0].update({'simulation_time' : (simulation_time + delay)})

    # setting the simulation time of the components according by delay
    def set_simulation_time_of_components(self, simulation_time, delay):
        for component_key in self.components:
            component_value  = self.components[component_key]
            if delay == 0:
                component_value[0].update({'simulation_time' : simulation_time})    
            else:
                if delay == 1:
                    if simulation_time == 0:
                        component_value[0].update({'simulation_time' : 1})
                    else:
                        component_value[0].update({'simulation_time' : simulation_time})
                else:
                    # reserved for future use, so assume delay = 0 
                    component_value[0].update({'simulation_time' : simulation_time})    

    # # setting the simulation time of the variable according by delay
    # def set_actual_values_according_by_simulation_time(self, simulation_time):
    #     for variable in self.variables:
    #         if simulation_time == 0  or \
    #             simulation_time == self.variables[variable][0].get('simulation_time'):
    #             self.move_future_to_actual_variable(variable)
    #             self.variables[variable][0].update({'simulation_time' : -1})

    # calculating the logical gates (components)
    def calculate_logical_gates(self, simulation_time, delay):

        # setting end of delta time
        end_delta_time = False   
        
        # running simulation of logical circuit while delta time is active 
        while not end_delta_time:
            print(f'calculate_logical_gates 01')

            # indicator of updating component values
            has_updating_component_value = False 

            # execute all component operations depending on the simulation time 
            for component_sequence in self.components_execution_sequence:

                print(f'calculate_logical_gates 02')

                # getting parameters to execute operation
                variable_output = component_sequence[1]

                component = self.components[variable_output]
                component_simulation_time = component[0].get('simulation_time')
                if component_simulation_time == simulation_time:
                    
                    print(f'calculate_logical_gates 02.1')

                    # get other component attributes 
                    operation = component[0].get('operation')
                    first_variable = component[0].get('first_variable')
                    second_variable = component[0].get('second_variable')
                
                    # getting current values of the variables
                    first_variable_value = self.get_penultimate_input_signal(first_variable)
                    second_variable_value = self.get_penultimate_input_signal(second_variable)
                
                    # calculating the operation 
                    result = self.calculate_operation_result(operation, first_variable_value, second_variable_value)
                
                    # setting indicator updating component value
                    if self.get_last_input_signal(variable_output) != result:
                        has_updating_component_value = True
                        
                    # setting result into the variables 
                    self.set_last_input_signal(variable_output, result)
                    if delay == self.DELAY_0:
                        self.move_last_to_penultimate_input_signal_of_variable(variable_output)
            
            if not has_updating_component_value:
                # setting end of delta time because need to run at least one more cycle
                end_delta_time = True 

        # adding variables values to output 
        self.add_values_to_simulation_output(simulation_time)

        print(f'calculate_logical_gates 03')

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
  
    # # check if each variable has different values of actual and future
    # def has_variable_with_actual_and_future_values_different(self):
    #     for variable, variable_value in self.variables.items():
    #         if self.get_variable_signal(variable, 'actual') != self.get_variable_signal(variable, 'future'):
    #             # there are no variables with actual and future values different
    #             return True
        
    #     # has some variable with actual and future values are different 
    #     return False
    
    # move the last input value to penultimate input value of all variables
    def move_last_to_penultimate_input_signal_of_variables(self):
        for variable, variable_value in self.variables.items():
            self.move_last_to_penultimate_input_signal_of_variable(variable)

    # move the last input value to penultimate input value of one variable 
    def move_last_to_penultimate_input_signal_of_variable(self, variable):
        self.set_penultimate_input_signal(variable, self.get_last_input_signal(variable))

    # # move the future value to actual value of all variables
    # def move_future_to_actual_values(self) -> str:
    #     for variable, variable_value in self.variables.items():
    #         self.move_future_to_actual_variable(variable)

    # # move the future value to actual value of the one variable 
    # def move_future_to_actual_variable(self, variable) -> str:
    #     self.set_actual_signal(variable, self.get_variable_signal(variable, 'future'))

    #  show variable values 
    def show_variables(self) -> str:
        print()        
        print(f'-'*30)
        print(f'Circuit Variables: {len(self.variables)}')
        print()
        for variable in self.variables:
            if variable <= 'H':
                print(f'{variable} - {self.variables.get(variable)} ')
  
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

    def add_values_to_simulation_output(self, time) -> str:
        output_string = str(time) 
        self.penultimate_output = self.last_output
        self.last_output = ''
        header = 'Tempo'
        for variable in self.variables:
            if self.get_variable_used(variable):
                header = header + ',' + variable
                output_string = output_string + ',' + str(self.get_last_input_signal(variable))
                self.last_output = self.last_output + str(self.get_last_input_signal(variable))

        # adding output header 
        if len(self.outputs) == 0:
            self.outputs.append(header)

        # printing future 
        self.outputs.append(output_string)
        print(output_string)

    def show_final_output(self, delay) -> str:
        print()
        print(f'-'*30)
        print(f'Simulation with delay: {delay}')
        print()
        print(f'Final output: {len(self.outputs)-1} simulation time')
        print()
        for output in self.outputs:
            print(output)

        print()
