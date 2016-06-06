'''
Created on 11.05.2016

@author: mkennert
'''
from abc import abstractmethod

class IObserver:
    '''
    update the gui when the materiallist
    has changed
    '''
    @abstractmethod
    def update(self):
        raise NotImplemented('not implemented')