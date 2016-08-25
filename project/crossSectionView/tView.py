'''
Created on 03.06.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty
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
    
    # important components
    csShape = ObjectProperty()
    
    # strings
    ylabelStr = StringProperty('cross-section-height [m]')
    xlabelStr = StringProperty('cross-section-width [m]')
    
    # constructor
    def __init__(self, **kwargs):
        super(TView, self).__init__(**kwargs)
        AView.__init__(self)
        self.cols = 1
        self.focusLine = LinePlot(width=1.5, color=Design.focusColor)
        self.lineIsFocused = False
        
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.update_values()
        self.deltaX = self.cw / 10.
        self.deltaY = self.ch / 50.
        self.graph = OwnGraph(xlabel=self.xlabelStr, ylabel=self.ylabelStr,
                              x_ticks_major=0.05, y_ticks_major=0.05,
                              y_grid_label=True, x_grid_label=True, padding=5,
                              xmin=0, xmax=self.cw + self.deltaX,
                              ymin=0, ymax=self.ch + self.deltaY)
        self.add_widget(self.graph)
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.p.points = self.draw_t()
        self.graph.add_plot(self.p)

    '''
    draw the T
    '''

    def draw_t(self):
        x0, y1 = self.graph.xmax / 2., self.ch / 1e3
        x1, y2 = x0 - self.bw / 2., self.bh
        x3, y4 = x1 + self.bw / 2. - self.tw / 2., y2 + self.th
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
        self.bh = self.csShape.bh  
        self.bw = self.csShape.bw  
        self.th = self.csShape.th  
        self.tw = self.csShape.tw  
        self.ch = self.csShape.get_total_height()
        self.cw = self.csShape.get_max_width()
    
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
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.p.points = self.draw_t()
        self.graph.add_plot(self.p)

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, x, y, material):
        mid = self.graph.xmax / 2.
        if y >= self.ch or y <= 0:
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
            l.material = material
            line = DashedLine(color=[1, 0, 0, 1], points=[(w1, y), (w2, y)])
            l.line = line
            self.graph.add_plot(line)
            self.csShape.layers.append(l)
    
    '''
    edit a layer which is already exist
    '''
    def edit_layer(self, y, material, csArea):
        mid = self.graph.xmax / 2.
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
            return
        self.csShape.hide_error_message()
        self.focusLayer.y = y
        self.focusLayer.material = material
        if y < self.bh:
            self.focusLayer.line.points = [(mid - self.bw / 2., y), (mid - self.bw / 2. + self.bw, y)]
        else:
            self.focusLayer.line.points = [(mid - self.tw / 2., y), (mid - self.tw / 2. + self.tw, y)]
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
        mid = self.graph.xmax / 2.
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY, mid):
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            b = Bar(x, y)
            b.material = material
            plot = FilledEllipse(xrange=[x - epsX, x + epsX], yrange=[y - epsY, y + epsY], color=[255, 0, 0, 1])
            b.ellipse = plot
            self.graph.add_plot(plot)
            self.csShape.bars.append(b)
    
    '''
    edit a bar which is already exist
    '''
    def edit_bar(self, x, y, material, csArea):
        mid = self.graph.xmax / 2.
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY, mid):
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
    proofs whether the coordinates are in the shape. 
    return True, when the coordinates are not in the shape
    '''
    def proof_coordinates(self, x, y, epsX, epsY, mid):
        if y + epsY > self.ch or x > self.cw or x < self.deltaX or y - epsY < 0 :
            return True
        elif y + epsY < self.bh and (x > mid + self.bw / 2. or x < mid - self.bw / 2.):
            return True
        elif y + epsY < self.ch and (x > mid + self.tw / 2. or x < mid - self.tw / 2.):
            return True
        else:
            return False
        
    '''
    give the user the possibility to focus a layer or a bar
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.cw + self.deltaX)
        y = (touch.y - y0) / gh * (self.ch + self.deltaY)
        # change_bar is a switch
        change_bar = False
        for bar in self.csShape.bars:
            if bar.mouse_within(x, y):
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
                if layer.mouse_within(y, self.ch / 1e2):
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
