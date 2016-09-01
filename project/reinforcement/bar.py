'''
Created on 21.06.2016

@author: mkennert
'''

from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty

class Bar:
    
    '''
    represents the layer in the cross-sections
    '''
        
    # x-coordinate of the bar
    x = NumericProperty()
    
    # y-coordinate of the bar
    y = NumericProperty()
    
    # cross-section-area
    csArea = NumericProperty()
    
    # material of the bar
    material = ObjectProperty()
    
    # boolean to save whether the bar has the focus
    focus = BooleanProperty(False)
    
    # filled-ellipse to represent the bar in the view
    ellipse = ObjectProperty()
    
    '''
    constructor
    '''
    
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
