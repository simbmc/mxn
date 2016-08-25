'''
Created on 14.03.2016

@author: mkennert
'''

from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.aview import AView
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.dashedLine import DashedLine
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
from reinforcement.bar import Bar
from reinforcement.layer import Layer


class CSRectangleView(GridLayout, AView):
    
    # important components
    csShape = ObjectProperty()
    
    # important values
    # heigth, width of the cross-section
    ch, cw = NumericProperty(0.5), NumericProperty(0.25)
    
    # strings
    ylabelStr = StringProperty('cross-section-height [m]')
    xlabelStr = StringProperty('cross-section-width [m]')
    
    # Constructor
    def __init__(self, **kwargs):
        super(CSRectangleView, self).__init__(**kwargs)
        self.cols = 1
        self.focusLine = LinePlot(width=1.5, color=Design.focusColor)
        self.lineIsFocused = False
        self.create_graph()

    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.xlabelStr, ylabel=self.ylabelStr,
                              x_ticks_major=0.05, y_ticks_major=0.05,
                              y_grid_label=True, x_grid_label=True, padding=5,
                              xmin=0, xmax=self.cw, ymin=0, ymax=self.ch)
        self.add_widget(self.graph)
        self.p = LinePlot(color=[0, 0, 0])
        self.p.points = self.draw_rectangle()
        self.graph.add_plot(self.p)

    '''
    update the graph
    '''

    def update_graph(self):
        self.graph.remove_plot(self.p)
        self.p = LinePlot(color=[0, 0, 0])
        self.p.points = self.draw_rectangle()
        self.graph.add_plot(self.p)

    '''
    draw the rectangle
    '''

    def draw_rectangle(self):
        h, w = self.ch / 1e3, self.cw / 1e3
        return [(w, h), (w, self.ch), (self.cw, self.ch), (self.cw, h), (w, h)]

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, x, y, material):
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            # default height 0
            l = Layer(0, y, 0., self.cw)
            l.material = material  # set_Material(material)
            line = DashedLine(color=[1, 0, 0, 1], points=[(0, y), (self.cw, y)])
            l.line = line  # set_line(line)
            self.graph.add_plot(line)
            self.csShape.layers.append(l)
    
    '''
    edit a layer which is already exist
    '''
        
    def edit_layer(self, y, material, csArea):
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            self.focusLayer.y = y
            self.focusLayer.material = material
            self.focusLayer.line.points = [(0, y), (self.cw, y)]
            if self.lineIsFocused:
                self.graph.remove_plot(self.focusLine)
    
    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        print('delete layer (rectangle)')
        if len(self.csShape.layers) > 0:
            print(len(self.csShape.layers))
            for layer in self.csShape.layers:
                print('layers: ')
                if layer.focus:
                    print('focus')
                    self.csShape.layers.remove(layer)
                    self.graph.remove_plot(layer.line)
                    self.graph.remove_plot(self.focusLine)
    
    '''
    add a bar
    '''

    def add_bar(self, x, y, material):
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        if y + epsY > self.ch or y - epsY < 0 or x + epsX > self.cw or x - epsX < 0:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            b = Bar(x, y)
            b.material = material  # set_Material(material)
            plot = FilledEllipse(xrange=[x - epsX, x + epsX],
                                 yrange=[y - epsY, y + epsY],
                                 color=[255, 0, 0, 1])
            b.ellipse = plot  # set_filled_ellipse(plot)
            self.graph.add_plot(plot)
            self.csShape.bars.append(b)
    
    '''
    edit a bar which is already exist
    '''
    def edit_bar(self, x, y, material, csArea):
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        if y + epsY > self.ch or y - epsY < 0 or x + epsX > self.cw or x - epsX < 0:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            self.focusBar.x = x
            self.focusBar.y = y
            self.focusBar.material = material
            self.focusBar.ellipse.xrange = [x - epsX, x + epsX]
            self.focusBar.ellipse.yrange = [y - epsY, y + epsY]

    # not finished yet
    def delete_bar(self):
        print('delete bar')
        if len(self.csShape.bars) > 0:
            for bar in self.csShape.bars:
                if bar.focus:
                    self.csShape.bars.remove(bar)
                    self.graph.remove_plot(bar.ellipse)          

    '''
    the method update_height change the height of the cross section shape
    and update the layers
    '''

    def update_height(self, value):
        self.ch = value
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.y_ticks_major = value / 5.
        self.graph.ymax = self.ch
        self.update_graph()

    '''
    the method update_width change the width of the cross section shape
    and update the layers
    '''

    def update_width(self, value):
        self.cw = value
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.x_ticks_major = value / 5.
        self.graph.xmax = self.cw
        self.update_graph()
        for layer in self.csShape.layers:
            layer.x = self.cw
            layer.line.points = [(0, layer.y), (self.cw, layer.y)]

   
    '''
    give the user the possibility to focus a layer or a bar
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.cw
        y = (touch.y - y0) / gh * self.ch
        # change_bar is a switch
        change_bar = False
        for bar in self.csShape.bars:
            if bar.mouse_within(x, y):  # checks whether the touch is in a bar
                bar.focus = True
                bar.ellipse.color = Design.focusColor
                self.focusBar = bar
                self.csShape.cancel_editing_layer()
                self.csShape.show_edit_bar_area()
                self.csShape.update_bar_information(bar.x, bar.y, bar.material, bar.csArea)
                change_bar = True
            else:
                bar.ellipse.color = [255, 0, 0]
                bar.focus = False
        # make sure that only one reinforcement can be added
        # at the same time
        if change_bar:
            return
        else:
            self.csShape.cancel_editing_bar()
        oneIsFocused = False
        if x < self.cw:
            for layer in self.csShape.layers:
                if layer.mouse_within(y, self.ch / 1e2):  # checks whether the touch is in a layer
                    layer.focus = True
                    oneIsFocused = True
                    self.lineIsFocused = True
                    self.focusLayer = layer
                    self.csShape.cancel_editing_bar()
                    self.csShape.show_edit_area_layer()
                    self.csShape.update_layer_information(layer.y, layer.material, layer.h)
                    self.focusLine.points = layer.line.points
                    self.graph.add_plot(self.focusLine)
                else:
                    layer.focus = False
        if not oneIsFocused and self.lineIsFocused:
            self.graph.remove_plot(self.focusLine)
            self.csShape.cancel_editing_layer()
