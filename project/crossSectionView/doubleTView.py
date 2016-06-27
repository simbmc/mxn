'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from bars.bar import Bar
from crossSectionView.aview import AView
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from layers.layer import Layer
from plot.filled_ellipse import FilledEllipse
from plot.filled_rect import FilledRect
from plot.line import LinePlot


class DoubleTView(AView, GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(DoubleTView, self).__init__(**kwargs)
        AView.__init__(self)
        self.cols = 1
        self.layers = []
        self.bars=[]
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.deltaX = self.wmax / 10.
        self.deltaY = self.hmax / 50.
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.wmax + self.deltaX,
            ymin=0, ymax=self.hmax + self.deltaY)
        self.add_widget(self.graph)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_double_t()
        self.graph.add_plot(self.p)

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

    '''
    update the view when the model has changed
    '''

    def update(self):
        # save old values for the update
        self.obw = self.bw
        self.obh = self.bh
        self.omw = self.mw
        self.omh = self.mh
        self.otw = self.tw
        self.oth = self.th
        self.ohmax = self.hmax
        # get the new values
        self.bh = self.csShape.get_height_bottom()
        self.bw = self.csShape.get_width_bottom()
        self.mh = self.csShape.get_height_middle()
        self.mw = self.csShape.get_width_middle()
        self.th = self.csShape.get_height_top()
        self.tw = self.csShape.get_width_top()
        self.hmax = self.csShape.get_height()
        self.wmax = self.csShape.get_width()
        # update graph
        self.update_all_graph()

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, x, y, material):
        mid=self.graph.xmax/2.
        if y>self.hmax:
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            if y<self.bh:
                w1=mid-self.bw/2.
                w2=mid+self.bw/2.
            elif y<self.bh+self.mh:
                w1=mid-self.mw/2.
                w2=mid+self.mw/2.
            else:
                w1=mid-self.tw/2.
                w2=mid+self.tw/2.
            l = Layer(0, y, 0., w1)
            l.set_Material(material)
            line = LinePlot(color=[1, 0, 0, 1], points = [(w1,y),(w2,y)])
            self.graph.add_plot(line)
            self.layers.append(l)
            self.csShape.calculate_strength()
            self.update_cross_section_information()
    
    '''
    add a bar
    '''
    def add_bar(self,x,y, material):
        mid=self.graph.xmax/2.
        epsY=self.hmax/1e2
        epsX=self.wmax/1e2
        if y>self.hmax or x>self.wmax or x<self.deltaX :
            self.csShape.show_error_message()
        elif y<self.bh and (x>mid+self.bw/2. or x<mid-self.bw/2.):
            self.csShape.show_error_message()
        elif y<self.bh+self.mh and y>self.bh and (x>mid+self.mw/2. or x<mid-self.mw/2.):
            self.csShape.show_error_message()
        elif y<self.hmax and y>self.bh+self.mh and (x>mid+self.tw/2. or x<mid-self.tw/2.):
            self.csShape.show_error_message()
        else:
            self.csShape.hide_error_message()
            b=Bar(x,y)
            b.set_Material(material)
            plot=FilledEllipse(xrange=[x-epsX,x+epsX],yrange=[y-epsY,y+epsY],color=[255,0,0,1])
            b.set_filled_ellipse(plot)
            self.graph.add_plot(plot)
            self.bars.append(b)
    
    '''
    update the graph and the layers
    '''
    def update_all_graph(self):
        # update graph
        self.deltaX = self.wmax / 10.
        self.deltaY = self.hmax / 50.
        self.graph.xmax = self.wmax + self.deltaX
        self.graph.ymax = self.hmax + self.deltaY
        self.graph.x_ticks_major = self.graph.xmax / 5.
        self.graph.y_ticks_major = self.graph.ymax / 5.
        self.graph.remove_plot(self.p)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_double_t()
        self.graph.add_plot(self.p)
        self.update_cross_section_information()

    '''
    update the cross section information
    '''

    def update_cross_section_information(self):
        self.csShape.calculate_weight_price()
        self.csShape.calculate_strength()
        self.csShape.set_cross_section_information()

    '''
    delete the selected layer
    '''

    def delete_layer(self):
        if len(self.layers)>0:
            for layer in self.layers:
                if layer.focus:
                    layer.filledRectCs.yrange = [0, 0]
                    layer.filledRectAck.yrange = [0, 0]
                    self.layers.remove(layer)
            self.csShape.calculate_strength()
            self.update_cross_section_information()
            
    '''
    update the layer information in the information-area
    '''

    def update_layer_information(self, name, price, density, stiffness, strength):
        self.csShape.set_layer_information(name, price, density,
                                         stiffness, strength)


    '''
    set the cross section
    '''

    def set_cross_section(self, cs):
        self.csShape = cs
        self.bh = self.csShape.get_height_bottom()
        self.bw = self.csShape.get_width_bottom()
        self.mh = self.csShape.get_height_middle()
        self.mw = self.csShape.get_width_middle()
        self.th = self.csShape.get_height_top()
        self.tw = self.csShape.get_width_top()
        self.hmax = self.csShape.get_height()
        self.wmax = self.csShape.get_width()
        self.create_graph()
