'''
Created on 14.03.2016

@author: mkennert
'''
from plot.filled_ellipse import FilledEllipse
from plot.circle import Circle
'''
the class CSRectangleView was developed to show the the cross section,
which has a rectangle shape
'''

from kivy.uix.gridlayout import GridLayout

from bars.bar import Bar
from crossSectionView.aview import AView
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from layers.layer import Layer
from plot.filled_rect import FilledRect
from plot.line import LinePlot


class CSRectangleView(GridLayout, AView):
    # Constructor

    def __init__(self, **kwargs):
        super(CSRectangleView, self).__init__(**kwargs)
        self.cols = 1
        self.ch = 0.5
        self.cw = 0.25
        self.csShape = None
        self.percent_change = False
        self.layers = []
        self.bars = []
        self.create_graph()

    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = Graph(
            #background_color = [1, 1, 1, 1],
            border_color=[0, 0, 0, 1],
            #tick_color = [0.25,0.25,0.25,0],
            #_trigger_color = [0,0,0,1],
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.cw, ymin=0, ymax=self.ch)
        self.add_widget(self.graph)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_rectangle()
        self.graph.add_plot(self.p)

    '''
    update the graph
    '''

    def update_graph(self):
        self.graph.remove_plot(self.p)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_rectangle()
        self.graph.add_plot(self.p)

    '''
    draw the rectangle
    '''

    def draw_rectangle(self):
        h = self.ch / 1e3
        w = self.cw / 1e3
        return [(w, h), (w, self.ch), (self.cw, self.ch), (self.cw, h), (w, h)]

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, x, y, material):
        if y > self.ch:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            # default height 0
            l = Layer(0, y, 0., self.cw)
            l.set_Material(material)
            line = LinePlot(color=[1, 0, 0, 1], points=[(0, y), (self.cw, y)])
            l.set_line(line)
            self.graph.add_plot(line)
            self.layers.append(l)
            self.csShape.calculate_strength()
            self.update_cross_section_information()

    '''
    add a bar
    '''

    def add_bar(self, x, y, material):
        if y > self.ch or x > self.cw:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            epsY = self.ch / 1e2
            epsX = self.cw / 1e2
            b = Bar(x, y)
            b.set_Material(material)
            plot = FilledEllipse(
                xrange=[x - epsX, x + epsX], yrange=[y - epsY, y + epsY], color=[255, 0, 0, 1])
            b.set_filled_ellipse(plot)
            self.graph.add_plot(plot)
            self.bars.append(b)

    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        if len(self.layers) > 0:
            for layer in self.layers:
                if layer.focus:
                    layer.filledRectCs.yrange = [0, 0]
                    layer.filledRectAck.yrange = [0, 0]
                    self.layers.remove(layer)
            self.csShape.calculate_strength()
            self.update_cross_section_information()

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

    ##########################################################################
    #                                Setter && Getter                        #
    ##########################################################################

    '''
    the method set_height change the height of the cross section shape
    and update the layers
    '''

    def set_height(self, value):
        self.ch = value
        self.graph.ymax = self.ch
        self.update_cross_section_information()
        self.update_graph()

    '''
    the method set_width change the width of the cross section shape
    and update the layers
    '''

    def set_width(self, value):
        self.cw = value
        self.graph.xmax = self.cw
        self.update_cross_section_information()
        self.update_graph()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.csShape = cs

    '''
    return all layers 
    '''

    def get_layers(self):
        return self.layers

    '''
    when the user touch the app
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.cw
        y = (touch.y - y0) / gh * self.ch
        for bar in self.bars:
            if bar.mouse_within(x, y):
                bar.ellipse.color = Design.focusColor
            else:
                bar.ellipse.color = [255, 0, 0]
        if y<self.cw:
            for layer in self.layers:
                if layer.mouse_within(y, self.ch / 1e2):
                    layer.line.color = [0, 0, 0, 1]
                    print('color')
                else:
                    layer.line.color = [1, 0, 0, 1]