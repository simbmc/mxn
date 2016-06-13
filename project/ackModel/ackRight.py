'''
Created on 14.04.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_rect import FilledRect


class AckRight(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(AckRight, self).__init__(**kwargs)
        self.cols = 1
    
    '''
    create the gui of the ack_right
    '''
    def createGui(self):
        self.createGraph()
        self.update()

    '''
    the method createGraph create the graph
    '''

    def createGraph(self):
        self.graph = Graph(xlabel='stress [MPa]', ylabel='height [m]',
                           y_ticks_major=0.1,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=0.0005, ymin=0, ymax=self.csShape.getHeight())
        self.add_widget(self.graph)
    
    
    '''
    the method set_crossSection was developed to say the view, 
    which cross section should it use
    '''

    def set_crossSection(self, cs):
        self.csShape = cs
        self.createGui()

    '''
    ackLeft sign in by ack right
    '''
    def setAckLeft(self, ackLeft):
        self.ackLeft = ackLeft

    '''
    update the layerinformation of layers
    '''
    def update(self):
        self.graph.ymax=self.csShape.getHeight()
        self.graph.y_ticks_major=self.graph.ymax/5.
        self.findMaxStress()
        for plot in self.graph.plots:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        self.concreteLayers=[]
        free_places = self.csShape.view.getFreePlaces()
        for l in free_places:
            filledRect = FilledRect(xrange=[0., 1e-5],
                                   yrange=[l[0], l[1]],
                                   color=[255, 255, 255])
            self.concreteLayers.append(filledRect)
            self.graph.add_plot(filledRect)
        self.updatePlots()
    
    
    def updatePlots(self):
        # the four points determining the ACK curve
        if self.csShape.view.layers:  # reinforcement layer exists
            points = self.ackLeft.calculatePoints()
            eps1, eps2, eps3 = points[1][0], points[2][0], points[3][0]
        else:
            eps1, eps2 = 1e6, 1e6
        # draw the free places of the cross section
        concreteStress = self.csShape.concreteStiffness * \
            self.ack.get_currentStrain() * (self.ack.get_currentStrain() <= eps1)
        maxStress = concreteStress
        for layer in self.concreteLayers:
            layer.xrange=[0.,concreteStress]
        # draw the stress of the reinforcing layers
        for layer in self.csShape.view.layers:
            if self.ack.get_currentStrain() <= eps1:
                layerStress = layer.material.stiffness * self.ack.get_currentStrain()
            elif self.ack.get_currentStrain() <= eps2:
                layerStress = layer.material.stiffness * eps1
            else:
                layerStress = layer.material.stiffness * eps1 + \
                    layer.material.stiffness * (self.ack.get_currentStrain() - eps2)
            maxStress = max(maxStress, layerStress)
            layer.filledRectAck.xrange=[0, layerStress]
            self.graph.add_plot(layer.filledRectAck)
        return self.graph
    
    def findMaxStress(self):
        self.maxStress = self.csShape.concreteStiffness * \
            self.ack.get_maxStrain()
        if self.csShape.view.layers:
            for l in self.csShape.view.layers:
                curValue = l.material.stiffness * self.ack.get_maxStrain()
                if self.maxStress < curValue:
                    self.maxStress = curValue
        self.graph.xmax = self.maxStress
        self.graph.x_ticks_major = int(self.maxStress / 5.)
    
    '''
    set the ack
    '''
    def setAck(self,ack):
        self.ack=ack