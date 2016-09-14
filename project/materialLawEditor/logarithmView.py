'''
Created on 13.09.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from numpy import arange

from materialLawEditor.aview import AView
from plot.line import LinePlot


class LogarithmView(GridLayout, AView):
    
    '''
    the view-component show the function in a graph
    '''
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(LogarithmView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.line = LinePlot(color=[255, 0, 0])
        self.line.points = [(x, self.editor.f(x)) for x in arange(-self.graph.xmax, self.graph.xmax + 1, self.graph.xmax / 1e2)]
        self.graph.add_plot(self.line)
    
    '''
    update the points of the line. => update of the function
    '''
    
    def update_points(self):
        self.line.points = [(x, self.editor.f(x)) for x in arange(self.graph.xmin, self.graph.xmax, self.graph.xmax / 1e2)]
    
    '''
    update the graph properties
    '''
    
    def update_graph_sizeproperties(self):
        self.graph.xmin = self.editor.minStrain
        self.graph.xmax = self.editor.maxStrain
        self.update_points()
        self.graph.ymin, self.graph.ymax = self.find_min_max(self.line.points)
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
    
    '''
    find the min- and the max-y-coordinate 
    '''
        
    def find_min_max(self, points):
        min_v = 1e10
        max_v = -1e10
        n = len(points)
        for i in range(n):
            c = points[i][1]
            if c < min_v:
                min_v = c
            if c > max_v:
                max_v = c
        return float(min_v), float(max_v)