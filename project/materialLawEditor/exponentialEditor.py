'''
Created on 09.09.2016

@author: mkennert
'''
from materialLawEditor.aeditor import AEditor
from kivy.properties import  NumericProperty
from materialLawEditor.exponentialView import ExponentialView
from materialLawEditor.exponentialInformation import ExponentialInformation
import numpy as np
from functions.exponential import Exponential
from kivy.uix.gridlayout import GridLayout

class ExponentialEditor(GridLayout, AEditor):
    
    '''
    ExponentialEditor is the main-component to create a exponential-function. 
    it manages the communication between the exponential-view and the exponential-information.
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
        super(ExponentialEditor, self).__init__(**kwargs)
        self.cols = 2
        self.view = ExponentialView(editor=self)
        self.information = ExponentialInformation(editor=self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    evaluate the function on the x-value.
    f(x)=a*exp(bx)-a
    '''
    def f(self, x):
        return self.a * np.exp(self.b * x) - self.a 
    
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
        f = Exponential(self.a, self.b, self.minStrain, self.maxStrain)
        self.create_function(f)
    
