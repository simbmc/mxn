'''
Created on 15.03.2016

@author: mkennert
'''
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.rectangleView import CSRectangleView
from shapes.ashape import AShape


class ShapeRectangle(GridLayout, AShape):
    
    '''
    represents a cross section which has the shape 
    of a rectangle
    '''
    
    # cross-section-view
    view = ObjectProperty(CSRectangleView())
    
    # information-view of the cross-section-rectangle
    information = ObjectProperty()
    
    # height of the cross-section
    ch = NumericProperty(0.5)
    
    # width of the cross-section
    cw = NumericProperty(0.25)
    
    # constructor
    def __init__(self, **kwargs):
        super(ShapeRectangle, self).__init__(**kwargs)
        self.view.csShape = self
        self.view.create_graph()
    
    '''
    y distance of gravity centre from upper rim
    '''
    def _get_gravity_centre(self):
        return self.ch / 2.
    
    '''
    returns width of cross section for different vertical coordinates
    '''
    def get_width(self, y):
        return self.cw
