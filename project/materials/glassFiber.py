'''
Created on 04.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial

class GlassFiber(AMaterial):
    def __init__(self):
        super(GlassFiber,self,).__init__('glass fiber', 2,2660.,50000.,1000.)

