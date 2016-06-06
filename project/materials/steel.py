'''
Created on 04.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial

class Steel(AMaterial):
    def __init__(self):
        super(Steel,self,).__init__('steel', 0.35,7850.,210000.,350.)
    