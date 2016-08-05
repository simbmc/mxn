'''
Created on 03.05.2016

@author: mkennert
'''
from functions.linearFunction import Linear
from ownComponents.design import Design

'''
f(x)=ax+b
'''

from kivy.uix.gridlayout import GridLayout

from materialLawEditor.linearInformation import LinearInformation
from materialLawEditor.linearView import LinearView


class LinearEditor(GridLayout):
    # constructor
    
    def __init__(self, **kwargs):
        super(LinearEditor, self).__init__(**kwargs)
        self.cols = 2
        self.spacing=Design.spacing
        self.a = 1
        self.upperStrain=10
        self.upperStress=10
        self.lowerStrain=0
        self.lowerStress=0
        self.view = LinearView()
        self.view.sign_in(self)
        self.information = LinearInformation()
        self.information.sign_in(self)
        self.add_widget(self.view)
        self.add_widget(self.information)

    def update_btn(self, value):
        self.a=value
        self.information.update_btn(value)

    def update_graph(self, value):
        self.a = value
        self.view.update_graph(value)

    def update_strain_upper_limit(self, value):
        self.upperStrain=value
        self.view.update_strain_upper_limit(value)

    def update_stress_upper_limit(self, value):
        self.upperStress=value
        self.view.update_stress_lower_limit(value)
    
    def update_strain_lower_limit(self, value):
        self.lowerStrain=value
        self.view.update_strain_lower_limit(value)

    def update_stress_lower_limit(self, value):
        self.lowerStress=value
        self.view.update_stress_lower_limit(value)
    
    def confirm(self):
        f=Linear(self.a,0,self.lowerStrain,self.upperStrain,self.lowerStress,self.upperStress)
        self.lawEditor.set_f(f)
        self.lawEditor.cancel_graphicShow()
        self.lawEditor.creater.cancel(None)
    
    def cancel(self):
        self.lawEditor.cancel_graphicShow()
    
    def sign_in(self,editor):
        self.lawEditor=editor
    
