'''
Created on 28.06.2016

@author: mkennert
'''
from kivy.graphics import Line

from kivy.uix.gridlayout import GridLayout

from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
import numpy as np

class ExpView(GridLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(ExpView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.create_point()
    
    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=2, y_ticks_major=.2,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=11, ymin=0, ymax=1)
        self.add_widget(self.graph)
    
    '''
    create the point
    '''
    def create_point(self):
        delta=50.
        self.epsX=self.graph.xmax/delta
        self.epsY=self.graph.ymax/delta
        x=10
        y=(1-1*np.exp(-10))
        self.point=FilledEllipse(color=[255,0,0])
        self.point.xrange = [x-self.epsX,x+self.epsX]
        self.point.yrange = [y-self.epsY,y+self.epsY]
        self.graph.add_plot(self.point)
        self.line=LinePlot(width=1.5)
        self.line.points=[(0.5*x,0.5*(1-1*np.exp(-x))) for x in range(20)]
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
            #self.line.points=[(0,0),(x,y)]
            c=(1-y)*np.exp(x)
            print('c: '+str(c))
            self.line.points=[(x,(1-c*np.exp(-x))) for x in range(10)]
            if x>0:
                self.editor.update_btn(c)
    
    '''
    upgrade the graph when the user 
    change the slope with the button
    '''
    def update_graph(self,value):
        x=5
        y=x*value
        self.graph.xmax=11
        self.graph.ymax=y+2
        delta=50.
        self.epsX=self.graph.xmax/delta
        self.epsY=self.graph.ymax/delta
        self.point.xrange=[x-self.epsX,x+self.epsX]
        self.point.yrange=[y-self.epsY,y+self.epsY]
        self.graph.y_ticks_major=int(self.graph.ymax/5.)
        self.point.xrange=[x-self.epsX,x+self.epsX]
        self.point.yrange=[y-self.epsY,y+self.epsY]
        self.line.points=[(0,0),(x,y)]
    
    '''
    sign in by the parent
    '''
    def sign_in(self, parent):
        self.editor=parent