'''
Created on 01.04.2016

@author: mkennert
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from numpy.random.mtrand import np

from crossSectionView.aview import AView
from kivy.garden.graph import Graph, MeshLinePlot 


class CSCircleView(AView, BoxLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(CSCircleView, self).__init__(**kwargs)
        self.crossSectionRadius = 0.5
        self.layers=[1]
        self.createGraph()
        self.add_widget(self.updateAllGraph)
    
    '''
    the method updateAllGraph update the graph. the method should be called, when
    something has changed
    '''
    @property    
    def updateAllGraph(self):
        #list = []
        '''
        for plot in self.graph.plots:
            list.append(plot)
        for layer in self.layers:
            if layer.focus:
                layer.p = MeshLinePlot(color=[1, 0, 0, 1])
                print(layer.y_coordinate)
            else:
                layer.p = MeshLinePlot(color=layer.colors)
            layer.p._points = self.draw_layer(0.5)
            self.graph.add_plot(layer.p)
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        if len(list)==0:
            self.graph._clear_buffer()
        '''
        self.drawCircle()
        self.p = MeshLinePlot(color=[1, 0, 0, 1])
        self.p._points=self.draw_layer(self.crossSectionRadius)
        self.graph.add_plot(self.p)
        return self.graph
    
    '''
    the method draw_layer was developed to get the _points of the rectangle
    the while_loop was create to make the rectangle set a grid.
    '''
    @staticmethod
    def draw_layer(radius):
        print('Hier')
        points=[]
        fi_outline_arr = np.linspace(0, 2 * np.pi, 60)
        points.append([np.cos(fi_outline_arr) * radius, np.sin(fi_outline_arr) * radius ])
        print(points)
        return points
    
    '''
    the method createGraph create the graph, where you can add 
    the rectangles. the method should be called only once at the beginning
    '''
    def createGraph(self):
        self.graph = Graph(
                        x_ticks_major=0.05, y_ticks_major=0.05,
                        y_grid_label=True, x_grid_label=True, padding=5,
                        xmin=0, xmax=self.crossSectionRadius, ymin=0, ymax=self.crossSectionRadius)
    
    def drawCircle(self):
        print('Hier')
        self.p = MeshLinePlot(color=[1, 0, 0, 1])
        self.p._points = self.draw_layer(0.5)
        self.graph.add_plot(self.p)
        
        
    def setHeight(self,value):
        pass
    
    def setWidth(self, value):
        pass
    
    def setPercent(self, value):
        pass
    
    def addLayer(self, percent,name):
        pass
    
    def deleteLayer(self):
        pass
    
    def updateLayerInformation(self,name,price,density,stiffness,strength,percent):
        pass
    
    '''
    Just for testing
    '''
class TestApp(App):
    def build(self):
        return CSCircleView()

if __name__ == '__main__':
    TestApp().run()