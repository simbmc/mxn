'''
Created on 14.04.2016

@author: mkennert
'''

from kivy.properties import NumericProperty, ObjectProperty


class Layer:
    
    '''
    represents the layer in the cross-sections
    '''
    
    # important components
    material, line = ObjectProperty(), ObjectProperty()
    
    # important values
    x, y = NumericProperty(), NumericProperty()
    w, h = NumericProperty(), NumericProperty()  # h=csArea
    focus = False
    
    # constructor
    def __init__(self, y, h, w):
        self.y = y
        self.w = w
        self.h = h
    
    '''
    proofs whether the coordinates are in the area of the line. 
    d is the tolerance of the distance
    '''
    def mouse_within(self, y, d):
        if y - d < self.y and y + d > self.y:
            return True
        else:
            return False
