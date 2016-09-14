'''
Created on 13.09.2016

@author: mkennert
'''
from kivy.properties import NumericProperty
from numpy import arange

from functions.function import IFunction
import numpy as np


class Logarithm(IFunction):
    '''
    represents a logarithm-function f(x)=log((y+a)/a)/b
    '''
    
    # parameter a
    a = NumericProperty()
    
    # parameter b 
    b = NumericProperty()
    
    '''
    constructor
    '''
    
    def __init__(self, a, b, minStrain, maxStrain):
        self.a, self.b = a, b
        self.eps = 1.05
        self.minStrain, self.maxStrain = minStrain, maxStrain
        d = (self.maxStrain - self.minStrain) / 1e2
        self.points = [(x, self.f(x)) for x in arange(self.minStrain, self.maxStrain, d)]
    
    '''
    evaluate the logarithm-function by the parameters a and b
    '''
    
    def f(self, x):
        if x >= self.minStrain * self.eps and x <= self.maxStrain * self.eps:
            return np.log((x + self.a) / self.a) / self.b
        else:
            return 0
    
    '''
    return the function as a string
    '''
       
    def f_toString(self):
        return "f(x)=log((x+" + str(self.a) + ")/" + str(self.a) + ")/" + str(self.b)
