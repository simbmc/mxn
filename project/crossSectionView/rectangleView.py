'''
Created on 14.03.2016

@author: mkennert
'''

from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.aview import AView
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.dashedLine import DashedLine
from plot.line import LinePlot


class CSRectangleView(GridLayout, AView):
    
    '''
    the class CSRectangleView was developed to show the rectangle-shape of 
    the cross-section
    '''
    
    # height of the cross-section
    ch = NumericProperty(0.5)
    
    # width of the cross-section
    cw = NumericProperty(0.25)
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(CSRectangleView, self).__init__(**kwargs)
        self.cols = 1

    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.epsX = self.cw / 2e1
        self.graph = OwnGraph(xlabel=self.xlabelStr, ylabel=self.ylabelStr,
                              x_ticks_major=0.05, y_ticks_major=0.05,
                              y_grid_label=True, x_grid_label=True, padding=5,
                              xmin=0, xmax=self.cw + 2 * self.epsX, ymin=0, ymax=1.04 * self.ch)
        self.add_widget(self.graph)
        self.p = LinePlot(color=[0, 0, 0])
        self.p.points = self.draw_rectangle()
        self.graph.add_plot(self.p)

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, y, csArea, material):
        #if the y-coordinate is out of range
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
        else:
            line = DashedLine(color=[1, 0, 0, 1], points=[(self.epsX, y), (self.cw + self.epsX, y)])
            self.create_layer(y, csArea, self.cw, material, line)
    
    '''
    edit a layer which is already exist
    '''
        
    def edit_layer(self, y, material, csArea):
        #if the y-coordinate is out of range
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
        else:
            self.focusLayer.line.points = [(self.epsX, y), (self.cw + self.epsX, y)]
            self.update_layer_properties(y, material, csArea)
    
    '''
    add a bar to the cross-section
    '''

    def add_bar(self, x, y, csArea, material):
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        #if the coordinates are out of range
        if y + epsY > self.ch or y - epsY < 0 or x + epsX > self.cw + self.epsX or x - epsX < self.epsX:
            self.csShape.show_error_message()
        else:
            self.create_bar(x, y, csArea, material, epsX, epsY)
    
    '''
    edit a bar which is already exist
    '''
            
    def edit_bar(self, x, y, csArea, material):
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        #if the coordinates are out of range
        if y + epsY > self.ch or y - epsY < 0 or x + epsX > self.cw + self.epsX or x - epsX < self.epsX:
            self.csShape.show_error_message()
        else:
            self.update_bar_properties(x, y, csArea, material, epsX, epsY)     
    
    
    '''
    the method update_height change the height of the cross section shape
    and update the layers
    '''

    def update_height(self, value):
        self.ch = value
        self.graph.y_ticks_major = value / 5.
        self.graph.ymax = self.ch * 1.04 
        self.p.points = self.draw_rectangle()
        self.delete_reinforcement()

    '''
    the method update_width change the width of the cross section shape
    and update the layers
    '''

    def update_width(self, value):
        self.cw = value
        self.graph.x_ticks_major = value / 5.
        self.graph.xmax = self.cw + 2 * self.epsX
        self.p.points = self.draw_rectangle()
        self.delete_reinforcement()
    
    '''
    give the user the possibility to focus a layer or a bar
    '''
            
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.cw + 2 * self.epsX)
        y = (touch.y - y0) / gh * self.graph.ymax
        self.touch_reaction(x, y, self.cw, self.ch)
    
    '''
    draw the rectangle
    '''

    def draw_rectangle(self):
        return [(self.epsX, 0), (self.epsX, self.ch), (self.cw + self.epsX, self.ch), (self.cw + self.epsX, 0), (self.epsX, 0)]
