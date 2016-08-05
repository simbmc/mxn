'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from numpy import arange

from ownComponents.ownGraph import OwnGraph
from plot.line import LinePlot


class QuadraticFunctionView(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionView, self).__init__(**kwargs)
        self.cols = 1
        
    
    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = OwnGraph(xlabel='strain', ylabel='stress',
                           x_ticks_major=2.5, y_ticks_major=2.5,
                           y_grid_label=True, x_grid_label=True,
                           x_grid=True, y_grid=True,
                           xmin=-self.editor.w, xmax=self.editor.w,
                           ymin=-self.editor.h, ymax=self.editor.h)
        self.add_widget(self.graph)
    
    '''
    draw the function
    '''
    def draw_lines(self):
        self.plot = LinePlot(color=[255,0,0])
        self.plot.points = [(x, self.editor.f(x)) for x in arange(-self.graph.xmax, self.graph.xmax+1,self.graph.xmax/1e2)]
        print('points: '+str(self.plot.points))
        self.graph.add_plot(self.plot)
            
    def update_points(self):
        self.plot.points=[(x, self.editor.f(x)) for x in arange(-self.graph.xmax, self.graph.xmax+1,self.graph.xmax/1e2)]
        
    def update_lower_stress(self,value):
        self.graph.ymin=value
    
    def update_lower_strain(self,value):
        self.graph.xmin=value
        
    '''
    sign in by the parent
    '''
    def sign_in(self, parent):
        self.editor=parent
        self.create_graph()
        self.draw_lines()
    
    '''
    update the graphwidth
    '''
    def update_width(self):
        self.graph.xmin=-self.editor.getwidth()
        self.graph.x_ticks_major=self.graph.xmax/5.
        self.graph.xmax=self.editor.getwidth()
    
    '''
    update the graphheight
    '''
    def update_height(self):
        self.graph.ymax=self.editor.get_height()
    
            