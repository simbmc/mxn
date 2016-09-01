'''
Created on 03.05.2016

@author: mkennert
'''
from kivy.properties import  NumericProperty
from kivy.uix.gridlayout import GridLayout

from functions.linearFunction import Linear
from materialLawEditor.linearInformation import LinearInformation
from materialLawEditor.linearView import LinearView
from ownComponents.design import Design
from materialLawEditor.aeditor import AEditor


class LinearEditor(GridLayout, AEditor):
    
    '''
    LinearEditor is the main-component to create a linear-function. 
    it manages the communication between the linear-view and the linear-information.
    when the user confirm the created function f, the editor will set the function
    of the material-law to f
    '''
    
    # parameter a
    a = NumericProperty(1.)
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(LinearEditor, self).__init__(**kwargs)
        self.cols , self.spacing = 2, Design.spacing
        self.view = LinearView(editor=self)
        self.information = LinearInformation(editor=self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    confirm the material-law and set the function f in the material-editor-class
    '''
    def confirm(self, btn):
        f = Linear(self.a, self.lowerStrain, self.upperStrain, self.lowerStress, self.upperStress)
        self.create_function(f)
