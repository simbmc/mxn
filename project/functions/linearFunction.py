'''
Created on 06.05.2016

@author: mkennert
'''
from functions.function import IFunction
'''
represents a linear function f(x)=ax+b
'''
class LinearFunction(IFunction):
    def __init__(self, a, b):
        self.a=a
        self.b=b
    
    def f(self,x):
        return self.a*x+self.b
    
    def setA(self,value):
        self.a=value
    
    def setB(self,value):
        self.b=value
        
    