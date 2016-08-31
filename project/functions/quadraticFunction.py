'''
Created on 06.05.2016

@author: mkennert
'''
'''
represents a quadratic function f(x)=ax^2+bx
'''

from kivy.properties import NumericProperty
from numpy import arange

from functions.function import IFunction


class QuadraticFunction(IFunction):
    
    '''
    represents a quadratic-function f(x)=ax*x+b*x
    '''
    
    # important values
    a, b = NumericProperty(), NumericProperty()
    minStrain, maxStrain = NumericProperty(), NumericProperty()
    minStress, maxStress = NumericProperty(), NumericProperty()
    
    # constuctor
    def __init__(self, a, b, minStrain, maxStrain, minStress, maxStress):
        self.a, self.b = a, b
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStress, maxStress
        d = (self.maxStrain - self.minStrain) / 1e2
        self.points = [(x, self.f(x)) for x in arange(self.minStrain, self.maxStrain, d)]
    
    '''
    evaluate the quadratic-function by the parameters a
    '''
        
    def f(self, x):
        if x >= self.minStrain and x <= self.maxStrain:
            return self.a * x ** 2 + self.b * x
        else:
            return 0
    
    '''
    return the function as a string
    '''
       
    def f_toString(self):
        return "f(x)=" + str(self.a) + "x^2+" + str(self.b) + "x"
