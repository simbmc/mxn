'''
Created on 03.05.2016
@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from functions.multilinear import Multilinear
from materialLawEditor.mulitlinearInformation import MultilinearInformation
from materialLawEditor.multilinearView import MultilinearView
from ownComponents.design import Design
from kivy.properties import NumericProperty
from materialLawEditor.aeditor import AEditor

class MultilinearEditor(GridLayout, AEditor):
    
    '''
    MultilinearEditor is the main-component to create a multilinear-function. 
    it manages the communication between the multilinear-view and the multilinear-information.
    when the user confirm the created function f, the editor will set the function
    of the material-law to f
    '''
    
    # number of points
    _points = NumericProperty(5)
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(MultilinearEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.information = MultilinearInformation(editor=self)
        self.view = MultilinearView(editor=self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    update the complete information by the given function-properties
    '''
        
    def update_function(self, points, minStress, maxStress, minStrain, maxStrain):
        self.minStrain = minStrain
        self.maxStrain = maxStrain
        self.lowerStress = minStress
        self.upperStress = maxStress
        self.information.update_function(points, minStress, maxStress, minStrain, maxStrain)
        self.view.update_function(points, minStrain, maxStrain)

    '''
    confirm the material-law and set the function f in the material-editor-class
    '''
        
    def confirm(self, btn):
        x, y = self.view.get_coordinates()
        f = Multilinear(x, y, self.minStrain, self.maxStrain, self.lowerStress, self.upperStress)
        self.create_function(f)

