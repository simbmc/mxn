'''
Created on 01.09.2016

@author: mkennert
'''
from ownComponents.ownGraph import OwnGraph
from kivy.properties import  ObjectProperty, StringProperty

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
                              x_ticks_major=2, y_ticks_major=2,
                              y_grid_label=True, x_grid_label=True,
                              x_grid=True, y_grid=True,
                              xmin=0, xmax=self.editor.upperStrain, ymin=0, ymax=self.editor.upperStress)
        self.add_widget(self.graph)
    
    '''
    update the complete graph by the given function-properties
    '''
        
    def update_function(self, points, minStress, maxStress, minStrain, maxStrain):
        self.line.points = points
        self.graph.xmin, self.graph.xmax = minStrain, maxStrain
        self.graph.ymin, self.graph.ymax = minStress, maxStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.