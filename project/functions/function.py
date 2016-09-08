'''
Created on 06.05.2016

@author: mkennert
'''
from abc import abstractmethod

from kivy.properties import NumericProperty


class IFunction:
    # minimal strain of the function
    minStrain = NumericProperty()
    
    # maximal strain of the function
    maxStrain = NumericProperty()
    
    
    '''
    the subclasses of IFunction must implemented 
    a method f to eval the functionvalue
    '''
    @abstractmethod
    def f(self, x):
        raise NotImplemented('not implemented')
    
    '''
    return a string, which presents the function
    '''
    @abstractmethod
    def f_toString(self):
        raise NotImplemented('not implemented')
    
    
