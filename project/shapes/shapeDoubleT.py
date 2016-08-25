'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.doubleTView import DoubleTView
from shapes.ashape import AShape


class ShapeDoubleT(GridLayout, AShape):
    
    '''
    represents a cross section which has the doubleT- or I-Shape
    '''
    
    # important components
    view = ObjectProperty(DoubleTView())
    information = ObjectProperty()
    layers, bars = ListProperty([]), ListProperty([])
    
    # important values
    tw, th = NumericProperty(0.3), NumericProperty(0.2)  # top-area
    mw, mh = NumericProperty(0.1), NumericProperty(0.25)  # middle-area
    bw, bh = NumericProperty(0.3), NumericProperty(0.2)  # bottom-area
    
    # constructor
    def __init__(self, **kwargs):
        super(ShapeDoubleT, self).__init__(**kwargs)
        self.cols = 2
        self.view.csShape = self
        self.view.create_graph()

    '''
    return the cs-height
    '''

    def get_total_height(self):
        return self.th + self.bh + self.mh

    '''
    return the max-width
    '''

    def get_max_width(self):
        wmax = self.tw
        if wmax < self.mw:
            wmax = self.mw
        if wmax < self.bw:
            wmax = self.bw
        return wmax


