'''
Created on 03.06.2016

@author: mkennert
'''
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
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
    layers, bars = ListProperty([]), ListProperty([])
    
    # important values
    tw, th = NumericProperty(0.3), NumericProperty(0.15)  # top-area
    bw, bh = NumericProperty(0.15), NumericProperty(0.3)  # bottom-area
    
    # constructor
    def __init__(self, **kwargs):
        super(ShapeT, self).__init__(**kwargs)
        self.cols = 2
        self.view.csShape = self
        self.view.create_graph()

    '''
    return the cs-height
    '''

    def get_total_height(self):
        return self.th + self.bh

    '''
    return the max-width
    '''

    def get_max_width(self):
        if self.tw < self.bw:
            return self.bw
        else:
            return self.tw
