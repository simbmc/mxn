'''
Created on 03.05.2016
@author: mkennert
'''
# version 120
from kivy.uix.gridlayout import GridLayout

from functions.multilinear import Multilinear
from materialLawEditor.mulitlinearInformation import MultilinearInformation
from materialLawEditor.multilinearView import MultilinearView
from ownComponents.design import Design


class MultilinearEditor(GridLayout):
    # constructor
    def __init__(self, **kwargs):
        super(MultilinearEditor, self).__init__(**kwargs)
        self.cols = 2
        self.spacing=Design.spacing
        self.h = 50.
        self.w = 50.
        self.lowerStrain=0.
        self.lowerStress=0.
        self._points = 5
        self.information = MultilinearInformation()
        self.view = MultilinearView()
        self.information.sign_in(self)
        self.view.sign_in(self)
        self.add_widget(self.view)
        self.add_widget(self.information)

    '''
    set the width of the graph
    '''

    def update_width(self, value):
        self.w = value
        self.view.update_width()

    '''
    set the height of the graph
    '''

    def update_height(self, value):
        self.h = value
        self.view.update_height()
        
    '''
    update the lower stress in the view
    '''
    def update_lower_stress(self,value):
        self.lowerStress=value
        self.view.update_lower_stress(value)
    
    '''
    update the lower strain in the view
    '''
    def update_lower_strain(self,value):
        self.lowerStrain=value
        self.view.update_lower_strain(value)
        
    '''
    set the numbers of points which the graph should have
    '''

    def set_points(self, value):
        self._points = value
        self.view.update_points()

    '''
    return the number of points
    '''

    def get_points(self):
        return self._points

    # not finished yet
    def update_coordinates(self, x, y):
        self.information.update_coordinates(x, y)

    # not finished yet
    def update_point_position_x(self, x):
        return self.view.update_point_position_x(x)

    # not finished yet
    def update_point_position_y(self, y):
        self.view.update_point_position_y(y)

    # not finished yet
    def confirm(self):
        x, y = self.view.get_coordinates()
        f = Multilinear(x, y,self.lowerStrain,self.h,self.lowerStress,self.w)
        self.lawEditor.set_f(f)
        self.lawEditor.cancel_graphicShow()
        self.lawEditor.creater.cancel(None)

    # not finished yest
    def cancel(self):
        self.lawEditor.cancel_graphicShow()

    def sign_in(self, editor):
        self.lawEditor = editor
