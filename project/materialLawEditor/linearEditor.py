'''
Created on 03.05.2016

@author: mkennert
'''
from functions.linearFunction import Linear

'''
f(x)=ax+b
'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.linearInformation import LinearInformation
from materialLawEditor.linearView import LinearView


class LinearEditor(GridLayout):
    # constructor

    def __init__(self, **kwargs):
        super(LinearEditor, self).__init__(**kwargs)
        self.cols = 2
        self.a = 1
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
        self.view.update_strain_upper_limit(value)

    def update_stress_upper_limit(self, value):
        self.view.update_stress_lower_limit(value)
    
    def update_strain_lower_limit(self, value):
        self.view.update_strain_lower_limit(value)

    def update_stress_lower_limit(self, value):
        self.view.update_stress_lower_limit(value)
    
    def confirm(self):
        f=Linear(self.a,0)
        self.lawEditor.set_f(f)
        self.lawEditor.cancel_graphicShow()
        self.lawEditor.creater.cancel(None)
    
    def cancel(self):
        print('cancel linear Editor')
        self.lawEditor.cancel_graphicShow()
    
    def sign_in(self,editor):
        self.lawEditor=editor
    
