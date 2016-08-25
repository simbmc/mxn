'''
Created on 16.03.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty

class AMaterial(object):
    
    '''
    baseclass for the materials. when you add more materials, 
    make sure that you call the constructor of this base-class
    '''
    
    #constructor
    def __init__(self, name, price, density,f):
        self.name=str(name)
        self.price=float(price)
        self.density=float(density)
        self.materialLaw=f
    
    
    
    
        