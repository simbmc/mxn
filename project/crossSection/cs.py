'''
Created on 12.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from materialEditor.materiallist import MaterialList
from shapes.shapeDoubleT import ShapeDoubleT
from shapes.shapeRectangle import ShapeRectangle
from shapes.shapeT import ShapeT
from shapes.shapeCircle import ShapeCircle


class CrossSection(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols=2
        self.allMaterials=MaterialList()
        self.csRectangle=ShapeRectangle()
        self.csDoubleT=ShapeDoubleT()
        self.csT=ShapeT()
        self.csCircle=ShapeCircle()
        self.view=self.csRectangle.view
    
    '''
    return the cs-rectangle-shape
    '''
    def get_cs_rectangle(self):
        return self.csRectangle
    
    '''
    return the cs-doubleT-shape
    '''
    def get_cs_double_t(self):
        return self.csDoubleT
    '''
    return the csT-shape
    '''
    def get_cs_t(self):
        return self.csT
    
    '''
    return the csCircle-shape
    '''
    def get_cs_circle(self):
        return self.csCircle
    
    '''
    set the rectangle-view
    '''
    def set_rectangle_view(self):
        self.remove_widget(self.view)
        self.view=self.csRectangle.view
        self.reEditor.change_cross_section(self.view)
    
    '''
    set the doubleT-view
    '''
    def set_doublet_view(self):
        self.remove_widget(self.view)
        self.view=self.csDoubleT.view
        self.reEditor.change_cross_section(self.view)
    
    '''
    set the T-view
    '''
    def set_t_view(self):
        self.remove_widget(self.view)
        self.view=self.csT.view
        self.reEditor.change_cross_section(self.view)
    
    '''
    set the circle-View
    '''
    def set_circle(self):
        self.remove_widget(self.view)
        self.view=self.csCircle.view
        self.reEditor.change_cross_section(self.view)
    
    '''
    get the information-component
    '''
    def get_information(self):
        return self.information
    
    '''
    set the cross section editor
    '''
    def set_cross_section_editor(self, csEditor):
        self.csEditor=csEditor
    
    '''
    set the reinforcement editor
    '''
    def set_reinforcement_editor(self,reEditor):
        self.reEditor=reEditor
        self.csRectangle.set_information(reEditor)
        self.csDoubleT.set_information(reEditor)
        self.csT.set_information(reEditor)
        self.csCircle.set_information(reEditor)