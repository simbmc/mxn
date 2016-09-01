'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from numpy import arange

from plot.line import LinePlot
from materialLawEditor.aview import AView

class QuadraticFunctionView(GridLayout, AView):
    
    '''
    the view-component show the function in a graph
    '''
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(QuadraticFunctionView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.plot = LinePlot(color=[255, 0, 0])
        self.plot.points = [(x, self.editor.f(x)) for x in arange(-self.graph.xmax, self.graph.xmax + 1, self.graph.xmax / 1e2)]
        self.graph.add_plot(self.plot)
 
    '''
    update the points of the line. => update of the function
    '''
    def update_points(self):
        self.plot.points = [(x, self.editor.f(x)) for x in arange(self.graph.xmin, self.graph.xmax, self.graph.xmax / 1e2)]
    
    '''
    update the graph properties
    '''
    def update_graph_sizeproperties(self):
        self.graph.xmin = self.editor.lowerStrain
        self.graph.xmax = self.editor.upperStrain
        self.graph.ymin = self.editor.lowerStress
        self.graph.ymax = self.editor.upperStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        self.update_points()
        
