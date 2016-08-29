'''
Created on 09.05.2016

@author: mkennert
'''

from kivy.uix.gridlayout import GridLayout

from ownComponents.ownGraph import OwnGraph
from plot.line import LinePlot
from kivy.properties import  ObjectProperty, StringProperty

class LinearView(GridLayout):
    
    '''
    the view-component show the function in a graph
    '''
    
    # important components
    editor = ObjectProperty()
    
    # strings
    strainStr, stressStr = StringProperty('strain'), StringProperty('stress [MPa]')
    
    # constructor
    def __init__(self, **kwargs):
        super(LinearView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
    
    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.strainStr, ylabel=self.stressStr,
                              x_ticks_major=2, y_ticks_major=2,
                              y_grid_label=True, x_grid_label=True,
                              x_grid=True, y_grid=True,
                              xmin=0, xmax=10, ymin=0, ymax=10)
        self.line = LinePlot(points=[(0, 0), (10, 10)], width=2, color=[1, 0, 0])
        self.graph.add_plot(self.line)
        self.add_widget(self.graph)
    
    
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
   
    '''
    update the complete graph by the given function-properties
    '''
    def update_function(self, points, minStress, maxStress, minStrain, maxStrain):
        self.line.points = points
        self.graph.xmin, self.graph.xmax = minStrain, maxStrain
        self.graph.ymin, self.graph.ymax = minStress, maxStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        
