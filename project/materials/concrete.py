'''
Created on 04.04.2016

@author: mkennert
'''
from functions.linear import Linear
from materials.amaterial import AMaterial


class Concrete(AMaterial):
    
    '''
    database for the material concrete
    '''
    
    # constructor
    def __init__(self):
        super(Concrete, self,).__init__('concrete', 0.065, 2300.,Linear(100., -0.2, 0.))


        
