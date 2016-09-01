'''
Created on 03.06.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from crossSectionView.aview import AView
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.dashedLine import DashedLine
from plot.line import LinePlot


class TView(AView, GridLayout):
    
    '''
    the class TView was developed to show the t-shape of 
    the cross-section
    '''
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(TView, self).__init__(**kwargs)
        AView.__init__(self)
        print('create t-view')
        self.cols = 1
        
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
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, y, csArea, material):
        mid = self.graph.xmax / 2.
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
        else:
            if y > self.bh:
                w1 = mid - self.bh / 2.
                w2 = mid + self.bh / 2.
            else:
                w1 = mid - self.th / 2.
                w2 = mid + self.th / 2.
            line = DashedLine(color=[1, 0, 0, 1], points=[(w1, y), (w2, y)])
            self.create_layer(y, csArea, w2 - w1, material, line)
    
    '''
    edit a layer which is already exist
    '''
    def edit_layer(self, y, material, csArea):
        mid = self.graph.xmax / 2.
        if y >= self.ch or y <= 0:
            self.csShape.show_error_message()
            return
        if y < self.bh:
            self.focusLayer.line.points = [(mid - self.bw / 2., y), (mid - self.bw / 2. + self.bw, y)]
        else:
            self.focusLayer.line.points = [(mid - self.tw / 2., y), (mid - self.tw / 2. + self.tw, y)]
        self.update_layer_properties(y, material, csArea)
    
    '''
    add a bar
    '''

    def add_bar(self, x, y, csArea, material):
        mid = self.graph.xmax / 2.
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY, mid):
            self.csShape.show_error_message()
        else:
            self.create_bar(x, y, csArea, material, epsX, epsY)
    
    '''
    edit a bar which is already exist
    '''
            
    def edit_bar(self, x, y, csArea, material):
        mid = self.graph.xmax / 2.
        epsY = self.ch / Design.barProcent
        epsX = self.cw / Design.barProcent
        if self.proof_coordinates(x, y, epsX, epsY, mid):
            self.csShape.show_error_message()
        else:
            self.update_bar_properties(x, y, csArea, material, epsX, epsY)
    
    '''
    update the view when the model has changed
    '''

    def update(self):
        self.update_values()
        self.update_all_graph()
    
    '''
    update the local values with the values of the shape
    '''
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
        self.p.points = self.draw_t()
              
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
        self.touch_reaction(x, y, self.cw, self.ch)
    
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