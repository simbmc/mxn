'''
Created on 03.06.2016

@author: mkennert
'''
from layers.aLayer import ALayer


class LayerT(ALayer):
    # Constructor

    def __init__(self, h1, h2, w1, w2, colors, percent):
        self.h1 = h1
        self.w1 = w1
        self.h2 = h2
        self.w2 = w2
        self.colors = colors
        self.focus = False
        self.percent = percent
    
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    '''

    def mouseWithin(self, x, y):
        # check whether the coordinates are in the first rectangle
        if y < self.r1.yrange[1] and y > self.r1.yrange[0] \
                and x > self.r1.xrange[0] and x < self.r1.xrange[1]:
            return True
        # check whether the coordinate are in the second rectangle
        elif y < self.r2.yrange[1] and y > self.r2.yrange[0] \
                and x > self.r2.xrange[0] and x < self.r2.xrange[1]:
            return True
        else:
            return False
    
    '''
    the method set_height change the height of the first rectangle
    '''

    def setHeight1(self, value):
        self.h1 = value

    '''
    the method set_width change the width of the the first rectangle
    '''

    def setWidth1(self, value):
        self.w1 = value

    '''
    the method set_height change the height of the first rectangle
    '''

    def setHeight2(self, value):
        self.h2 = value

    '''
    the method set_width change the width of the the first rectangle
    '''

    def setWidth2(self, value):
        self.w2 = value
    
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    Attention: it checks only the x_coordinate. this method
    was developed to make the the movement of the layer faster
    '''

    def mouseWithinX(self, x):
        if x > self.r1.xrange[0] and x < self.r1.xrange[1]:
            return True
        elif x > self.r2.xrange[0] and x < self.r2.xrange[1]:
            return True
        else:
            return False
    
    '''
    set the rectangle 1
    '''

    def setFilledRect1(self, filledRect):
        self.r1 = filledRect

    '''
    set the rectangle 2
    '''

    def setFilledRect2(self, filledRect):
        self.r2 = filledRect

    '''
    set the color
    '''

    def setColor(self, color):
        self.r1.color = color
        self.r2.color = color

    '''
    reset the focus-color
    '''

    def resetColor(self):
        self.r1.color = self.colors
        self.r2.color = self.colors

    '''
    set the yrange of the rectangle 1
    '''

    def setYRange1(self, values):
        self.r1.yrange = values

    '''
    set the xrange of the rectangle 1
    '''

    def setXRange1(self, values):
        self.r1.xrange = values

    '''
    set the yrange of the rectangle 2
    '''

    def setYRange2(self, values):
        self.r2.yrange = values

    '''
    set the xrange of the rectangle 2
    '''

    def setXRange2(self, values):
        self.r2.xrange = values

    '''
    return the total height of the layer
    '''

    def getHeight(self):
        return (self.r1.yrange[1] - self.r1.yrange[0] + self.r2.yrange[1] - self.r2.yrange[0])

    '''
    return the size of the layer. its important for the calculation, when you need 
    the percent of the layer in the cross section
    '''

    def getSize(self):
        return (self.r1.yrange[1] - self.r1.yrange[0]) * (self.r1.xrange[1] - self.r1.xrange[0]) \
            + (self.r2.yrange[1] - self.r2.yrange[0]) * (self.r2.xrange[1] - self.r2.xrange[0]) \


    '''
    return the weight of the layer
    '''

    def getWeight(self):
        volume = (self.r1.yrange[1] - self.r1.yrange[0]) * (self.r1.xrange[1] - self.r1.xrange[0]) +\
                 (self.r2.yrange[1] - self.r2.yrange[0]) * \
            (self.r2.xrange[1] - self.r2.xrange[0])
        weight = self.material.density * volume
        return weight
