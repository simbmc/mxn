'''
Created on 09.05.2016

@author: mkennert
'''

from kivy.uix.gridlayout import GridLayout

from plot.line import LinePlot
from materialLawEditor.aview import AView

class LinearView(GridLayout, AView):
    
    '''
    the view-component show the function in a graph
    '''
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(LinearView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.line = LinePlot(points=[(0, 0), (self.editor.upperStrain, self.editor.upperStress)], width=2, color=[1, 0, 0])
        self.graph.add_plot(self.line)
    
    '''
    update the graph with the new lower strain limit.
    '''
    def update_strain_lower_limit(self, value):
        self.graph.xmin = value
        self.graph.x_ticks_major = (self.graph.xmax - value) / 5.
        self.update_graph(self.editor.a)
    
    '''
    update the graph with the new upper strain limit.
    '''
    def update_strain_upper_limit(self, value):
        self.graph.xmax = value
        self.graph.x_ticks_major = (value - self.graph.xmin) / 5.
        self.update_graph(self.editor.a)
    
    '''
    update the graph with the new lower stress limit.
    '''
    def update_stress_lower_limit(self, value):
        self.graph.ymin = value
        self.graph.y_ticks_major = (self.graph.ymax - value) / 5.
        self.update_graph(self.editor.a)
    
    '''
    update the graph with the new upper stress limit.
    '''
    def update_stress_upper_limit(self, value):
        self.graph.ymax = value
        self.graph.y_ticks_major = (value - self.graph.ymin) / 5.
        self.update_graph(self.editor.a)
    
    '''
    update the graph
    '''
    def update_graph(self, value):
        y1, y2 = self.graph.xmin * value, self.graph.xmax * value
        self.line.points = [(self.graph.xmin, y1), (self.graph.xmax, y2)]