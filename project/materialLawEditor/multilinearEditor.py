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
    # constructor

    def __init__(self, **kwargs):
        super(Multilinear, self).__init__(**kwargs)
        self.cols = 2
        self.h = 50.
        self.w = 50.
        self._points = 5
        self.information = MultilinearInformation()
        self.view = MultilinearView()
        self.information.sign_in(self)
        self.view.sign_in(self)
        self.add_widget(self.view)
        self.add_widget(self.information)

    '''
    set the width of the graph
    '''

    def set_width(self, value):
        self.w = value
        self.view.update_width()

    '''
    set the height of the graph
    '''

    def set_height(self, value):
        self.h = value
        self.view.update_height()

    '''
    set the numbers of points which the graph should have
    '''

    def set_points(self, value):
        self._points = value
        self.view.update_points()

    '''
    return the number of points
    '''

    def get_points(self):
        return self._points

'''
Just for testing
'''


class TestApp(App):

    def build(self):
        return Multilinear()

TestApp().run()
