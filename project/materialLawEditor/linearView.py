'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.graphics import OwnLine

from kivy.uix.gridlayout import GridLayout

from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot


class LinearView(GridLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(LinearView, self).__init__(**kwargs)
        self.cols = 1
        self.createGraph()
        self.createPoint()
    
    '''
    create the graph of the view
    '''
    def createGraph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=1, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=11, ymin=0, ymax=11)
        self.add_widget(self.graph)
    
    '''
    create the point
    '''
    def createPoint(self):
        delta=100.
        self.epsX=self.graph.xmax/delta
        self.epsY=self.graph.ymax/delta
        x=10
        y=10
        self.point=FilledEllipse(color=[255,0,0])
        self.point.xrange = [x-self.epsX,x+self.epsX]
        self.point.yrange = [y-self.epsY,y+self.epsY]
        self.graph.add_plot(self.point)
        #with self.canvas:
        #        self.line=OwnLine(points=[0, 0, 10, 10], width=1)
        #self.graph.add_plot(self.line)
        self.line=LinePlot(xrange=[0,x],yrange=[0,y])
        self.graph.add_plot(self.line)
    
    '''
    reaction when the user move touch on the graph 
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        #11=xmax=ymax
        x = (touch.x - x0) / gw*self.graph.xmax
        y = (touch.y - y0) / gh*self.graph.ymax
        if self.point.xrange[0]<=x and self.point.xrange[1]>=x \
            and self.point.yrange[0]<=y and self.point.yrange[1]>=y:
            self.point.color=Design.focusColor
        else:
            self.point.color=[255,0,0]
    
    '''
    reaction when the user move over the graph
    '''             
    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        #11=xmax=ymax
        x = (touch.x - x0) / gw*self.graph.xmax
        y = (touch.y - y0) / gh*self.graph.ymax
        if self.point.color==Design.focusColor:
            self.point.xrange=[x-self.epsX,x+self.epsX]
            self.point.yrange=[y-self.epsY,y+self.epsY]
    
    '''
    sign in by the parent
    '''
    def signIn(self, parent):
        self.editor=parent
    