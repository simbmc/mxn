'''
Created on 14.04.2016

@author: mkennert
'''

from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty


class Layer:
    
    '''
    represents the layer in the cross-sections
    '''
    
    # material of the layer
    material = ObjectProperty()
    
    # line to represent the layer in the view
    line = ObjectProperty()
    
    # x-coordinate of the layer
    x = NumericProperty()
    
    # y-coordinate of the layer
    y = NumericProperty()
    
    # width of the layer
    w = NumericProperty()
    
    # height of the layer
    h = NumericProperty()
    
    # # boolean to save whether the layer has the focus
    focus = BooleanProperty(False)
    
    '''
    constructor
    '''
    
    def __init__(self, y, h, w):
        self.y = y
        self.w = w
        self.h = h
    
    '''
    proofs whether the coordinates are in the area of the line. 
    d is the tolerance of the distance
    '''
    
    def mouse_within(self, y, d):
        if y - d < self.y and y > self.y:
            return True
        else:
            return False
