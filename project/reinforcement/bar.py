'''
Created on 21.06.2016

@author: mkennert
'''

from kivy.properties import NumericProperty, ObjectProperty

class Bar:
    
    '''
    represents the layer in the cross-sections
    '''
    
    # important components
    material, ellipse = ObjectProperty(), ObjectProperty()
    
    # important values
    x, y = NumericProperty(), NumericProperty()
    focus = False
    
    # constructor
    def __init__(self, x, y, csArea):
        self.x = x
        self.y = y
        self.csArea = csArea
    
    '''
    proofs whether the mouse in the ellipse. if the coordinates of the mouse/touch
    are in the ellipse the method return true, else return false
    ''' 
    def mouse_within(self, x, y):
        if x > self.ellipse.xrange[0] and x < self.ellipse.xrange[1] and \
            y > self.ellipse.yrange[0] and y < self.ellipse.yrange[1]:
            return True
        else:
            return False
