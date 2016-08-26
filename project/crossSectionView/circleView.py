'''
Created on 01.04.2016

@author: mkennert
'''

from kivy.properties import NumericProperty, ObjectProperty, StringProperty
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


class CSCircleView(AView, BoxLayout):
    
    '''
    the class CSCircleView was developed to show the circle-shape of 
    the cross-section
    '''
    
    # important components
    csShape = ObjectProperty()
    
    # important values
    d = NumericProperty(0.25)
    
    # strings
    ylabelStr = StringProperty('cross-section-height [m]')
    xlabelStr = StringProperty('cross-section-width [m]')
    
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
        self.graph = OwnGraph(xlabel=self.xlabelStr, ylabel=self.ylabelStr,
                              x_ticks_major=0.05, y_ticks_major=0.05,
                              y_grid_label=True, x_grid_label=True, padding=5,
                              xmin=0, xmax=self.d, ymin=0, ymax=self.d)
        self.draw_circle()
        self.add_widget(self.graph)

    '''
    set the radius of the circle
    '''
    def update_circle(self, r):
        self.d = r
        self.graph.x_ticks_major = self.graph.y_ticks_major = self.d / 5.
        self.graph.xmax = self.graph.ymax = r
        self.graph.remove_plot(self.circle)
        self.draw_circle()
    
    '''
    add a new layer
    '''
    def add_layer(self, x, y, material):
        if y >= self.csShape.d or y <= 0:
            self.csShape.show_error_message()
            return
        self.csShape.hide_error_message()
        x1 = -np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
        x2 = np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2.
        l = Layer(0, y, 0., 0)
        l.material = material
        line = DashedLine(color=[1, 0, 0, 1], points=[(x1, y), (x2, y)])
        l.line = line
        self.graph.add_plot(line)
        self.csShape.layers.append(l)

    '''
    edit a layer which is already exist
    '''
    def edit_layer(self, y, material, csArea):
        if y >= self.csShape.d or y <= 0:
            self.csShape.show_error_message()
            return
        self.csShape.hide_error_message()
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
    add a new bar
    '''

    def add_bar(self, x, y, material):
        epsY = self.d / Design.barProcent
        epsX = self.d / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY):
            self.csShape.show_error_message()
            return
        self.csShape.hide_error_message()
        epsY = self.d / Design.barProcent
        epsX = self.d / Design.barProcent
        b = Bar(x, y)
        b.material = material
        plot = FilledEllipse(xrange=[x - epsX, x + epsX], yrange=[y - epsY, y + epsY],
                             color=[255, 0, 0, 1])
        b.ellipse = plot
        self.graph.add_plot(plot)
        self.csShape.bars.append(b)
    
    '''
    edit a bar which is already exist
    '''
    def edit_bar(self, x, y, material, csArea):
        epsY = self.d / Design.barProcent
        epsX = self.d / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY):
            self.csShape.show_error_message()
            return
        self.csShape.hide_error_message()
        self.focusBar.x = x
        self.focusBar.y = y
        self.focusBar.material = material
        epsY = self.d / Design.barProcent
        epsX = self.d / Design.barProcent
        self.focusBar.ellipse.xrange = [x - epsX, x + epsX]
        self.focusBar.ellipse.yrange = [y - epsY, y + epsY]
    
    '''
    proofs whether the coordinates are in the shape. 
    return True, when the coordinates are not in the shape
    '''
    def proof_coordinates(self, x, y, epsX, epsY):
        if y + epsY > self.csShape.d or y - epsY < 0:
            return True
        x1 = -np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2. - epsX
        x2 = np.sqrt(np.power(self.d / 2., 2) - np.power(y - self.d / 2., 2)) + self.d / 2. + epsX
        print(x1)
        print(x)
        if x < x1 or x > x2:
            return True
        else: 
            return False 
            
    '''
    give the user the possibility to focus a layer or a bar
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.d)
        y = (touch.y - y0) / gh * (self.d)
        # change_bar is a switch
        self.touch_reaction(x, y, self.d, self.d)
    
    '''
    draw the circle
    '''

    def draw_circle(self):
        self.circle = Ellipse()
        self.circle.xrange = [0, self.graph.xmax]
        self.circle.yrange = [0, self.graph.ymax]
        self.circle.color = [0, 0, 0, 1]
        self.graph.add_plot(self.circle)