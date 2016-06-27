'''
Created on 03.05.2016

@author: mkennert
'''

'''
f(x)=mx+b
'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.linearInformation import LinearInformation
from materialLawEditor.linearView import LinearView

class Linear(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(Linear, self).__init__(**kwargs)
        self.cols=2
        self.m=1
        self.b=0
        self.view=LinearView()
        self.view.sign_in(self)
        self.information=LinearInformation()
        self.information.sign_in(self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    def set_m(self,value):
        self.m=value
    
    def set_b(self,value):
        self.b=value
    
    def get_m(self):
        return self.m   
    
    def get_b(self):
        return self.b
    
    def update_btn(self,value):
        self.information.update_btn(value)
    
    def update_graph(self,value):
        self.view.update_graph(value)
'''
Just for testing
'''
class TestApp(App):
        def build(self):
            return Linear()
TestApp().run()
    
    