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
    
    # important values
    a = NumericProperty()
    minStrain, maxStrain = NumericProperty(), NumericProperty()
    minStress, maxStress = NumericProperty(), NumericProperty()
    
    # constructor
    def __init__(self, a, minStrain, maxStrain, minStress, maxStress):
        self.a = a
        self.minStrain, self.maxStrain = minStrain, maxStrain
        self.minStress, self.maxStress = minStress, maxStress
        self.points = [(minStress, self.f(minStress)), (maxStress, self.f(maxStress))]
    
    '''
    eval the linear-function by the parameters a
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
