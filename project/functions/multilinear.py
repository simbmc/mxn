'''
Created on 06.07.2016

@author: mkennert
'''

from numpy import interp

from functions.function import IFunction


class Multilinear(IFunction):
    
    '''
    represents a multilinear function
    '''
    
    
    '''
    constructor
    '''
    
    def __init__(self, x, y, minStrain, maxStrain, minStress, maxStress):
        # x=x-coordinates, y=y-coordinates
        self.x, self.y = x, y
        self.eps=1.05
        self.points = [(x[i], y[i]) for i in range(len(x))]
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStrain, maxStress
    
    '''
    evaluate the multi-linear-function by the given points
    '''
        
    def f(self, x):
        if x >= self.minStrain*self.eps and x <= self.maxStrain*self.eps:
            return interp(x, self.x, self.y)
        else: 
            return 0
    
    '''
    return the function as a string
    '''
    def f_toString(self):
        return "multi-linear"
        
