'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from functions.quadraticFunction import QuadraticFunction
from materialLawEditor.quadraticFunctionInformation import QuadraticFunctionInformation
from materialLawEditor.quadraticFunctionView import QuadraticFunctionView
import numpy as np


class QuadraticFunctionEditor(GridLayout):
    # constructor

    def __init__(self, **kwargs):
        super(QuadraticFunctionEditor, self).__init__(**kwargs)
        self.cols = 2
        self.a = 1.
        self.b = 0.
        self.h = 10
        self.w = 10
        self.view = QuadraticFunctionView()
        self.view.sign_in(self)
        self.information = QuadraticFunctionInformation()
        self.information.sign_in(self)
        self.add_widget(self.view)
        self.add_widget(self.information)

    '''
    set the factor a
    '''

    def set_a(self, value):
        self.a = value
        self.view.update_points()

    '''
    set the factor b
    '''

    def set_b(self, value):
        self.b = value
        self.view.update_points()

    '''
    set the width
    '''

    def set_width(self, value):
        self.w = value
        self.view.graph.xmax = value
        self.view.graph.x_ticks_major = value / 5.
        self.view.update_points()

    '''
    set the height 
    '''

    def set_height(self, value):
        self.h = value
        self.view.graph.ymax = value
        self.view.graph.y_ticks_major = value / 5.
        self.view.update_points()

    '''
    eval the function on the x-value
    '''

    def f(self, x):
        return self.a * np.power(x, 2) + self.b * x 
    
    def confirm(self):
        self.lawEditor.cancel_graphicShow()
        f=QuadraticFunction(self.a,self.b)
        self.lawEditor.set_f(f)
        self.lawEditor.cancel_graphicShow()
        self.lawEditor.creater.cancel(None)
    
    def cancel(self):
        self.lawEditor.cancel_graphicShow()
    
    def sign_in(self,editor):
        self.lawEditor=editor
