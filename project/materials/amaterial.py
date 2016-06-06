'''
Created on 16.03.2016

@author: mkennert
'''
class AMaterial(object):
    #Constructor
    def __init__(self, name, price, density,stiffness, strength):
        self.name=str(name)
        self.price=float(price)
        self.density=float(density)
        self.stiffness=float(stiffness)
        self.strength=float(strength)

    
    
    
    
        