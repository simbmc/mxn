'''
Created on 13.09.2016

@author: mkennert
'''
from kivy.properties import  NumericProperty
from kivy.uix.gridlayout import GridLayout

from functions.logarithm import Logarithm
from materialLawEditor.aeditor import AEditor
from materialLawEditor.logarithmInformation import LogarithmInformation
from materialLawEditor.logarithmView import LogarithmView
import numpy as np


class LogarithmEditor(GridLayout, AEditor):
    
    '''
    LogarithmEditor is the main-component to create a logarithm-function. 
    it manages the communication between the logarithm-view and the logarithm-information.
    when the user confirm the created function f, the editor will set the function
    of the material-law to f
    '''
    
    # parameter a
    a = NumericProperty(1)
    
    # parameter b
    b = NumericProperty(0.5)
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(LogarithmEditor, self).__init__(**kwargs)
        self.cols = 2
        self.view = LogarithmView(editor=self)
        self.information = LogarithmInformation(editor=self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    evaluate the logarithm-function by the parameters a and b
    '''
    
    def f(self, x):
            return np.log((x + self.a) / self.a) / self.b
        
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
        f = Logarithm(self.a, self.b, self.minStrain, self.maxStrain)
        self.create_function(f)
    
