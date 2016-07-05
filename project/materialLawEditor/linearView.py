'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.graphics import Line

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
        self.b=0.
        self.create_graph()
        self.create_point()
    
    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=2, y_ticks_major=2,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=11, ymin=0, ymax=11)
        self.add_widget(self.graph)
    
    '''
    create the point
    '''
    def create_point(self):
        delta=50.
        self.epsX=self.graph.xmax/delta
        self.epsY=self.graph.ymax/delta
        x=10
        y=10
        self.point=FilledEllipse(color=[255,0,0])
        self.point.xrange = [x-self.epsX,x+self.epsX]
        self.point.yrange = [y-self.epsY,y+self.epsY]
        self.graph.add_plot(self.point)
        self.line=LinePlot(points=[(0,self.b),(x,y)],width=1.5)
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
        if self.point.color==Design.focusColor and x<self.graph.xmax and y<self.graph.ymax\
            and y>0 and x>0:
            self.point.xrange=[x-self.epsX,x+self.epsX]
            self.point.yrange=[y-self.epsY,y+self.epsY]
            self.line.points=[(0,self.b),(x,y)]
            if x>0:
                self.editor.update_btn((y-self.b)/x)
    
    '''
    upgrade the graph when the user 
    change the slope with the button
    '''
    def update_graph(self,value):
        x=5
        y=x*value
        delta=50.
        self.epsX=self.graph.xmax/delta
        self.epsY=self.graph.ymax/delta
        self.point.xrange=[x-self.epsX,x+self.epsX]
        self.point.yrange=[y-self.epsY,y+self.epsY]
        self.point.xrange=[x-self.epsX,x+self.epsX]
        self.point.yrange=[y-self.epsY,y+self.epsY]
        self.line.points=[(0,self.b),(x,y)]
    
    '''
    sign in by the parent
    '''
    def sign_in(self, parent):
        self.editor=parent
    
    #not finished yet
    def update_strain_limit(self,value):
        self.graph.ymax=value
        self.graph.y_ticks_major=value/10.
        delta=50.
        x=self.point.yrange[0]+self.epsY
        self.epsY=self.graph.ymax/delta
        self.point.yrange=[x-self.epsY,x+self.epsY]
        
    
    #not finished yet
    def update_stress_limit(self,value):
        self.graph.xmax=value
        self.graph.x_ticks_major=value/10.
        delta=50.
        x=self.point.xrange[0]+self.epsX
        self.epsX=self.graph.xmax/delta
        self.point.xrange=[x-self.epsX,x+self.epsX]
        
    #not finished yet
    def update_b(self,value):
        self.b=value
        cur=self.line.points[1]
        self.line.points=[(0,self.b),cur]