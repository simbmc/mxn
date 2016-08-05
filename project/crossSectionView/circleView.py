'''
Created on 01.04.2016

@author: mkennert
'''

from kivy.uix.boxlayout import BoxLayout

from crossSectionView.aview import AView
import numpy as np
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.dashedLine import DashedLine
from plot.ellipse import Ellipse
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
from reinforcement.bar import Bar
from reinforcement.layer import Layer
from kivy.properties import ListProperty,NumericProperty,ObjectProperty

class CSCircleView(AView, BoxLayout):
    layers,bars = ListProperty([]),ListProperty([])
    d = NumericProperty(0.25)
    csShape=ObjectProperty()
    
    # constructor
    def __init__(self, **kwargs):
        super(CSCircleView, self).__init__(**kwargs)
        self.focusLine = LinePlot(width=1.5, color=Design.focusColor)
        self.lineIsFocused = False

    '''
    the method create_graph create the graph, where you can add 
    the rectangles. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = OwnGraph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.d, ymin=0, ymax=self.d)
        self.draw_circle()
        self.add_widget(self.graph)

    '''
    draw the circle
    '''

    def draw_circle(self):
        self.circle = Ellipse()
        self.circle.xrange = [0, self.graph.xmax]
        self.circle.yrange = [0, self.graph.ymax]
        self.circle.color = [0, 0, 0, 1]
        self.graph.add_plot(self.circle)

    '''
    set the radius of the circle
    '''
    def update_circle(self, r):
        self.d = r
        self.graph.x_ticks_major = self.graph.y_ticks_major = self.d / 5.
        self.graph.xmax = r
        self.graph.ymax = r
        self.graph.remove_plot(self.circle)
        self.draw_circle()

    '''
    add a new bar
    '''

    def add_bar(self, x, y, material):
        epsY = self.d / Design.barProcent
        epsX = self.d / Design.barProcent
        b = Bar(x, y)
        b.set_Material(material)
        plot = FilledEllipse(xrange=[x - epsX, x + epsX], 
                             yrange=[y - epsY, y + epsY], 
                             color=[255, 0, 0, 1])
        b.set_filled_ellipse(plot)
        self.graph.add_plot(plot)
        self.bars.append(b)
    
    '''
    edit a bar which is already exist
    '''
    def edit_bar(self, x, y, material, csArea):
        self.focusBar.x = x
        self.focusBar.y = y
        self.focusBar.material = material
        epsY = self.d / Design.barProcent
        epsX = self.d / Design.barProcent
        self.focusBar.ellipse.xrange = [x - epsX, x + epsX]
        self.focusBar.ellipse.yrange = [y - epsY, y + epsY]
    
    '''
    add a new layer
    '''
    def add_layer(self, x, y, material):
        x1 = -np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
        x2 = np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
        l = Layer(0, y, 0., 0)
        l.set_Material(material)
        line = DashedLine(color=[1, 0, 0, 1], points=[(x1, y), (x2, y)])
        l.set_line(line)
        self.graph.add_plot(line)
        self.layers.append(l)

    '''
    edit a layer which is already exist
    '''
    def edit_layer(self, y, material, csArea):
        self.focusLayer.y = y
        self.focusLayer.material = material
        if y < self.d * 2:
            x1 = -np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
            x2 = np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
            self.focusLayer.line.points = [(x1, y), (x2, y)]
            self.csShape.hide_error_message()
        if self.lineIsFocused:
            self.graph.remove_plot(self.focusLine)
    
    '''
    give the user the possibility to focus a layer or a bar
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.d)
        y = (touch.y - y0) / gh * (self.d)
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
        oneIsFocused = False
        if x < self.d:
            for layer in self.layers:
                if layer.mouse_within(y, self.graph.ymax / 1e2):
                    oneIsFocused = True
                    self.lineIsFocused = True
                    self.focusLayer = layer
                    self.csShape.cancel_editing_bar()
                    self.csShape.show_edit_area_layer()
                    self.focusLine.points = layer.line.points
                    self.graph.add_plot(self.focusLine)
        if not oneIsFocused and self.lineIsFocused:
            self.graph.remove_plot(self.focusLine)
            self.csShape.cancel_editing_layer()