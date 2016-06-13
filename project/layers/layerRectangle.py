'''
Created on 14.04.2016

@author: mkennert
'''
from layers.aLayer import ALayer


class LayerRectangle(ALayer):
    # Constructor
    def __init__(self, x, y, h, w, colors):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.colors = colors
        self.focus = False
        self.filledRectCs=None
        self.filledRectAck=None
        
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    '''

    def mouseWithin(self, x, y):
        if y < self.filledRectAck.yrange[1] and y>self.filledRectAck.yrange[0]\
             and x < self.filledRectAck.xrange[1] and x>self.filledRectAck.xrange[0]:
            return True
        else:
            return False

    '''
    the method setHeight change the height of the small_keyboard-rectangle
    '''
    def setHeight(self, value):
        self.h = value


    '''
    the method setWidth change the width of the small_keyboard-rectangle
    '''
    def setWidth(self, value):
        self.w = value


    '''
    return the weight of the layer
    '''

    def getWeight(self):
        v = self.h * self.w
        w = self.material.density * v
        return w

    
    '''
    set the filledRectCs
    '''
    def setFilledRectCs(self, filledRect):
        self.filledRectCs=filledRect
    
    '''
    set the filledRectAck
    '''
    def setFilledRectAck(self, filledRect):
        self.filledRectAck=filledRect
    
    '''
    set the yrange
    '''
    def setYRange(self,values):
        self.filledRectAck.yrange=values
        self.filledRectCs.yrange=values