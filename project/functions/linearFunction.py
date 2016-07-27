'''
Created on 06.05.2016

@author: mkennert
'''
from functions.function import IFunction
'''
represents a linear function f(x)=ax+b
'''
class Linear(IFunction):
    def __init__(self, a, b):
        self.a=a
        self.b=b
    
    def f(self,x):
        return self.a*x+self.b
        
    def f_toString(self):
        return "f(x)="+str(self.a)+"x"