'''
Created on 16.03.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty

class AMaterial(object):
    #Constructor
    def __init__(self, name, price, density,f):
        self.name=str(name)
        self.price=float(price)
        self.density=float(density)
        self.material_law=f
    
    
    
    
        