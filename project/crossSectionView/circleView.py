'''
Created on 01.04.2016

@author: mkennert
'''

from kivy.uix.boxlayout import BoxLayout

from bars.bar import Bar
from crossSectionView.aview import AView
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from layers.layer import Layer
import numpy as np
from plot.dashedLine import DashedLine
from plot.ellipse import Ellipse
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot


class CSCircleView(AView, BoxLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(CSCircleView, self).__init__(**kwargs)
        self.crossSectionRadius = 0.25
        self.focusLine=LinePlot(width=1.5,color=Design.focusColor)
        self.lineIsFocused=False
        self.layers = []
        self.bars = []

    '''
    the method create_graph create the graph, where you can add 
    the rectangles. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.r, ymin=0, ymax=self.r)
        self.draw_circle()
        self.add_widget(self.graph)

    '''
    draw the circle
    '''

    def draw_circle(self):
        self.circle = Ellipse()
        self.circle.xrange = [0, self.graph.xmax]
        self.circle.yrange = [0, self.graph.ymax]
        self.circle.color = [255, 255, 255, 1]
        self.graph.add_plot(self.circle)

    '''
    the method update_layer_information update the layer information of 
    the view_information
    '''

    def update_layer_information(self, name, price, density, stiffness, strength):
        self.csShape.set_layer_information(
            name, price, density, stiffness, strength)

    '''
    the method update_cross_section_information update the cross section information of 
    the view_information
    '''

    def update_cross_section_information(self):
        self.csShape.calculate_weight_price()
        self.csShape.set_cross_section_information()

    '''
    set the cross section
    '''

    def set_cross_section(self, cs):
        self.csShape = cs
        self.r = self.csShape.get_radius()
        self.create_graph()

    # not finished yet
    def set_radius(self, r):
        self.r = r
        self.graph.x_ticks_major = self.graph.y_ticks_major = self.r / 5.
        self.graph.xmax = r
        self.graph.ymax = r
        self.graph.remove_plot(self.circle)
        self.draw_circle()

    '''
    add a bar
    '''

    def add_bar(self, x, y, material):
        epsY = self.r / Design.barProcent
        epsX = self.r / Design.barProcent
        b = Bar(x, y)
        b.set_Material(material)
        plot = FilledEllipse(
            xrange=[x - epsX, x + epsX], yrange=[y - epsY, y + epsY], color=[255, 0, 0, 1])
        b.set_filled_ellipse(plot)
        self.graph.add_plot(plot)
        self.bars.append(b)
    
    '''
    add a new layer
    '''
    def add_layer(self, x, y, material):
        print('y: '+str(y))
        print('r: '+str(self.r))
        x=np.sqrt(np.power(self.r/2.,2)-np.power(y-self.r/2.,2))+self.r/2.
        #x1=self.r-(x-self.r/2.)
        x1=-np.sqrt(np.power(self.r/2.,2)-np.power(y-self.r/2.,2))+self.r/2.
        x2=x
        print('x1: '+str(x))
        print('x2: '+str(x1))
        l = Layer(0, y, 0., 0)
        l.set_Material(material)
        line = DashedLine(color=[1, 0, 0, 1], points=[(x1, y), (x2, y)])
        l.set_line(line)
        self.graph.add_plot(line)
        self.layers.append(l)
        
    
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.r)
        y = (touch.y - y0) / gh * (self.r)
        # change_bar is a switch
        change_bar = False
        for bar in self.bars:
            if bar.mouse_within(x, y):
                bar.ellipse.color = Design.focusColor
                self.focusBar = bar
                self.csShape.cancel_editing_layer()
                self.csShape.show_edit_bar_area()
                change_bar = True
            else:
                bar.ellipse.color = [255, 0, 0]
        # make sure that only one reinforcement can be added
        # at the same time
        if change_bar:
            return
        else:
            self.csShape.cancel_editing_bar()
        oneIsFocused=False
        if x < self.r:
            for layer in self.layers:
                if layer.mouse_within(y, self.graph.ymax / 1e2):
                    oneIsFocused=True
                    self.lineIsFocused=True
                    self.focusLayer = layer
                    self.csShape.cancel_editing_bar()
                    self.csShape.show_edit_area_layer()
                    self.focusLine.points=layer.line.points
                    self.graph.add_plot(self.focusLine)
        if not oneIsFocused and self.lineIsFocused:
            self.graph.remove_plot(self.focusLine)
            self.csShape.cancel_editing_layer()
    # not finished yet

    def edit_bar(self, x, y, material, csArea):
        self.focusBar.x = x
        self.focusBar.y = y
        self.focusBar.material = material
        epsY = self.r / Design.barProcent
        epsX = self.r / Design.barProcent
        self.focusBar.ellipse.xrange = [x - epsX, x + epsX]
        self.focusBar.ellipse.yrange = [y - epsY, y + epsY]

    # not finished yet

    def edit_layer(self, y, material, csArea):
        mid = self.graph.xmax / 2.
        self.focusLayer.y = y
        self.focusLayer.material = material
        if y < self.bh:
            self.focusLayer.line.points = [
                (mid - self.bw / 2., y), (mid - self.bw / 2. + self.bw, y)]
            self.csShape.hide_error_message()
        else:
            self.focusLayer.line.points = [
                (mid - self.tw / 2., y), (mid - self.tw / 2. + self.tw, y)]
            self.csShape.hide_error_message()
        if self.lineIsFocused:
            self.graph.remove_plot(self.focusLine)
