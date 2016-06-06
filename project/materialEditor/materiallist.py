'''
Created on 18.04.2016

@author: mkennert
'''
from materials.steel import Steel
from materials.carbonFiber import CarbonFiber
from materials.concrete import Concrete
from materials.glassFiber import GlassFiber

'''
the class MaterialList was developed to make it possible
to use only one materiallist and update the observerclasses
when something has changed. the class implements the observer-pattern.
Attention: if you add a new observer, make sure that the observer
implements a update-method.
'''

class MaterialList:
    #constuctor
    def __init__(self):
        self.allMaterials=[Steel(),CarbonFiber(),Concrete(),GlassFiber()]
        self.listeners=[]
     
    '''
    update all listeners when a new material was added
    '''
    def update(self):
        for listener in self.listeners:
            listener.update()
    
    '''
    add observer to the listeners-list.
    '''
    def addListener(self,listener):
        self.listeners.append(listener)
    
    '''
    add a new material in the materiallist and 
    update all listeners
    '''
    def addMaterial(self, material):
        self.allMaterials.append(material)
        self.update()
    
    '''
    return the length of the materiallist
    '''
    def getLength(self):
        return len(self.allMaterials)