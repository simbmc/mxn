'''
Created on 21.06.2016

@author: mkennert
'''


class Bar:
    # Constructor

    def __init__(self, x, y):
        self.x = x
        self.y = y

    '''
    the method set_height change the height of the small_keyboard-rectangle
    '''

    def set_height(self, value):
        self.h = value

    '''
    return the weight of the layer
    '''

    def get_weight(self):
        v = self.h * self.w
        w = self.material.density * v
        return w

    '''
    set the material
    '''

    def set_Material(self, material):
        self.material = material

    '''
    return the strain of the layer
    '''

    def get_strain(self):
        return self.material.strength / self.material.stiffness
