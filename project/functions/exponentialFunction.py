'''
Created on 06.05.2016

@author: mkennert
'''
import numpy as np
from functions.function import IFunction
'''
represents a exponentialFunction f(x)=ae^(bx)
'''
class ExponentialFunction(IFunction):
    def __init__(self,a,b):
        self.a=a
        self.b=b
    
    def f(self,x):
        return self.a*np.exp(self.b*x)
    
    def setA(self,value):
        self.a=value
    
    def setB(self,value):
        self.b=value 