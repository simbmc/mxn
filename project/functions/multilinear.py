'''
Created on 06.07.2016

@author: mkennert
'''
from functions.function import IFunction
from numpy import interp


class Multilinear(IFunction):
    # constructor

    def __init__(self, x, y):
        # x=x-coordinates, y=y-coordinates
        self.x, self.y = x, y
    
    def f(self, val):
        return interp(val, self.x, self.y)
    
    '''
    return the function as a string
    '''
    def f_toString(self):
        return "multilinear"
        