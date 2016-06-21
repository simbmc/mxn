'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from plot.circle import Circle


class ShapeSelection(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(ShapeSelection, self).__init__(**kwargs)
        self.cols = 2
        self.btnSize = Design.btnSize

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
    create the rectangle graph
    '''

    def create_graph_rectangle(self):
        self.graphRectangle = Graph(
            #x_ticks_major=0.05, y_ticks_major=0.05,
            #y_grid_label=True, x_grid_label=True, padding=5,
            border_color = [0.5,0.5,0.5,0],
            xmin=0, xmax=0.5, ymin=0, ymax=0.25)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_rectangle()
        self.graphRectangle.add_plot(self.p)
    
    '''
    draw the rectangle
    '''
    def draw_rectangle(self):
        c=1e-2
        h=0.23
        w=0.45
        return [(c,c),(c,h),(w,h),(w,c),(c,c)]
    '''
    create the doubleT graph
    '''

    def create_graph_double_t(self):
        self.graphDoubleT = Graph(
            #x_ticks_major=0.05, y_ticks_major=0.05,
            #y_grid_label=True, x_grid_label=True, padding=5,
            border_color = [0.5,0.5,0.5,0],
            xmin=0, xmax=0.27, ymin=0, ymax=0.65)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_double_t()
        self.graphDoubleT.add_plot(self.p)

    '''
    draw the double_T
    '''

    def draw_double_t(self):
        y1 = 1e-3
        bw=tw=0.25
        mw=0.1
        bh=th=0.15
        mh=0.3
        x1 = bw / 30.
        y2 = y3 = bh
        x3 = x4 = x1 + bw / 2. - mw / 2.
        y4 = y5 = y3 + mh
        x5 = x6 = x4 + mw / 2. - tw / 2.
        y6 = y7 = mh+bh+th
        x7 = x8 = x6 + tw
        x9 = x10 = x8 - tw / 2. + mw / 2.
        x11 = x12 = x10 + tw / 2. - mw / 2.
        points = [(x1, y1), (x1, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6),
                  (x7, y7), (x8, y4), (x9, y4), (x10, y3), (x11, y3), (x12, y1),(x1,y1)]
        return points

    '''
    create the doubleT graph
    '''

    def create_graph_t(self):
        self.graphT = Graph(
            #x_ticks_major=0.05, y_ticks_major=0.05,
            #y_grid_label=True, x_grid_label=True, padding=5,
            border_color = [0.5,0.5,0.5,0],
            xmin=0, xmax=0.27, ymin=0, ymax=0.5)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.draw_t()
        self.graphT.add_plot(self.p)

    '''
    return the t-coordinates to draw
    '''

    def draw_t(self):
        bw = 0.1
        bh = 0.3
        tw = 0.25
        th = 0.15

        x0 = 0.27 / 2.
        y1 = 1e-3
        x1 = x0 - bw / 2.
        y2 = bh
        x3 = x1 + bw / 2. - tw / 2.
        #y4 = y3 + self.mh
        #x5 = x3 + self.mw / 2. - self.tw / 2.
        y4 = y2 + th
        x5 = x3 + tw
        x7 = x5 - tw / 2. + bw / 2.
        return [(x1, y1), (x1, y2), (x3, y2), (x3, y4), (x5, y4), (x5, y2),
                (x7, y2), (x7, y1),(x1,y1)]

    '''
    create the graph circle
    '''

    def create_graph_circle(self):
        self.graphCircle = Graph(
            #x_ticks_major=0.05, y_ticks_major=0.05,
            #y_grid_label=True, x_grid_label=True, padding=5,
            #border_color = [0.5,0.5,0.5,0],
            #xmin=0, xmax=0.51, ymin=0, ymax=0.51)
            xmin=0, xmax=0.51, ymin=0, ymax=0.51)
        self.circle = Circle()
        self.circle.r = 0.25
        self.circle.pos = [0.25, 0.25]
        self.circle.color=[255, 255, 255, 1]
        self.graphCircle.add_plot(self.circle)

    '''
    create the right area where you can select 
    the shape
    '''

    def create_selection(self):
        self.create_btns()
        self.contentRight = GridLayout(cols=1)
        #self.contentRight.add_widget(self.focusShape)
        self.btns = GridLayout(cols=1, spacing=10, size_hint_y=None)
        #self.contentRight.add_widget(self.btns)
        # Make sure the height is such that there is something to scroll.
        self.btns.bind(minimum_height=self.btns.setter('height'))
        self.btns.add_widget(self.rectangle)
        self.btns.add_widget(self.doubleT)
        self.btns.add_widget(self.t)
        self.btns.add_widget(self.circle)
        ###################################################################
        #here you can add more shapes.                                    #
        #implement the button in the create_btns method                   #
        ###################################################################
        layout = GridLayout(cols=2, spacing=15)
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
        self.finishedBtn = Button(
            text='finished', size_hint_y=None, height=self.btnSize)
        self.finishedBtn.bind(on_press=self.finished)
        self.btnOK = Button(text='ok', size_hint_y=None, height=self.btnSize)
        self.btnOK.bind(on_press=self.finished)
        self.btnCancel = Button(
            text='cancel', size_hint_y=None, height=self.btnSize)
        self.btnCancel.bind(on_press=self.cancel)

        # default-shape=rectangle
        self.focusShape = Button(
            text='rectangle', size_hint_y=None, height=self.btnSize)
        self.focusShape.bind(on_press=self.show_shapes_btn)
        # btns
        self.rectangle = Button(
            text='rectangle', size_hint_y=None, height=self.btnSize)
        self.rectangle.bind(on_press=self.show_rectangle)
        self.doubleT = Button(
            text='I-shape', size_hint_y=None, height=self.btnSize)
        self.doubleT.bind(on_press=self.show_double_t)
        self.t = Button(text='T-shape', size_hint_y=None, height=self.btnSize)
        self.t.bind(on_press=self.show_t)
        self.circle = Button(
            text='circle', size_hint_y=None, height=self.btnSize)
        self.circle.bind(on_press=self.show_circle)
        #######################################################################
        #here you can add more shapes                                             #
        #Attention: make sure that the buttons habe the properties                #
        #size_hint_y=None, height=self.btnSize and a bind-method                  #
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

    def show_circle(self, btn):
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

    '''
    set the information
    '''

    def set_information(self, information):
        self.information = information
        self.create_gui()
