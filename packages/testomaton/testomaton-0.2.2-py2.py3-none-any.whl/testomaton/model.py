# 
#  Copyright Testify AS
# 
#  This file is part of testomaton suite
# 
#  testomaton is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  For the commercial license, please contact Testify AS.
#
#  testomaton is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with testomaton.  If not, see <http://www.gnu.org/licenses/>.
# 
#  See LICENSE file for the complete license text.
# 

from copy import deepcopy
import sys

ignore_constraints = False
ignore_assignments = False
global_whitelist = []
global_blacklist = []
parameters_blacklist = []
parameters_whitelist = []
choices_blacklist = []
choices_whitelist = []
constraints_blacklist = []
constraints_whitelist = []
assignments_blacklist = []
assignments_whitelist = []

def should_parse_element(description, specific_whitelist=[], specific_blacklist=[], extra_labels=[]):
    """
    Check if an element described by 'description' should be parsed based on global and local whitelists and blacklists, 
    as well as other conditions.

    Args:
        description (dict): The description of the element
        specific_whitelist (list): The list of labels that are allowed
        specific_blacklist (list): The list of labels that are not allowed
        extra_labels (list): The list of labels that are inherited from the parent

    Returns: 
        bool: True if the element should be parsed, False otherwise.

    Examples: 
        >>> should_parse_element('choice')
        True
        >>> should_parse_element('constraint', ignore_constraints=True)
        False
    """
    #if description is a primitive type, return true and allow parsing
    if not isinstance(description, dict):
        return True
    
    #get the keys of the dictionary and set the element type to the first key
    element_type = list(description.keys())[0]
    if element_type == 'constraint' and ignore_constraints:
        return False
    if element_type == 'assignment' and ignore_assignments:
        return False
    
    name = description[element_type]
    labels = [] + extra_labels
    #if labels are in the description, set the labels list to the labels in the description 
    if 'labels' in description:
        labels = description['labels']
    labels.append(name)
    
    #set the blacklist to the union of the global_blacklist and the specific_blacklist
    blacklist = list(set(global_blacklist) | set(specific_blacklist))    
    #set the whitelist to the union of the global_whitelist and the specific_whitelis
    whitelist = list(set(global_whitelist) | set(specific_whitelist))
    
    #if the whitelist is not empty, check if any of the labels in 'labels' are in the whitelist, if not return false
    if len(whitelist) > 0:
        if len([label for label in labels if label in whitelist]) == 0:
            return False
    #if the blacklist is not empty, check if any of the labels in 'labels' are in the blacklist, if so return false
    if len(blacklist) > 0:
        if len([label for label in labels if label in blacklist]) > 0:
            return False
    
    return True

class ParameterParent:
    """ Parent class for parameters, which includes all methods for handling parameters in the model"""
    def __init__(self, description, global_params, inherited_labels=[]) -> None:
        """
        Initialize a Parameter object.
        
        Args:
            description (dict): The description of the parameter.
            global_params (dict): The global parameters.
            inherited_labels (list): The list of labels that are inherited from the parent. Defaults to an empty list.

        Raises:
            Exception: If the parameter has both 'parameters' and 'choices' keys. This is not allowed.
            
        Attributes:
            name (str): The name of the parameter.
            choices (list): A list of sub-choices, each being represented as a choice object.
            parameters (list): A list of sub-parameters, each being represented as a parameter object.
            aliases (dict): A dictionary of aliases.
            constraints (dict): A dictionary of constraints.
        
        Returns:
            None
        """
        if 'parameter' in description:
            self.name = str(description['parameter'])
        elif 'output parameter' in description:
            self.name = str(description['output parameter'])

        self.parameters = []
        self.output_parameters = []
        #if description is a yaml node, set the name to the value of the 'parameter' key
        if isinstance(description, dict):
            #if description has 'parameters' key, set labels to the inherited labels and the labels in the description
            if 'parameters' in description:
                labels = [] + inherited_labels
                if 'labels' in description:
                    labels += description['labels']
                #iterate through the parameters in the description and create parameter objects for each
                for parameter in description['parameters']:
                    if not should_parse_element(parameter, parameters_whitelist, parameters_blacklist, labels):
                        continue
                    
                    #if description has 'output parameter'
                    if 'output parameter' in parameter:
                        param = OutputParameter(parameter)
                        self.parameters.append(param)
                        self.output_parameters.append(param)   

                    #if description has 'linked parameter' key, copies and modifies parameter before appending to the parameters list
                    if 'linked parameter' in parameter:
                        linked_to = parameter['linked to']
                        name = parameter['linked parameter']
                        whitelist = parameter['constraints whitelist'] if 'constraints whitelist' in parameter else None
                        blacklist = parameter['constraints blacklist'] if 'constraints blacklist' in parameter else None
                        if whitelist is not None and blacklist is not None:
                            raise Exception(f'Both constraints whitelist and blacklist are defined for linked parameter {parameter.name}')
                        copy = deepcopy(global_params[linked_to])
                        copy.name = name
                        copy.filter_constraints(whitelist, blacklist)
                        self.parameters.append(copy)
                    else:
                        self.parameters.append(Parameter(parameter, global_params, labels))

    def get_leaf_choice_names(self):
        # Get all leaf parameters with full path
        parameter_names = self.get_parameter_names()
        result = []

        for name in parameter_names:
            if name is None:
                continue

            p = self.get_parameter(name)
            if not p.parameters:
                # If the parameter has no sub-parameters, return its own choices
                result.append(p.get_choice_names())  # Append the list of choices as a group
            else:
                # If the parameter has sub-parameters, recursively get their choices
                result.append(p.get_leaf_choice_names())

        result = [r for r in result if r]
        
        return result
    
    def get_parameter_names(self, current_path=''):
        result = []
        for parameter in self.parameters:
            if isinstance(parameter, OutputParameter):
                continue
            if parameter.parameters:
                if current_path == '':
                    result.extend(parameter.get_parameter_names(parameter.name))
                else:
                    result.extend(parameter.get_parameter_names(current_path + '::' + parameter.name))
            else:
                if(current_path == ''): 
                    result.append(parameter.name)
                else:
                    result.append(current_path + '::' + parameter.name)
                
        return result         
    

    def get_parameter(self, name):
        #print("get_parameter is being called in the parent class")
        #if the name contains '::', split the name into tokens
        if name is None:
            return None
        
        if '::' in name:
            tokens = name.split('::')
            child_name = tokens[0]
            remains = '::'.join(tokens[1:])
            #iterate through the parameters and recursively call get_parameter to get each parameter
            for parameter in self.parameters:
                if parameter.name == child_name:
                    return parameter.get_parameter(remains)
        else:
            #iterate through the parameters and return the parameter with the given name
            for parameter in self.parameters:
                if parameter.name == name:
                    return parameter
        return None
   

    def get_parameter_index(self, name):
        """ Get the index of a parameter by name."""
        for i, parameter in enumerate(self.get_parameter_names()):
            if parameter == name:
                return i
        return None
    
class ConstraintParent(ParameterParent):
    def __init__(self, description) -> None:
        self.aliases = {}
        self.constraints = {}
        if 'logic' in description:
            logic = description['logic']

            for element in logic:
                #if element is an alias, set the name and expression of the alias
                if 'alias' in element:
                    name = str(element['alias'])
                    expression = str(element['expression'])
                    if name in self.aliases:
                        raise Exception(f"Alias '{name}' already defined")
                    self.aliases[name] = expression

                #if the element is a constraint, check if the element should be parsed, 
                # then set the name and expression of the constraint    
                if 'constraint' in element:
                    if not should_parse_element(element, constraints_whitelist, constraints_blacklist):
                        continue
                    name = str(element['constraint'])
                    expression = str(element['expression'])
                    if name not in self.constraints:
                        self.constraints[name] = []
                    self.constraints[name].append((None, expression))
            
            #add potential constraints from structures           
            # for parameter in [p for p in self.parameters if p.is_structure()]:
            #     context = parameter.name
            #     for context, name, expression in parameter.get_constraints():
            #         if name not in self.constraints:
            #             self.constraints[name] = []
            #         self.constraints[name].append((context, expression))
        
    def filter_constraints(self, whitelist, blacklist):
        if whitelist is not None and blacklist is not None:
            raise Exception(f'Both constraints whitelist and blacklist are defined for parameter {self.name}')
        if whitelist is not None:
            self.constraints = {k: v for k, v in self.constraints.items() if k in whitelist}
        if blacklist is not None:
            self.constraints = {k: v for k, v in self.constraints.items() if k not in blacklist}
            
        for parameter in self.parameters:
            parameter.filter_constraints(whitelist, blacklist)
    
class ChoiceParent:
    """ Parent class for choices, which includes all methods for handling choices in the model"""
    def __init__(self, description, inherited_labels=[]) -> None:
        self.choices = []
        
        #description is a directory created from parsing the yaml file
        if isinstance(description, dict):                
            if 'choices' in description:
                labels = inherited_labels
                if 'labels' in description:
                    labels += description['labels']
                self.choices = [Choice(choice, labels) for choice in description['choices'] if should_parse_element(choice, choices_whitelist, choices_blacklist, labels)]
            

    def get_choice_names(self, current_path=''):
        result = []
        for choice in self.choices:
            if choice.choices:
                if current_path == '':
                    result.extend(choice.get_choice_names(choice.name))
                else:
                    result.extend(choice.get_choice_names(current_path + '::' + choice.name))
            else:
                if(current_path == ''): 
                    result.append(choice.name)
                else:
                    result.append(current_path + '::' + choice.name)
                
        return result            
        
    def get_choice(self, name):
        """
        Get a choice by name.
    
        Args:
            name (str): The name of the choice to get.
            
        Returns:
            choice: The choice object with the given name.
            or None if the choice is not found.
        """
        #if the name contains '::', split the name into tokens
        if '::' in name:
            tokens = name.split('::')
            child_name = tokens[0]
            #set the remains to the concatenation of the tokens from index 1, separated by '::'
            remains = '::'.join(tokens[1:])
        
            #for each choice in the choices list, if the name of the choice is equal to the child_name, 
            #recursively call get_choice with the remains
            for choice in self.choices:
                if choice.name == child_name:
                    return choice.get_choice(remains)
        else:
            #for each choice in the choices list, if the name of the choice 
            #is equal to the name, return the choice
            for choice in self.choices:
                if choice.name == name:
                    return choice
        return None

class Choice(ChoiceParent):
    def __init__(self, description, global_params, inherited_labels=[]):
        self.name = ''
        self.value = ''
        
        #description is a yaml node
        if isinstance(description, dict):
            children = list(description.keys())
            if 'choice' in children:
                self.name = str(description['choice'])
                if 'value' in description:
                    self.value = str(description['value'])
                    if 'choices' in description:
                        raise Exception(f"Choice '{self.name}' has both value and choices")
                else:
                    self.value = self.name
            else:
                self.value = self.name
        else:
            self.name = str(description)
            self.value = str(description)
            

        super().__init__(description, inherited_labels)


    def __str__(self):
        return f'{self.name}: {self.value}'
    
    def __repr__(self):
        return str(self)


class OutputParameter(ParameterParent):
    """
    A class used to represent an output parameter in a model.

    Output parameters do not have choices which are used in combinatoric test generation.
    However, their value can be defined based on a precondition defined in assignments
    
    Attributes:
        name (str): The name of the output parameter.
        default_value (str): The default value linked to the output parameter.
        parameters (list): The list of parameters that are children of the current output parameter.
    
    Methods:
        get_choice_names: returns a default_value which has been predefined.
    """
    def __init__(self, description):
        """
        Initialize an OutputParameter object.
        
        Args:
            description (dict): The description of the output parameter.
            
        Attributes:
            name (str): The name of the output parameter.
            default_value (str): The default value linked to the output parameter.
            parameters (list): A list of sub-parameters, each being represented as a parameter object.
        
        Returns:
            None
        """
        self.name = str(description['output parameter'])
        self.default_value = str(description['default value'])
        self.parameters = []

    def __str__(self):
        return f'{self.name}: {self.default_value}'
    
    def __repr__(self):
        return str(self)
    
    def get_choice_names(self):
        return [str(self.default_value)]
    
    def is_structure(self):
        return False
        
class Parameter(ConstraintParent, ChoiceParent):
    def __init__(self, description, global_params, inherited_labels=[]) -> None:
        """
        Initialize a Parameter object.
        
        Args:
            description (dict): The description of the parameter.
            global_params (dict): The global parameters.
            inherited_labels (list): The list of labels that are inherited from the parent. Defaults to an empty list.

        Raises:
            Exception: If the parameter has both 'parameters' and 'choices' keys. This is not allowed.
            
        Attributes:
            name (str): The name of the parameter.
            choices (list): A list of sub-choices, each being represented as a choice object.
            parameters (list): A list of sub-parameters, each being represented as a parameter object.
            aliases (dict): A dictionary of aliases.
            constraints (dict): A dictionary of constraints.
        
        Returns:
            None
        """
        ChoiceParent.__init__(self, description, inherited_labels)
        ParameterParent.__init__(self, description, global_params, inherited_labels)
        ConstraintParent.__init__(self, description)

        if isinstance(description, dict):
            #if the description has both 'parameters and 'choices' keys, raise an exception and exit
            if 'parameters' in description and 'choices' in description:
                raise Exception(f'Error: {self.name1} has both parameters and choices')
                
    def __str__(self):
        result = f'{self.name}'
        if self.parameters:
            result += '('
            for parameter in self.parameters:
                result += f'{parameter}, '
            result = result[:-2] + ')'
        return result
    
    def __repr__(self):
        return str(self)


    def get_structures(self):
        return [p for p in self.parameters if p.is_structure()]
        

    def is_structure(self):
        return len(self.parameters) > 0
    

    def get_constraints(self):
        result = []
        for name, expressions in self.constraints.items():
            for expression in expressions:
                result.append((self.name, name, expression))
                
        if self.parameters:
            for parameter in self.parameters:
                for context, name, expression in parameter.get_constraints():
                    result.append((self.name + '::' + context, name, expression))
                    
        return result
    
    def get_aliases(self):
        result = []
        for name, expression in self.aliases.items():
            result.append((self.name, name, expression))

        if self.parameters:
            for parameter in self.parameters:
                for context, name, expression in parameter.get_aliases():
                    result.append((self.name + '::' + context, name, expression))
        return result

class Function(ConstraintParent, ParameterParent):
    def __init__(self, global_params, description):
        """
        Initialize a Function object.
        
        Args:
            global_params (dict): The global parameters.
            description (dict): The description of the function.
        
        Attributes:
            name (str): The name of the function.
            parameters (list): A list of sub-parameters, each being represented as a parameter object.
            output_parameters (list): A list of sub-output parameters, each being represented as an output parameter object.
            aliases (dict): A dictionary of aliases.
            constraints (dict): A dictionary of constraints.
            assignments (dict): A dictionary of assignments.
        
        Returns:
            None
        """
        if 'function' not in description:
            raise ValueError("The 'function' key is missing in the description.")
        
        self.name = str(description['function'])
        ParameterParent.__init__(self, description, global_params)
        ConstraintParent.__init__(self, description)

        self.assignments = {}
        if 'logic' in description:
            logic = description['logic']
            for element in logic:
                #if it is an assignment, check if it should be parsed and set name and expression
                if 'assignment' in element:
                    if not should_parse_element(element, assignments_whitelist, assignments_blacklist):
                        continue
                    name = str(element['assignment'])
                    expression = str(element['expression'])
                    if name not in self.assignments:
                        self.assignments[name] = []
                    self.assignments[name].append(expression)
                
    def __str__(self):
        return f'{self.name}({[parameter.name for parameter in self.parameters]})'
    
    def get_structures(self):
        return [p for p in self.parameters if p.is_structure()]
    
    def get_generator_input(self):
        return self.get_parameter_names(), self.get_leaf_choice_names()

def parse_function(model, function_name=None, **kwargs):
    """ 
    Parse a function from a model file.
    
    Args:
        file (str): The path to the model file.
        function_name (str): The name of the function to parse. Defaults to None.
        **kwargs: Additional keyword arguments.
        
    Returns:
        function: The function object.
    """
    global ignore_constraints, ignore_assignments
    global global_whitelist, global_blacklist
    global parameters_blacklist, parameters_whitelist
    global choices_blacklist, choices_whitelist
    global constraints_blacklist, constraints_whitelist
    global assignments_blacklist, assignments_whitelist
    
    if 'ignore_constraints' in kwargs:
        ignore_constraints = kwargs['ignore_constraints']
    if 'ignore_assignments' in kwargs:
        ignore_assignments = kwargs['ignore_assignments']
    if 'whitelist' in kwargs:
        global_whitelist = kwargs['whitelist']
    if 'blacklist' in kwargs:
        global_blacklist = kwargs['blacklist']
    if 'parameters_blacklist' in kwargs:
        parameters_blacklist = kwargs['parameters_blacklist']
    if 'parameters_whitelist' in kwargs:
        parameters_whitelist = kwargs['parameters_whitelist']
    if 'choices_blacklist' in kwargs:
        choices_blacklist = kwargs['choices_blacklist']
    if 'choices_whitelist' in kwargs:
        choices_whitelist = kwargs['choices_whitelist']
    if 'constraints_blacklist' in kwargs:
        constraints_blacklist = kwargs['constraints_blacklist']
    if 'constraints_whitelist' in kwargs:
        constraints_whitelist = kwargs['constraints_whitelist']
    if 'assignments_blacklist' in kwargs:
        assignments_blacklist = kwargs['assignments_blacklist']
    if 'assignments_whitelist' in kwargs:
        assignments_whitelist = kwargs['assignments_whitelist']            
    
    global_params = {}
    #Makes parameter objects for global parameters if they exist
    if 'global parameters' in model:
        for parameter in model['global parameters']:
            global_params[parameter['parameter']] = Parameter(parameter, global_params)

    if 'functions' not in model:
        raise Exception('No functions defined in model')
    if function_name is None:
        function_def = model['functions'][0]
    #Get the function if the function name is provided
    else:
        function_defs = [function for function in model['functions'] if function['function'] == function_name]
        if len(function_defs) > 1:
            raise Exception(f'Multiple functions with name {function_name}')
        if len(function_defs) == 0:
            raise Exception(f'Function {function_name} not found in the model file')
        function_def = function_defs[0]
    function = Function(global_params, function_def) 

    return function                

