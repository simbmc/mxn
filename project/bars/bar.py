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
    set the ellipse
    '''
    def set_filled_ellipse(self,ellipse):
        self.ellipse=ellipse
    
    '''
    proofs whether the mouse in the ellipse
    ''' 
    def mouse_within(self,x,y):
        print('x: '+str(x))
        print('xrange: '+str(self.ellipse.xrange))
        print('y: '+str(x))
        print('yrange: '+str(self.ellipse.yrange))
        if x>self.ellipse.xrange[0] and x<self.ellipse.xrange[1] and \
            y>self.ellipse.yrange[0] and y<self.ellipse.yrange[1]:
            return True
        else:
            return False