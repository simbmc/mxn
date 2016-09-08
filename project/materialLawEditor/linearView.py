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
        self.line = LinePlot(points=[(0, 0), (self.editor.maxStrain, self.editor.upperStress)], width=2, color=[1, 0, 0])
        self.graph.add_plot(self.line)
    

    '''
    update the graph-properties
    '''    
        
    def update_graph_properties(self):
        print('update_graph_properties (linearView)')
        self.graph.xmax = self.editor.maxStrain
        self.graph.xmin = self.editor.minStrain
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        y1, y2 = self.graph.xmin * self.editor.a, self.graph.xmax * self.editor.a
        self.graph.ymin = y1
        self.graph.ymax = y2
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        self.line.points = [(self.graph.xmin, y1), (self.graph.xmax, y2)]
