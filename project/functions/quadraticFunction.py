'''
Created on 06.05.2016

@author: mkennert
'''
from functions.function import IFunction
'''
represents a quadratic function f(x)=ax^2+bx
'''
class QuadraticFunction(IFunction):
    def __init__(self,a,b):
        self.a=a
        self.b=b
    
    def f(self,x):
        return self.a*x**2+self.b*x
    
    def f_toString(self):
        return "f(x)="+str(self.a)+"x^2+"+str(self.b)+"x"