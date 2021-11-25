import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import re 


class GraphSaveImage:
    def __init__(self, user_function, range_start, range_finish ):
        self.user_function = user_function 
        self.range_start = range_start 
        self.range_finish = range_finish

    def format_user_function(self):
        trigonometric_indicators = ['sin', 'cos', 'tan', 'sqrt'] 

        def trigonometric_replacement(sequence):

            user_trigonometric = ['arcsin', 'arccos', 'arctg', 'tg']
            computer_trigonometric = ['asin', 'acos', 'atan', 'tan']
            for i in range(4):
                sequence = sequence.replace(user_trigonometric[i], computer_trigonometric[i])
            return sequence

        self.user_function = trigonometric_replacement(self.user_function)

        def add_math_in_sequence(input, sequence):

            default = [m.start() for m in re.finditer(sequence, input)]
            default = default[::-1]
            for i in default:

                if input[i-1] == 'a':
                    i = i-1
                input = input[:i] + 'math.' + input[i:]
            return input
        
        for i in trigonometric_indicators:
            self.user_function = add_math_in_sequence(self.user_function, i) 


        self.user_function = self.user_function.replace('^', '**')

        return self.user_function 


    def save_graph_img(self,eqName):
        plt.clf() 
        x_values = []
        y_values = []
    
        def get_y_values_from_function(function, x_values):
            for x in x_values:
                y_values.append(eval(function))
            return y_values
        self.user_function = self.format_user_function() 

        x_values = np.linspace(self.range_start, self.range_finish, num=1000)
        y_values = get_y_values_from_function(self.user_function, x_values)
        
        plt.plot(x_values, y_values)
        plt.savefig(f'ImageGraphics\{eqName}.jpg', dpi = 300) 
        

