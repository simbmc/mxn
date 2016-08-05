'''
Created on 06.05.2016

@author: mkennert
'''
from functions.function import IFunction


class Linear(IFunction):
    '''
    represents a linear function f(x)=ax+b
    '''
    # constructor
    def __init__(self, a, b, minStrain, maxStrain, minStress, maxStress):
        self.a = a
        self.b = b
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStrain, maxStress
        self.points=[(minStress,self.f(minStress)),(maxStress,self.f(maxStress))]
        
    def f(self, x):
        return self.a * x + self.b
        
    def f_toString(self):
        return "f(x)=" + str(self.a) + "x"
