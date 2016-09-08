'''
Created on 01.09.2016

@author: mkennert
'''
from kivy.properties import  ObjectProperty, NumericProperty


class AEditor:
    
    '''
    base class of the function-editors
    '''
    
    # law-editor
    lawEditor = ObjectProperty()
    
    # view-component where you can see 
    view = ObjectProperty()
    
    # information-component where you can edit the function
    information = ObjectProperty()    
    
    # upper strain limit 
    maxStrain = NumericProperty(1.)
    
    # upper stress limit 
    upperStress = NumericProperty(1.)
    
    # lower strain limit
    minStrain = NumericProperty(0.)
    
    # lower stress limit
    lowerStress = NumericProperty(0.)
    
    '''
    set the function f in the material-editor-class
    '''
    
    def create_function(self, f):
        self.lawEditor.f = f
        self.lawEditor.creater.materialLaw.text = f.f_toString()
        self.lawEditor.creater.update_graph(self.minStrain,self.maxStrain, f.points)
        self.lawEditor.cancel_graphicShow()
        self.lawEditor.creater.close_material_law_editor(None)
    
    '''
    cancel the selection where you can select the function-type
    of the material-law
    '''
    
    def cancel(self, btn):
        self.lawEditor.cancel_graphicShow()