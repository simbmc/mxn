'''
Created on 13.06.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from shapes.ashape import AShape
from crossSectionView.circleView import CSCircleView
from kivy.properties import NumericProperty, ObjectProperty

class ShapeCircle(GridLayout, AShape):
    d = NumericProperty(0.25)
    view, information = ObjectProperty(), ObjectProperty()
    
    # Constructor
    def __init__(self, **kwargs):
        super(ShapeCircle, self).__init__(**kwargs)
        self.view = CSCircleView()
        self.view.csShape,self.view.d=self,self.d
        self.view.create_graph()

    '''
    get all the layers
    '''
    def get_layers(self):
        return self.view.get_layers()
