'''
Created on 03.05.2016

@author: mkennert
'''
from kivy.properties import  ObjectProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout

from functions.linearFunction import Linear
from materialLawEditor.linearInformation import LinearInformation
from materialLawEditor.linearView import LinearView
from ownComponents.design import Design


class LinearEditor(GridLayout):
    
    '''
    LinearEditor is the main-component to create a linear-function. 
    it manages the communication between the linear-view and the linear-information.
    when the user confirm the created function f, the editor will set the function
    of the material-law to f
    '''
    
    # important components
    view = ObjectProperty()
    information = ObjectProperty()
    lawEditor = ObjectProperty()
    f = ObjectProperty()
    
    # important values
    upperStrain, upperStress = NumericProperty(10.), NumericProperty(10.)
    lowerStrain, lowerStress = NumericProperty(0.), NumericProperty(0.)
    a = NumericProperty(1.)
    
    # constructor
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
        self.lawEditor.f = f
        self.lawEditor.creater.materialLaw.text = f.f_toString()
        self.lawEditor.creater.update_graph(self.lowerStress, self.upperStress, self.lowerStrain,
                                            self.upperStrain, f.points)
        self.lawEditor.cancel_graphicShow()
        self.lawEditor.creater.close_material_law_editor(None)
    
    '''
    cancel the selection where you can select the function-type
    of the material-law
    '''
    def cancel(self, btn):
        self.lawEditor.cancel_graphicShow()
    
    '''
    update the complete information and graph by the given function-properties
    '''
    def update_function(self, points, minStress, maxStress, minStrain, maxStrain, a):
        self.lowerStress = minStress
        self.upperStress = maxStress
        self.lowerStrain = minStrain
        self.upperStrain = maxStrain
        self.information.update_function(points, minStress, maxStress, minStrain, maxStrain, a)
        self.view.update_function(points, minStress, maxStress, minStrain, maxStrain)
