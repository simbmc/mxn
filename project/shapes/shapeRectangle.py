'''
Created on 15.03.2016

@author: mkennert
'''
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.rectangleView import CSRectangleView
from shapes.ashape import AShape


class ShapeRectangle(GridLayout, AShape):
    
    '''
    represents a cross section which has the shape 
    of a rectangle
    '''
    
    # important components
    view, information = ObjectProperty(CSRectangleView()), ObjectProperty()
    layers, bars = ListProperty([]), ListProperty([])
    
    # important values
    ch, cw = NumericProperty(0.5), NumericProperty(0.25)
    
    # constructor
    def __init__(self, **kwargs):
        super(ShapeRectangle, self).__init__(**kwargs)
        self.view.csShape = self
    
