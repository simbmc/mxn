'''
Created on 03.06.2016

@author: mkennert
'''
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionView.aview import AView
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.dashedLine import DashedLine
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
from reinforcement.bar import Bar
from reinforcement.layer import Layer


class TView(AView, GridLayout):
    layers, bars = ListProperty([]), ListProperty([])
    csShape = ObjectProperty()
    # Constructor

    def __init__(self, **kwargs):
        super(TView, self).__init__(**kwargs)
        AView.__init__(self)
        self.cols = 1
        self.focusLine=LinePlot(width=1.5,color=Design.focusColor)
        self.lineIsFocused=False
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.update_values()
        self.deltaX = self.cw / 10.
        self.deltaY = self.ch / 50.
        self.graph = OwnGraph(x_ticks_major=0.05, y_ticks_major=0.05,
                              y_grid_label=True, x_grid_label=True, padding=5,
                              xmin=0, xmax=self.cw + self.deltaX,
                              ymin=0, ymax=self.ch + self.deltaY)
        self.add_widget(self.graph)
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.p.points = self.draw_t()
        self.graph.add_plot(self.p)

    '''
    draw the double_T
    '''

    def draw_t(self):
        x0 = self.graph.xmax / 2.
        y1 = self.ch / 1e3
        x1 = x0 - self.bw / 2.
        y2 = self.bh
        x3 = x1 + self.bw / 2. - self.tw / 2.
        #y4 = y3 + self.mh
        #x5 = x3 + self.mw / 2. - self.tw / 2.
        y4 = y2 + self.th
        x5 = x3 + self.tw
        x7 = x5 - self.tw / 2. + self.bw / 2.
        return [(x1, y1), (x1, y2), (x3, y2), (x3, y4), (x5, y4), (x5, y2),
                (x7, y2), (x7, y1), (x1, y1)]

    '''
    update the view when the model has changed
    '''

    def update(self):
        self.update_values()
        self.update_all_graph()
    
    def update_values(self):
        self.bh = self.csShape.get_height_bottom()
        self.bw = self.csShape.get_width_bottom()
        self.th = self.csShape.get_height_top()
        self.tw = self.csShape.get_width_top()
        self.ch = self.csShape.get_height()
        self.cw = self.csShape.get_width()
    
    '''
    update the graph and the layers
    '''

    def update_all_graph(self):
        # update graph
        self.deltaX = self.cw / 10.
        self.deltaY = self.ch / 50.
        self.graph.xmax = self.cw + self.deltaX
        self.graph.ymax = self.ch + self.deltaY
        self.graph.x_ticks_major = self.graph.xmax / 5.
        self.graph.y_ticks_major = self.graph.ymax / 5.
        self.graph.remove_plot(self.p)
        self.p = LinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_t()
        self.graph.add_plot(self.p)
        self.update_cross_section_information()

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, x, y, material):
        mid = self.graph.xmax / 2.
        if y > self.ch:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            if y > self.bh:
                w1 = mid - self.bh / 2.
                w2 = mid + self.bh / 2.
            else:
                w1 = mid - self.th / 2.
                w2 = mid + self.th / 2.
            l = Layer(0, y, 0., w1)
            l.set_Material(material)
            line = DashedLine(color=[1, 0, 0, 1], points=[(w1, y), (w2, y)])
            l.set_line(line)
            self.graph.add_plot(line)
            self.layers.append(l)
            self.csShape.calculate_strength()
            self.update_cross_section_information()
    '''
    add a bar
    '''

    def add_bar(self, x, y, material):
        mid = self.graph.xmax / 2.
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        if y > self.ch or x > self.cw or x < self.deltaX:
            self.csShape.show_error_message()
            print('case 1')
        elif y < self.bh and (x > mid + self.bw / 2. or x < mid - self.bw / 2.):
            self.csShape.show_error_message()
            print('case 2')
        elif y < self.bh + self.th and y > self.bh and (x > mid + self.tw / 2. or x < mid - self.tw / 2.):
            self.csShape.show_error_message()
            print('case 3')
        else:
            self.csShape.hide_error_message()
            b = Bar(x, y)
            b.set_Material(material)
            plot = FilledEllipse(
                xrange=[x - epsX, x + epsX], yrange=[y - epsY, y + epsY], color=[255, 0, 0, 1])
            b.set_filled_ellipse(plot)
            self.graph.add_plot(plot)
            self.bars.append(b)

    '''
    delete the selected layer
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
    give the user the possibility to focus a layer or a bar
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.cw+self.deltaX)
        y = (touch.y - y0) / gh * (self.ch+self.deltaY)
        print('x: ' + str(x))
        print('y: ' + str(y))
        # change_bar is a switch
        change_bar = False
        for bar in self.bars:
            if bar.mouse_within(x, y):
                print('bar')
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
        if x < self.cw:
            for layer in self.layers:
                if layer.mouse_within(y, self.ch / 1e2):
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

    '''
    edit a bar which is already exist
    '''
    def edit_bar(self, x, y, material, csArea):
        self.focusBar.x = x
        self.focusBar.y = y
        self.focusBar.material = material
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        self.focusBar.ellipse.xrange = [x - epsX, x + epsX]
        self.focusBar.ellipse.yrange = [y - epsY, y + epsY]

    '''
    edit a layer which is already exist
    '''
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
