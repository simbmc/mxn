'''
Created on 06.05.2016

@author: mkennert
'''
from numpy import arange

from functions.function import IFunction
import numpy as np
from kivy.properties import NumericProperty


class ExponentialFunction(IFunction):
    
    '''
    represents a exponentialFunction f(x)=ae^(bx)
    '''
    
    # parameter a
    a = NumericProperty()
    
    # parameter b 
    b = NumericProperty()
    
    '''
    constructor
    '''
    
    def __init__(self, a, b, minStrain, maxStrain, minStress, maxStress):
        self.a, self.b = a, b
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStrain, maxStress
        d = (self.maxStrain - self.minStrain) / 1e2
        self.points = [(x, self.f(x)) for x in arange(self.minStrain, self.maxStrain, d)]
    
    '''
    evaluate the exponential-function by the parameters a and b
    '''
    
    def f(self, x):
        if x >= self.minStrain and x <= self.maxStrain:
            return self.a * np.exp(self.b * x)
        else:
            return 0
    
    '''
    return the function as a string
    '''
       
    def f_toString(self):
        return "f(x)=" + str(self.a) + "e^(" + str(self.b) + "x)"
    
