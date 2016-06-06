'''
Created on 04.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial

class CarbonFiber(AMaterial):
    def __init__(self):
        super(CarbonFiber,self,).__init__('carbon fiber', 20,1600.,250000.,1600.)

