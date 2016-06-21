'''
Created on 01.04.2016

@author: mkennert
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from numpy.random.mtrand import np

from crossSectionView.aview import AView
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from plot.circle import Circle


class CSCircleView(AView, BoxLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(CSCircleView, self).__init__(**kwargs)
        self.crossSectionRadius = 0.5
        self.layers = []

    '''
    the method update_all_graph update the graph. the method should be called, when
    something has changed
    '''
    @property
    def update_all_graph(self):
        self.draw_circle()
        self.p = MeshLinePlot(color=[1, 0, 0, 1])
        self.p._points = self.draw_layer(self.crossSectionRadius)
        self.graph.add_plot(self.p)
        return self.graph

    '''
    the method create_graph create the graph, where you can add 
    the rectangles. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.crossSectionRadius, ymin=0, ymax=self.crossSectionRadius)
        self.draw_circle()
        self.add_widget(self.graph)

    '''
    draw the circle
    '''

    def draw_circle(self):
        self.circle = Circle()
        self.circle.r = 0.25
        self.circle.pos = [self.crossSectionRadius/2., self.crossSectionRadius/2.]
        self.circle.color = [255, 255, 255, 1]
        self.graph.add_plot(self.circle)
    
    
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
    
    '''
    set the cross section
    '''

    def set_cross_section(self, cs):
        self.csShape = cs
        self.r=self.csShape.get_radius()
        self.create_graph()