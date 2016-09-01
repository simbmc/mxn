'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from functions.quadraticFunction import QuadraticFunction
from materialLawEditor.quadraticFunctionInformation import QuadraticFunctionInformation
from materialLawEditor.quadraticFunctionView import QuadraticFunctionView
import numpy as np
from kivy.properties import  NumericProperty
from materialLawEditor.aeditor import AEditor

class QuadraticFunctionEditor(GridLayout, AEditor):
    
    '''
    QuadraticFunctionEditor is the main-component to create a quadratic-function. 
    it manages the communication between the quadratic-view and the quadratic-information.
    when the user confirm the created function f, the editor will set the function
    of the material-law to f
    '''
    
    # parameter a
    a = NumericProperty(1.)
    
    # parameter b
    b = NumericProperty(0.)
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(QuadraticFunctionEditor, self).__init__(**kwargs)
        self.cols = 2
        self.view = QuadraticFunctionView(editor=self)
        self.information = QuadraticFunctionInformation(editor=self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    eval the function on the x-value
    '''
    def f(self, x):
        return self.a * np.power(x, 2) + self.b * x 
    
    def confirm(self, btn):
        self.lawEditor.cancel_graphicShow()
        f = QuadraticFunction(self.a, self.b, self.lowerStrain, self.upperStrain, self.lowerStress, self.upperStress)
        self.create_function(f)
    

