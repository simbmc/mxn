'''
Created on 13.06.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from shapes.ashape import AShape
from crossSectionView.circleView import CSCircleView
from kivy.properties import NumericProperty, ObjectProperty, ListProperty

class ShapeCircle(GridLayout, AShape):
    
    '''
    represents the cross section which has the shape 
    of a circle
    '''
    
    # important components
    view, information = ObjectProperty(), ObjectProperty()
    layers, bars = ListProperty([]), ListProperty([])
    
    # important values
    d = NumericProperty(0.25)
    
    # Constructor
    def __init__(self, **kwargs):
        super(ShapeCircle, self).__init__(**kwargs)
        self.view = CSCircleView()
        self.view.csShape, self.view.d = self, self.d
        self.view.create_graph()
