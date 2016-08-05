'''
Created on 28.07.2016

@author: mkennert
'''

from kivy.garden.graph import Graph,MeshLinePlot
from ownComponents.design import Design


class OwnGraph(Graph):
    '''
    owngraph has properties for the color
    this class make sure, that the uses graphs are the same 
    in every component and make it easier to change properties for 
    all graphs
    '''
    def __init__(self, **kwargs):
        super(OwnGraph, self).__init__(**kwargs)
        self.background_color = [1,1,1,1]
        self.border_color=[0.5,0.5,0.5,1]
        self.color=[0.25,0.25,0.25,1]
        self.label_options.color=Design.foregroundColor
        
