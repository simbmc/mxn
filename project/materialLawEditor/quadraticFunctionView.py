'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from numpy import arange

from ownComponents.ownGraph import OwnGraph
from plot.line import LinePlot
from kivy.properties import  ObjectProperty, StringProperty

class QuadraticFunctionView(GridLayout):
    
    # important components
    editor = ObjectProperty()
    
    # strings
    strainStr, stressStr = StringProperty('strain'), StringProperty('stress [MPa]')
    
    # constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
    
    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.stressStr, ylabel=self.strainStr,
                           x_ticks_major=2.5, y_ticks_major=2.5,
                           y_grid_label=True, x_grid_label=True,
                           x_grid=True, y_grid=True,
                           xmin=self.editor.lowerStress, xmax=self.editor.upperStress,
                           ymin=self.editor.lowerStrain, ymax=self.editor.upperStrain)
        self.add_widget(self.graph)
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
        self.graph.xmin = self.editor.lowerStress
        self.graph.xmax = self.editor.upperStress
        self.graph.ymin = self.editor.lowerStrain
        self.graph.ymax = self.editor.upperStrain
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        
