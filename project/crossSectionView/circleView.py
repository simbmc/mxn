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
    the method updateAllGraph update the graph. the method should be called, when
    something has changed
    '''
    @property
    def updateAllGraph(self):
        self.drawCircle()
        self.p = MeshLinePlot(color=[1, 0, 0, 1])
        self.p._points = self.draw_layer(self.crossSectionRadius)
        self.graph.add_plot(self.p)
        return self.graph

    '''
    the method createGraph create the graph, where you can add 
    the rectangles. the method should be called only once at the beginning
    '''

    def createGraph(self):
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.crossSectionRadius, ymin=0, ymax=self.crossSectionRadius)
        self.drawCircle()
        self.add_widget(self.graph)

    '''
    draw the circle
    '''

    def drawCircle(self):
        self.circle = Circle()
        self.circle.r = 0.25
        self.circle.pos = [self.crossSectionRadius/2., self.crossSectionRadius/2.]
        self.circle.color = [255, 255, 255, 1]
        self.graph.add_plot(self.circle)
    
    
    '''
    the method updateLayerInformation update the layer information of 
    the view_information
    '''
    def updateLayerInformation(self, name, price, density, stiffness, strength):
        self.csShape.setLayerInformation(
            name, price, density, stiffness, strength)

    '''
    the method updateCrossSectionInformation update the cross section information of 
    the view_information
    '''

    def updateCrossSectionInformation(self):
        self.csShape.calculateWeightPrice()
        self.csShape.setCrossSectionInformation()
    
    '''
    return the freePlaces, where is no layer of the cross section
    '''

    def getFreePlaces(self):
        return []
    
    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.r
        y = (touch.y - y0) / gh * self.r
        for l in self.layers:
            if l.mouseWithin(x, y):
                if l.focus == True:
                    self.updateAllGraph()
                    return
                if l.focus == False:
                    l.focus = True
                    l.filledRectCs.color = Design.focusColor
                    info = l.getMaterialInformations()
                    self.csShape.setLayerInformation(info[0], info[1], info[
                        2], info[3], info[4])
            else:
                if l.focus == True:
                    l.focus = False
                    l.filledRectCs.color=l.colors
    
    '''
    set the cross section
    '''

    def set_crossSection(self, cs):
        self.csShape = cs
        self.r=self.csShape.getRadius()
        self.createGraph()