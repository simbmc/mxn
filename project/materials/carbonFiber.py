'''
Created on 04.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial
from functions.linearFunction import Linear

class CarbonFiber(AMaterial):
    '''
    database for the material carbonfiber
    '''
    def __init__(self):
        super(CarbonFiber, self,).__init__('carbon fiber', 20, 1600.,Linear(1, 0, 1))
