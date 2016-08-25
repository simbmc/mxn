'''
Created on 06.05.2016

@author: mkennert
'''
'''
represents a quadratic function f(x)=ax^2+bx
'''

from numpy import arange

from functions.function import IFunction


class QuadraticFunction(IFunction):
    def __init__(self, a, b, minStrain, maxStrain, minStress, maxStress):
        self.a = a
        self.b = b
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStrain, maxStress
        d=(self.maxStrain-self.minStrain)/1e2
        self.points=[(x,self.f(x)) for x in arange(self.minStrain,self.maxStrain,d)]
    
    def f(self, x):
        return self.a * x ** 2 + self.b * x
    
    def f_toString(self):
        return "f(x)=" + str(self.a) + "x^2+" + str(self.b) + "x"
