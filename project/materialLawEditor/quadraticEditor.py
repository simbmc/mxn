'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from functions.quadratic import Quadratic
from materialLawEditor.quadraticInformation import QuadraticInformation
from materialLawEditor.quadraticView import QuadraticFunctionView
import numpy as np
from kivy.properties import  NumericProperty
from materialLawEditor.aeditor import AEditor

class QuadraticEditor(GridLayout, AEditor):
    
    '''
    QuadraticEditor is the main-component to create a quadratic-function. 
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
        super(QuadraticEditor, self).__init__(**kwargs)
        self.cols = 2
        self.view = QuadraticFunctionView(editor=self)
        self.information = QuadraticInformation(editor=self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    evaluate the function on the x-value
    '''
    def f(self, x):
        return self.a * np.power(x, 2) + self.b * x 
    
    '''
    update the complete information and graph by the given function-properties
    '''
        
    def update_function(self, points, minStrain, maxStrain, a, b):
        self.minStrain = minStrain
        self.maxStrain = maxStrain
        self.a = a
        self.b = b
        self.information.update_function(points, minStrain, maxStrain, a, b)
        self.view.update_function(points, minStrain, maxStrain)
    
    '''
    confirm the material-law and set the function f in the material-editor-class
    '''
   
    def confirm(self, btn):
        self.lawEditor.cancel_graphicShow()
        f = Quadratic(self.a, self.b, self.minStrain, self.maxStrain)
        self.create_function(f)