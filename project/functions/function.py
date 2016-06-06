'''
Created on 06.05.2016

@author: mkennert
'''
from abc import abstractmethod

class IFunction:
    '''
    the subclasses of IFunction must implemented 
    a method f to eval the functionvalue
    '''
    @abstractmethod
    def f(self,x):
        raise NotImplemented('not implemented')
    