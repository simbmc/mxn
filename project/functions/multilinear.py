'''
Created on 06.07.2016

@author: mkennert
'''
from functions.function import IFunction
from numpy import interp


class Multilinear(IFunction):
    
    # constructor
    def __init__(self, x, y,minStrain, maxStrain, minStress, maxStress):
        # x=x-coordinates, y=y-coordinates
        self.x, self.y = x, y
        self.points=[(x[i],y[i]) for i in range(len(x))]
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStrain, maxStress
    
    def f(self, val):
        return interp(val, self.x, self.y)
    
    '''
    return the function as a string
    '''
    def f_toString(self):
        return "multilinear"
        