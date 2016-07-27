'''
Created on 28.06.2016

@author: mkennert
'''
from materialLawEditor.expView import ExpView
from materialLawEditor.expInformation import ExpInformation
'''
f(x)=1-c*exp(-x)
'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.linearInformation import LinearInformation
from materialLawEditor.linearView import LinearView


class ExpEditor(GridLayout):
    # constructor

    def __init__(self, **kwargs):
        super(ExpEditor, self).__init__(**kwargs)
        self.cols = 2
        self.c = 1
        self.view = ExpView()
        self.view.sign_in(self)
        self.information = ExpInformation()
        self.information.sign_in(self)
        self.add_widget(self.view)
        self.add_widget(self.information)

    def set_c(self, value):
        self.c = value

    def get_c(self):
        return self.c

    def update_btn(self, value):
        self.information.update_btn(value)

    def update_graph(self, value):
        self.view.update_graph(value)
'''
Just for testing
'''


class TestApp(App):

    def build(self):
        return ExpEditor()
TestApp().run()
