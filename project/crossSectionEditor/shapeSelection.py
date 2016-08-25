'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty,StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from plot.circle import Circle
from plot.line import LinePlot


class ShapeSelection(GridLayout):
    
    '''
    create the component, where you can select
    the currently cross-section-shape 
    '''
    
    # important components
    information = ObjectProperty()
    
    # strings
    circleStr, rectangleStr = StringProperty('circle'), StringProperty('rectangle')
    ishapeStr, tshapeStr = StringProperty('I-shape'), StringProperty('T-shape')
    shapeStr = StringProperty('shape')
    
    # constructor
    def __init__(self, **kwargs):
        super(ShapeSelection, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing

    '''
    create the gui
    '''

    def create_gui(self):
        self.create_graphs()
        self.create_selection()
    '''
    create all graphs
    '''

    def create_graphs(self):
        self.create_graph_rectangle()
        self.create_graph_double_t()
        self.create_graph_t()
        self.create_graph_circle()
        # default-shape Rectangle
        self.add_widget(self.graphRectangle)
        self.focusGraph = self.graphRectangle
        self.create_graph_double_t()

    '''
    create the plot graph
    '''

    def create_graph_rectangle(self):
        self.graphRectangle = OwnGraph(border_color=[1, 1, 1, 1],
                                       xmin=0, xmax=0.5, ymin=0, ymax=0.25)
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.p.points = self.draw_rectangle()
        self.graphRectangle.add_plot(self.p)
    
    '''
    draw the plot
    '''
    def draw_rectangle(self):
        c, h, w = 0.02, 0.23, 0.45
        return [(c, 0.005), (c, h), (w, h), (w, 0.005), (c, 0.005)]
    '''
    create the doubleT graph
    '''

    def create_graph_double_t(self):
        self.graphDoubleT = OwnGraph(border_color=[0.5, 0.5, 0.5, 0],
                                     xmin=0, xmax=0.27, ymin=0, ymax=0.65)
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.p.points = self.draw_double_t()
        self.graphDoubleT.add_plot(self.p)

    '''
    draw the double_T
    '''

    def draw_double_t(self):
        y1 = 1e-3
        bw = tw = 0.25
        mw, mh = 0.1, 0.3
        bh = th = 0.15
        x1 = bw / 30.
        y2 = y3 = bh
        x3 = x4 = x1 + bw / 2. - mw / 2.
        y4 = y5 = y3 + mh
        x5 = x6 = x4 + mw / 2. - tw / 2.
        y6 = y7 = mh + bh + th
        x7 = x8 = x6 + tw
        x9 = x10 = x8 - tw / 2. + mw / 2.
        x11 = x12 = x10 + tw / 2. - mw / 2.
        points = [(x1, y1), (x1, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6),
                  (x7, y7), (x8, y4), (x9, y4), (x10, y3), (x11, y3), (x12, y1), (x1, y1)]
        return points

    '''
    create the doubleT graph
    '''

    def create_graph_t(self):
        self.graphT = OwnGraph(border_color=[0.5, 0.5, 0.5, 0],
                               xmin=0, xmax=0.27, ymin=0, ymax=0.5)  
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.p.points = self.draw_t()
        self.graphT.add_plot(self.p)

    '''
    return the t-coordinates to draw
    '''

    def draw_t(self):
        bw, bh = 0.1, 0.3
        tw, th = 0.25, 0.15
        x0 = 0.27 / 2.
        y1, y2 = 1e-3, bh
        x1 = x0 - bw / 2.
        x3 = x1 + bw / 2. - tw / 2.
        y4 = y2 + th
        x5 = x3 + tw
        x7 = x5 - tw / 2. + bw / 2.
        return [(x1, y1), (x1, y2), (x3, y2), (x3, y4), (x5, y4), (x5, y2),
                (x7, y2), (x7, y1), (x1, y1)]

    '''
    create the graph circle
    '''

    def create_graph_circle(self):
        self.graphCircle = OwnGraph(xmin=0, xmax=0.51, ymin=0, ymax=0.51)
        self.circle = Circle()
        self.circle.d = 0.25
        self.circle.pos = [0.25, 0.25]
        self.circle.color = [0, 0, 0, 1]
        self.graphCircle.add_plot(self.circle)

    '''
    create the right area where you can select 
    the shape
    '''

    def create_selection(self):
        self.create_btns()
        self.contentRight = GridLayout(cols=1)
        # self.contentRight.add_widget(self.focusShape)
        self.btns = GridLayout(cols=1, spacing=Design.spacing, size_hint_y=None)
        # self.contentRight.add_widget(self.btns)
        # Make sure the height is such that there is something to scroll.
        self.btns.bind(minimum_height=self.btns.setter('height'))
        self.btns.add_widget(self.plot)
        self.btns.add_widget(self.doubleT)
        self.btns.add_widget(self.t)
        self.btns.add_widget(self.circle)
        ###################################################################
        # here you can add more shapes.                                    #
        # implement the button in the create_btns method                   #
        ###################################################################
        layout = GridLayout(cols=2, spacing=Design.spacing)
        layout.add_widget(self.btnOK)
        layout.add_widget(self.btnCancel)
        self.btns.add_widget(layout)
        self.shapes = ScrollView()
        self.shapes.add_widget(self.btns)
        self.contentRight.add_widget(self.shapes)
        self.add_widget(self.contentRight)

    '''
    create and bind all btns from the gui
    '''

    def create_btns(self):
        # finshed button
        self.finishedBtn = OwnButton(text='finished')
        self.finishedBtn.bind(on_press=self.finished)
        self.btnOK = OwnButton(text='ok')
        self.btnOK.bind(on_press=self.finished)
        self.btnCancel = OwnButton(text='cancel')
        self.btnCancel.bind(on_press=self.cancel)
        # default-shape=rectangle
        self.focusShape = OwnButton(text=self.rectangleStr)
        self.focusShape.bind(on_press=self.show_shapes_btn)
        # btns
        self.plot = OwnButton(text=self.rectangleStr)
        self.plot.bind(on_press=self.show_rectangle)
        self.doubleT = OwnButton(text=self.ishapeStr)
        self.doubleT.bind(on_press=self.show_double_t)
        self.t = OwnButton(text=self.tshapeStr)
        self.t.bind(on_press=self.show_t)
        self.circle = OwnButton(text=self.circleStr)
        self.circle.bind(on_press=self.show_circle_shape)
        #######################################################################
        # here you can add more shapes                                             #
        # Attention: make sure that the buttons habe the properties                #
        # size_hint_y=None, height=Design.btnHeight and a bind-method                  #
        #######################################################################

    '''
    show doubleT-View
    '''

    def show_double_t(self, btn):
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphDoubleT, 1)
        self.focusGraph = self.graphDoubleT
        self.focusShape.text = btn.text

    '''
    show T-View
    '''

    def show_t(self, btn):
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphT, 1)
        self.focusGraph = self.graphT
        self.focusShape.text = btn.text

    '''
    show Rectangle-Graph
    '''

    def show_rectangle(self, btn):
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphRectangle, 1)
        self.focusGraph = self.graphRectangle
        self.focusShape.text = btn.text

    '''
    show circle graph
    '''

    def show_circle_shape(self, btn):
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphCircle, 1)
        self.focusGraph = self.graphCircle
        self.focusShape.text = btn.text

    '''
    show the btns where you can select the shape
    '''

    def show_shapes_btn(self, btn):
        self.contentRight.remove_widget(self.focusShape)
        self.contentRight.add_widget(self.shapes)

    '''
    finished the totally selection and call the 
    finished_shape_selection of the information
    '''

    def finished(self, btn):
        self.information.finished_shape_selection(self.focusShape)
        
    '''
    cancel the shape selection 
    '''

    def cancel(self, btn):
        self.information.cancel_shape_selection()

