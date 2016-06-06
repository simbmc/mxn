'''
Created on 06.05.2016

@author: mkennert
'''
from functions.function import IFunction
'''
represents a quadratic function f(x)=ax^2+bx+c
'''
class QuadraticFunction(IFunction):
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c
    
    def f(self,x):
        return self.a*x**2+self.b*x+self.c
    
    def setA(self,value):
        self.a=value
    
    def setB(self,value):
        self.b=value 
    
    def setC(self,value):
        self.c=value 