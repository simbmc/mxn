'''
Created on 04.04.2016

@author: mkennert
'''
from functions.linear import Linear
from materials.amaterial import AMaterial


class GlassFiber(AMaterial):
    
    '''
    database for the material glassfiber
    '''
    
    def __init__(self):
        super(GlassFiber, self,).__init__('glass fiber', 2, 2660.,Linear(1, 0, 1))

