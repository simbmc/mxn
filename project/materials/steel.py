'''
Created on 04.04.2016

@author: mkennert
'''
from functions.linear import Linear
from materials.amaterial import AMaterial


class Steel(AMaterial):
    
    '''
    database for the material steel
    '''
    
    # constructor
    def __init__(self):
        super(Steel, self,).__init__('steel', 0.35, 7850., Linear(500, -0.3, 0.3))
    
