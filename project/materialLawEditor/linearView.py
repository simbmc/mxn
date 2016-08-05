'''
Created on 09.05.2016

@author: mkennert
'''

from kivy.uix.gridlayout import GridLayout

from ownComponents.ownGraph import OwnGraph
from plot.line import LinePlot


class LinearView(GridLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(LinearView, self).__init__(**kwargs)
        self.cols = 1
        self.b=0.
        self.create_graph()
    
    def update_strain_lower_limit(self, value):
        self.graph.ymin=-value
        self.graph.y_ticks_major=value/5
        self.update_graph(self.editor.a)

    def update_stress_lower_limit(self, value):
        self.graph.xmin=-value
        self.graph.x_ticks_major=value/5
        self.update_graph(self.editor.a)
    
    def update_stress_upper_limit(self,value):
        self.graph.xmax=value
        self.graph.x_ticks_major=value/5
        self.update_graph(self.editor.a)
    
    def update_strain_upper_limit(self,value):
        self.graph.ymax=value
        self.graph.y_ticks_major=value/5
        self.update_graph(self.editor.a)
    
    '''
    update the graph
    '''
    def update_graph(self,value):
        y1,y2=self.graph.xmin*value,self.graph.xmax*value
        self.line.points=[(self.graph.xmin,y1),(self.graph.xmax,y2)]
    
    '''
    sign in by the editor
    '''
    def sign_in(self, parent):
        self.editor=parent
    
    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = OwnGraph(xlabel='strain', ylabel='stress',
                           x_ticks_major=2, y_ticks_major=2,
                           y_grid_label=True, x_grid_label=True,
                           x_grid=True, y_grid=True,
                           xmin=0, xmax=10, ymin=0, ymax=10)
        self.line=LinePlot(points=[(0,0),(10,10)],width=2,color=[1,0,0])
        self.graph.add_plot(self.line)
        self.add_widget(self.graph)
        