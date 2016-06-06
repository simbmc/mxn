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
        self.view.signIn(self)
        self.information=LinearInformation()
        self.information.signIn(self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    def setM(self,value):
        self.m=value
    
    def setB(self,value):
        self.b=value
    
    def getM(self):
        return self.m   
    
    def getB(self):
        return self.b
    
'''
Just for testing
'''
class TestApp(App):
        def build(self):
            return Linear()
TestApp().run()
    
    