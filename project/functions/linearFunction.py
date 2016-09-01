'''
Created on 06.05.2016

@author: mkennert
'''
from functions.function import IFunction
from kivy.properties import NumericProperty

class Linear(IFunction):
    
    '''
    represents a linear function f(x)=ax
    '''
    
    # parameter a
    a = NumericProperty()
    
    
    '''
    constructor
    '''
    
    def __init__(self, a, minStrain, maxStrain, minStress, maxStress):
        self.a = a
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStress, maxStress
        self.points = [(minStrain, self.f(minStrain)), (maxStrain, self.f(maxStrain))]
    
    '''
    evaluate the linear-function by the parameters a
    '''
        
    def f(self, x):
        if x >= self.minStrain and x <= self.maxStrain:
            return self.a * x
        else:
            return 0
    
    '''
    return the String which represents the function
    '''
       
    def f_toString(self):
        return "f(x)=" + str(self.a) + "x"
