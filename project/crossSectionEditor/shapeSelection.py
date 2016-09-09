'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty
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
    
    # refEditor
    information = ObjectProperty()
    
    circleStr = StringProperty('circle')
    
    rectangleStr = StringProperty('rectangle')
    
    ishapeStr = StringProperty('I-shape')
    
    tshapeStr = StringProperty('T-shape')
    
    shapeStr = StringProperty('shape')
    
    okStr = StringProperty('ok')
    
    cancelStr = StringProperty('cancel')
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(ShapeSelection, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.create_gui()
    
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
        self.graph = OwnGraph(border_color=[1, 1, 1, 1],
                            xmin=0, xmax=0.3, ymin=0, ymax=0.65)
        self.pRec = LinePlot(color=[0, 0, 0, 1], points=self.draw_rectangle())
        self.pdoubleT = LinePlot(color=[0, 0, 0, 1], points=self.draw_double_t())
        self.pT = LinePlot(color=[0, 0, 0, 1], points=self.draw_t())
        self.pCircle = Circle(d=0.225, pos=[0.15, 0.325], color=[0, 0, 0, 1])
        ##########################################################################
        # when you implemented a new shape, make sure that the shape has a plot  #
        ##########################################################################
        self.focusPlot = self.pRec
        self.graph.add_plot(self.focusPlot)
        self.add_widget(self.graph)
    
    '''
    create the right area where you can select 
    the shape
    '''

    def create_selection(self):
        self.create_btns()
        self.contentRight = GridLayout(cols=1)
        # self.contentRight.add_widget(self.focusShape)
        self.btns = GridLayout(cols=1, spacing=Design.spacing, size_hint_y=None)
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
        self.btnOK = OwnButton(text=self.okStr)
        self.btnOK.bind(on_press=self.finished)
        self.btnCancel = OwnButton(text=self.cancelStr)
        self.btnCancel.bind(on_press=self.information.cancel_shape_selection)
        # default-shape=rectangle
        self.focusShape = OwnButton(text=self.rectangleStr)
        # self.focusShape.bind(on_press=self.show_shapes_btn)
        # btns
        self.plot = OwnButton(text=self.rectangleStr)
        self.plot.bind(on_press=self.show_shape)
        self.doubleT = OwnButton(text=self.ishapeStr)
        self.doubleT.bind(on_press=self.show_shape)
        self.t = OwnButton(text=self.tshapeStr)
        self.t.bind(on_press=self.show_shape)
        self.circle = OwnButton(text=self.circleStr)
        self.circle.bind(on_press=self.show_shape)
        #######################################################################
        # here you can add more shapes                                         #
        # Attention: make sure that the buttons habe the properties            #
        # size_hint_y=None, height=Design.btnHeight and a bind-method          #
        #######################################################################
    
    '''
    finished the totally selection and call the 
    finished_shape_selection of the information
    '''

    def finished(self, btn):
        self.information.finished_shape_selection(self.focusShape)
    
    
    ##############################################
    # every shape must implement a show-method  #
    ##############################################
    
    def show_shape(self, btn):
        while self.graph.plots:
            self.graph.remove_plot(self.focusPlot)
        if btn.text == self.circleStr:
            self.focusPlot = self.pCircle
        elif btn.text == self.rectangleStr:
            self.focusPlot = self.pRec
        elif btn.text == self.ishapeStr:
            self.focusPlot = self.pdoubleT
        elif btn.text == self.tshapeStr:
            self.focusPlot = self.pT
        self.focusShape.text = btn.text
        self.graph.add_plot(self.focusPlot)

    ######################################
    # help-methods to draw the shapes    #
    ######################################
    
    '''
    draw a rectangle
    '''
        
    def draw_rectangle(self):
        c, h, w = 0.02, 0.6, 0.25
        return [(c, 0.005), (c, h), (w, h), (w, 0.005), (c, 0.005)]
    
    '''
    return the t-coordinates to draw
    '''

    def draw_t(self):
        bw, bh = 0.1, 0.4
        tw, th = 0.25, 0.2
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
