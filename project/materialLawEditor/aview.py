'''
Created on 01.09.2016

@author: mkennert
'''
from kivy.properties import  ObjectProperty, StringProperty

from ownComponents.ownGraph import OwnGraph


class AView:
    '''
    base class of the function-views
    '''
    # editor 
    editor = ObjectProperty()
    
    # strain-string for the x-label of the graph
    strainStr = StringProperty('strain')
    
    # stress-string for the y-label of the graph
    stressStr = StringProperty('stress [MPa]')
    
    '''
    create the graph of the view
    '''
    
    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.strainStr, ylabel=self.stressStr,
                              x_ticks_major=0.2, y_ticks_major=0.2,
                              y_grid_label=True, x_grid_label=True,
                              x_grid=True, y_grid=True,
                              xmin=0, xmax=self.editor.maxStrain, ymin=0, ymax=self.editor.upperStress)
        self.add_widget(self.graph)
    
    '''
    update the complete graph by the given function-properties
    '''
        
    def update_function(self, points, minStrain, maxStrain):
        self.line.points = points
        self.graph.ymin, self.graph.ymax = self.find_min_max(points)
        self.graph.xmin, self.graph.xmax = minStrain, maxStrain
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        
    '''
    find the min- and the max-y-coordinate 
    '''
        
    def find_min_max(self, points):
        min_v = 1e10
        max_v = -1e10
        n = len(points)
        for i in range(n):
            c = points[i][1]
            if c < min_v:
                min_v = c
            if c > max_v:
                max_v = c
        return float(min_v), float(max_v)
    
