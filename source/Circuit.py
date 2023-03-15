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

        # variables list of the circuit
        for letter in string.ascii_uppercase:
            self.variables[letter] = [{'input' : 0, 'output' : 0}]
        
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
                if (self.is_output_of_component(first_variable)     and 
                    not self.has_priority(first_variable)
                    ):
                    end = False
                    continue

                second_variable = component_value[0].get('second_variable')
                if (second_variable != None                         and
                    self.is_output_of_component(second_variable)    and 
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
        self.components_execution_sequence = sorted(list)

    # checking if the varibale is output of some of circuit component
    def has_priority(self, variable):
        xxx =  self.components.get(variable)[0].get('priority')
        return True if self.components.get(variable)[0].get('priority') > 0 else False
        
    # checking if component has setted priority
    def is_output_of_component(self, variable):
        return True if self.components.get(variable) != None else False

    # getting the signal value of  the variable input 
    def get_variable_signal(self, variable, input_or_output): 
        if variable is np.nan:
            return None
        return self.variables.get(variable)[0].get(input_or_output)
    
    # setting signal value in the variable input 
    def set_input_signal(self, variable, signal_value):
        (self.variables[variable])[0].update({'input' : signal_value})
        
    # setting signal value in the variable output 
    def set_output_signal(self, variable, signal_value):
        (self.variables[variable])[0].update({'output' : signal_value})
        
    # checking if is variable or time indicator 
    def isVariable(self, token):
        return True if token in string.ascii_uppercase else False
     
    # getting the time value 
    def get_time(self, token):
        return int(token[1:])
    
    # running the circuit cycles according to the time indicator 
    def run_cycles(self, time_indicator):
        # when do I have to use the time indicator?


        # execute all component operations
        for component_sequence in self.components_execution_sequence:
            # getting parameters to execute operation
            variable_output = component_sequence[1]
            # print(f'{component_sequence[0]} - {variable_output} ')
            component = self.components[variable_output]
            operation = component[0].get('operation')
            first_variable = component[0].get('first_variable')
            second_variable = component[0].get('second_variable')
            # print(component)
            # print(f'{variable_output} = {operation} {first_variable} {second_variable}')

            # getting current values in the variables input 
            first_variable_value = self.get_variable_signal(first_variable, 'input')
            second_variable_value = self.get_variable_signal(second_variable, 'input')
            # print(f'first_variable: {first_variable}:{first_variable_value}  second_variable_value: {second_variable}:{second_variable_value}  ')
            
            # calculating the operation 
            result = 0
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
            # print(f'result: {result}')

            # setting result into the variables output
            self.set_output_signal(variable_output, result)
            # self.show_variables()

            # when compute component operation, the output must be copied to input value signal 
            self.move_output_to_input_variable(variable_output)

            x = 0

        # adding variables output to final output 
        self.add_final_output(time_indicator)

        # moving output signal to input signal of all variables 
        self.move_output_to_input_values()
        x = 0

        # components[item[0]] = [{'operation' : item[2], 
        #                                  'first_variable' : item[3], 
        #                                  'second_variable' : item[4],
        #                                  'priority' : 0}

    # calculating the AND operation 
    def operation_AND(self, first_operator, second_operator):
        print(f'{first_operator} and {second_operator} = {first_operator and second_operator}')
        return first_operator and second_operator
    
    # calculating the OR operation 
    def operation_OR(self, first_operator, second_operator):
        print(f'{first_operator} or {second_operator} = {first_operator or second_operator}')
        return first_operator or second_operator
    
    # calculating the NOT operation 
    def operation_NOT(self, operator):
        print(f'not {operator} = {~operator+2}')
        return ~operator+2
        # return not(operator)
    
    # calculating the NAND operation 
    def operation_NAND(self, first_operator, second_operator):
        print(f'> {first_operator} nand {second_operator} = {self.operation_NOT(self.operation_AND(first_operator, second_operator))}')
        return self.operation_NOT(self.operation_AND(first_operator, second_operator))
 
    # calculating the NOR operation   
    def operation_NOR(self, first_operator, second_operator):
        print(f'> {first_operator} nor {second_operator} = {self.operation_NOT(self.operation_OR(first_operator, second_operator))}')
        return self.operation_NOT(self.operation_OR(first_operator, second_operator))
    
    # calculating the XOR operation 
    def operation_XOR(self, first_operator, second_operator):
        print(f'{first_operator} xor {second_operator} = {first_operator ^ second_operator}')
        return first_operator ^ second_operator
  
    # move the output value to input value of all variables
    def move_output_to_input_values(self) -> str:
        for variable, variable_value in self.variables.items():
            self.move_output_to_input_variable(variable)

    # move the output value to input value of the one variable 
    def move_output_to_input_variable(self, variable) -> str:
        self.set_input_signal(variable, self.get_variable_signal(variable, 'output'))

    def show_variables(self) -> str:
        print()        
        print(f'-'*30)
        print(f'Circuit Variables: {len(self.variables)}')
        print()
        for variable in self.variables:
            if variable <= 'H':
                print(f'{variable} - {self.variables.get(variable)} ')
            # print(f'variable: {self.variables[variable]}  input:  ')
            # print(variable['input'])
            # print(f'variable: {variable}  input: {variable['input']}   output: {variable['output']} ')
  
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

    def add_final_output(self, time) -> str:
        output_string = str(time) + '-'
        for variable in self.variables:
            if variable <= 'H':
                output_string = output_string + ',' + str(self.get_variable_signal(variable, 'output'))

        # printing output 
        self.outputs.append(output_string)
        print(output_string)

    def show_final_output(self) -> str:
        print()
        print(f'-'*30)
        print(f'Final Output: {len(self.outputs)}')
        print()
        for output in self.outputs:
            print(output)

        print()
