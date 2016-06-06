'''
Created on 11.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial

class OwnMaterial(AMaterial):
    def __init__(self,name,price,density,stiffness,strength):
        super(OwnMaterial,self,).__init__(name, float(price),float(density),float(stiffness),float(strength))