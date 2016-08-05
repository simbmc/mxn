'''
Created on 15.03.2016

@author: mkennert
'''


from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.rectangleView import CSRectangleView
from shapes.ashape import AShape


class ShapeRectangle(GridLayout, AShape):
    cw,ch=NumericProperty(0.5), NumericProperty(0.25)
    view,information=ObjectProperty(CSRectangleView()),ObjectProperty()
    
    # constructor
    def __init__(self, **kwargs):
        super(ShapeRectangle, self).__init__(**kwargs)
        self.view.csShape=self

    '''
    the method update_height changes the height of the view
    '''
 
    def update_height(self, value):
        self.view.update_height(value)
        self.ch = value

    '''
    the method update_width change the width of the view
    '''

    def update_width(self, value):
        self.view.update_width(value)
        self.cw = value

    '''
    sign in by the cross section
    '''

    def sign_parent(self, crossSection):
        self.allCrossSection = crossSection
        self.information = crossSection.get_information()
