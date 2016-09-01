'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.doubleTView import DoubleTView
from shapes.ashape import AShape


class ShapeDoubleT(GridLayout, AShape):
    
    '''
    represents a cross section which has the doubleT- or I-Shape
    '''
    
    # cross-section-view
    view = ObjectProperty(DoubleTView())
    
    # information-view of the cross-section-rectangle
    information = ObjectProperty()
    
    # width of the top rectangle
    tw = NumericProperty(0.3)
    
    # height of the top rectangle
    th = NumericProperty(0.2)  
    
    # width of the middle rectangle
    mw = NumericProperty(0.1)
    
    # height of the middle rectangle
    mh = NumericProperty(0.25)
    
    # width of the bottom rectangle
    bw = NumericProperty(0.3)
    
    # height of the bottom rectangle
    bh = NumericProperty(0.2)
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(ShapeDoubleT, self).__init__(**kwargs)
        self.cols = 2
        self.view.csShape = self
        self.view.create_graph()

    '''
    return the total height of the cross-section
    '''

    def get_total_height(self):
        return self.th + self.bh + self.mh

    '''
    return the total width of the cross-section
    '''

    def get_max_width(self):
        wmax = self.tw
        if wmax < self.mw:
            wmax = self.mw
        if wmax < self.bw:
            wmax = self.bw
        return wmax
    
    '''
    y distance of gravity centre from upper rim
    '''
   
    def _get_gravity_centre(self):
        h = self.get_total_height()
        A_up, z_up = self.tw * self.th, self.th / 2
        A_lo, z_lo = self.bw * self.bh, h - self.bh / 2
        A_st, z_st = self.mw * self.mh, (h + self.th - self.bh) / 2
        return (A_up * z_up + A_lo * z_lo + A_st * z_st) / (A_up + A_lo + A_st)
    
    '''
    returns width of cross section for different vertical coordinates
    '''
   
    def get_width(self, y):
        if y < self.bh:
            return self.bw
        elif y <= self.bh + self.mh:
            return self.mw
        else:
            return self.tw
