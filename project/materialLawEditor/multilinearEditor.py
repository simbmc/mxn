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
        self.lawEditor.creater.cancel(None)

    # not finished yet
    def cancel(self, btn):
        self.lawEditor.cancel_graphicShow()
