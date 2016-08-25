'''
Created on 06.05.2016

@author: mkennert
'''
from functions.function import IFunction


class Linear(IFunction):
    
    '''
    represents a linear function f(x)=ax
    '''
    
    # constructor
    def __init__(self, a, minStrain, maxStrain, minStress, maxStress):
        self.a = a
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStress, maxStress
        self.points=[(minStress,self.f(minStress)),(maxStress,self.f(maxStress))]
        
    def f(self, x):
        return self.a*x
    
    def f_toString(self):
        return "f(x)=" + str(self.a) + "x"
