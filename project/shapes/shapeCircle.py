'''
Created on 13.06.2016

@author: mkennert
'''
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.circleView import CSCircleView
from shapes.ashape import AShape
import numpy as np

class ShapeCircle(GridLayout, AShape):
    
    '''
    represents the cross section which has the shape 
    of a circle
    '''
    
    # cross-section-view
    view = ObjectProperty(CSCircleView())
    
    # information-view of the cross-section
    information = ObjectProperty()
    
    # diameter of the circle
    d = NumericProperty(0.25)
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(ShapeCircle, self).__init__(**kwargs)
        self.view = CSCircleView()
        self.view.csShape, self.view.d = self, self.d
        self.view.create_graph()
    
    '''
    y distance of gravity centre from upper rim
    '''
        
    def _get_gravity_centre(self):
        return self.d / 2.
    
    '''
    returns width of cross section for different vertical coordinates
    '''
   
    def get_width(self, y):
        x1 = -np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
        x2 = np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
        return x2 - x1
