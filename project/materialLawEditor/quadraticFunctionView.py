'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot


class QuadraticFunctionView(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionView, self).__init__(**kwargs)
        self.cols = 1
        
    
    '''
    create the graph of the view
    '''
    def createGraph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=2, y_ticks_major=2,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0, xmax=self.editor.w, ymin=0, ymax=self.editor.h)
        self.add_widget(self.graph)
    
    '''
    draw the function
    '''
    def drawLines(self):
        while len(self.graph.plots)>0:
            for plot in self.graph.plots:
                self.graph.remove_plot(plot)
                self.graph._clear_buffer()
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, self.editor.f(x)) for x in range(-self.graph.xmax, self.graph.xmax+1)]
        self.graph.add_plot(plot)
            
    '''
    sign in by the parent
    '''
    def signIn(self, parent):
        self.editor=parent
        self.createGraph()
        self.drawLines()
    
    '''
    update the graphwidth
    '''
    def updateWidth(self):
        self.graph.xmax=self.editor.getwidth()
    
    '''
    update the graphheight
    '''
    def updateHeight(self):
        self.graph.ymax=self.editor.getHeight()
    
            