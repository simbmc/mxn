'''
Created on 11.05.2016

@author: mkennert
'''
from abc import abstractmethod

class IObserver:
    
    '''
    iobserver must implement by the components, which contains
    the materiallist. so when the materiallist has changed the 
    oberserver must update the view
    '''
    
    @abstractmethod
    def update(self):
        # update the gui when the materiallist
        # has changed 
        raise NotImplemented('not implemented')