'''
Created on 03.05.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, MeshLinePlot
from materialLawEditor.mulitlinearInformation import MultilinearInformation
from materialLawEditor.multilinearView import MultilinearView


class Multilinear(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(Multilinear, self).__init__(**kwargs)
        self.cols = 2
        self.h=50.
        self.w=50.
        self._points=5
        self.information=MultilinearInformation()
        self.view=MultilinearView()
        self.information.signIn(self)
        self.view.signIn(self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    set the width of the graph
    '''
    def setWidth(self, value):
        self.w=value
        self.view.updateWidth()
    
    '''
    set the height of the graph
    '''
    def setHeight(self,value):
        self.h=value
        self.view.updateHeight()
    
    '''
    return the height of the graph
    '''
    def getHeight(self):
        return self.h
    
    '''
    return the width of the graph
    '''
    def getWidth(self):
        return self.w
    
    '''
    set the numbers of points which the graph should have
    '''
    def setPoints(self,value):
        self._points=value
        self.view.updatePoints()
    
    '''
    return the number of points
    '''
    def getPoints(self):
        return self._points     

'''
Just for testing
'''
class TestApp(App):
        def build(self):
            return Multilinear()

TestApp().run()