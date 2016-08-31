'''
Created on 03.06.2016

@author: mkennert
'''
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.tView import TView
from shapes.ashape import AShape


class ShapeT(AShape, GridLayout):
    
    '''
    represents a cross section which has the shape 
    of a T
    '''
    
    # important components
    view = ObjectProperty(TView())
    
    # width of the top rectangle
    tw = NumericProperty(0.3)
    
    # height of the top rectangle
    th = NumericProperty(0.15) 
    
    # width of the bottom rectangle
    bw = NumericProperty(0.15)
    
    # height of the bottom rectangle
    bh = NumericProperty(0.3)  # bottom-area
    
    # constructor
    def __init__(self, **kwargs):
        super(ShapeT, self).__init__(**kwargs)
        self.cols = 2
        self.view.csShape = self
        self.view.create_graph()

    '''
    return the total height of the cross-section
    '''

    def get_total_height(self):
        return self.th + self.bh

    '''
    return the total width of the cross-section
    '''

    def get_max_width(self):
        if self.tw < self.bw:
            return self.bw
        else:
            return self.tw
    
    '''
    y distance of gravity centre from upper rim
    '''
   
    def _get_gravity_centre(self):
        h = self.get_total_height()
        At, yt = self.tw * self.th, self.th / 2
        Ab, yb = self.bw * self.bh, h - self.bh / 2
        return (At * yt + Ab * yb) / (At + Ab) 
    
    '''
    returns width of cross section for different vertical coordinates
    '''
   
    def get_width(self, y):
        if y < self.bh:
            return self.bw
        else:
            return self.tw