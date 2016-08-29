'''
Created on 09.05.2016

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


class DoubleTView(AView, GridLayout):
    
    '''
    the class DoubleTView was developed to show the doubleT-shape of 
    the cross-section
    '''
    
    # important components
    csShape = ObjectProperty()
    
    # strings
    ylabelStr = StringProperty('cross-section-height [m]')
    xlabelStr = StringProperty('cross-section-width [m]')
    
    # constructor
    def __init__(self, **kwargs):
        super(DoubleTView, self).__init__(**kwargs)
        AView.__init__(self)
        self.cols = 1
        self.focusLine = LinePlot(width=1.5, color=Design.focusColor)
        self.lineIsFocused = False
        
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        # save the values of the cs shape
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
        self.p.points = self.draw_double_t()
        self.graph.add_plot(self.p)

    '''
    update the view when the model has changed
    '''

    def update(self):
        # get the new values
        self.update_values()
        # update graph
        self.update_all_graph()

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, y, csArea, material):
        mid = self.graph.xmax / 2.
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            if y < self.bh:
                w1 = mid - self.bw / 2.
                w2 = mid + self.bw / 2.
            elif y <= self.bh + self.mh:
                w1 = mid - self.mw / 2.
                w2 = mid + self.mw / 2.
            else:
                w1 = mid - self.tw / 2.
                w2 = mid + self.tw / 2.
            l = Layer(y, csArea, w1)
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
        self.focusLayer.csArea = csArea
        if y < self.bh:
            self.focusLayer.line.points = [(mid - self.bw / 2., y), (mid - self.bw / 2. + self.bw, y)]
        elif y <= self.bh + self.mh:
            self.focusLayer.line.points = [(mid - self.mw / 2., y), (mid - self.mw / 2. + self.mw, y)]
        elif y < self.bh + self.mh + self.th:
            self.focusLayer.line.points = [(mid - self.tw / 2., y), (mid - self.tw / 2. + self.tw, y)]
        if self.lineIsFocused:
            self.focusLine.points = self.focusLayer.line.points
            self.graph.remove_plot(self.focusLine)
                    
    '''
    add a bar
    '''
    def add_bar(self, x, y, csArea, material):
        mid = self.graph.xmax / 2.
        epsY = self.graph.ymax / Design.barProcent
        epsX = self.graph.xmax / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY, mid):
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            b = Bar(x, y, csArea)
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
        epsY = self.graph.ymax / Design.barProcent
        epsX = self.graph.xmax / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY, mid):
            self.csShape.show_error_message()
            return
        self.csShape.hide_error_message()
        self.focusBar.ellipse.xrange = [x - epsX, x + epsX]
        self.focusBar.ellipse.yrange = [y - epsY, y + epsY]
        self.focusBar.x = x
        self.focusBar.y = y
        self.focusBar.material = material
        self.focusBar.csArea = csArea
    
    '''
    update the local values with the values of the shape
    '''
    def update_values(self):
        self.bh = self.csShape.bh
        self.bw = self.csShape.bw
        self.mh = self.csShape.mh
        self.mw = self.csShape.mw
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
        self.p.points = self.draw_double_t()
            
    '''
    proofs whether the coordinates are in the shape. 
    return True, when the coordinates are not in the shape
    '''
    def proof_coordinates(self, x, y, epsX, epsY, mid):
        if y + epsY > self.ch or x > self.cw or x < self.deltaX or y - epsY < 0 :
            return True
        elif y + epsY < self.bh and (x > mid + self.bw / 2. or x < mid - self.bw / 2.):
            return True
        elif y + epsY < self.bh + self.mh and y - epsY > self.bh and (x > mid + self.mw / 2. or x < mid - self.mw / 2.):
            return True
        elif y + epsY < self.ch and y - epsY > self.bh + self.mh and (x > mid + self.tw / 2. or x < mid - self.tw / 2.):
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
        self.touch_reaction(x, y, self.cw, self.ch)
    
    '''
    draw the double_T
    '''
    def draw_double_t(self):
        x0 = self.graph.xmax / 2.
        y1 = self.graph.ymax / 1e3
        x1 = x0 - self.bw / 2.
        y2 = y3 = self.bh
        x3 = x1 + self.bw / 2. - self.mw / 2.
        y4 = y3 + self.mh
        x5 = x3 + self.mw / 2. - self.tw / 2.
        y6 = y4 + self.th
        x7 = x5 + self.tw
        x9 = x7 - self.tw / 2. + self.mw / 2.
        x11 = x9 + self.bw / 2. - self.mw / 2.
        return [(x1, y1), (x1, y2), (x3, y2), (x3, y4), (x5, y4), (x5, y6),
                (x7, y6), (x7, y4), (x9, y4), (x9, y3), (x11, y3), (x11, y1), (x1, y1)]
