'''
Created on 03.05.2016
@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from functions.multilinear import Multilinear
from materialLawEditor.mulitlinearInformation import MultilinearInformation
from materialLawEditor.multilinearView import MultilinearView
from ownComponents.design import Design
from kivy.properties import  ObjectProperty, NumericProperty

class MultilinearEditor(GridLayout):
    
    '''
    MultilinearEditor is the main-component to create a multilinear-function. 
    it manages the communication between the multilinear-view and the multilinear-information.
    when the user confirm the created function f, the editor will set the function
    of the material-law to f
    '''
    
    # important components
    lawEditor = ObjectProperty()
    
    # important values
    upperStrain, upperStress = NumericProperty(50.), NumericProperty(50.)
    lowerStrain, lowerStress = NumericProperty(0.), NumericProperty(0.)
    _points = NumericProperty(5)
    
    # constructor
    def __init__(self, **kwargs):
        super(MultilinearEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.information = MultilinearInformation(editor=self)
        self.view = MultilinearView(editor=self)
        self.add_widget(self.view)
        self.add_widget(self.information)


    # not finished yet
    def confirm(self, btn):
        x, y = self.view.get_coordinates()
        f = Multilinear(x, y, self.lowerStrain, self.upperStrain, self.lowerStress, self.upperStress)
        self.lawEditor.f = f
        self.lawEditor.creater.update_graph(self.lowerStress, self.upperStress, self.lowerStrain,
                                            self.upperStrain, f.points)
        self.lawEditor.creater.materialLaw.text = f.f_toString()
        self.lawEditor.cancel_graphicShow()
        self.lawEditor.creater.close_material_law_editor(None)

    '''
    cancel the selection where you can select the function-type
    of the material-law
    '''
    
    def cancel(self, btn):
        self.lawEditor.cancel_graphicShow()
