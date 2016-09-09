'''
Created on 12.05.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from materialEditor.materiallist import MaterialList
from ownComponents.design import Design
from shapes.shapeCircle import ShapeCircle
from shapes.shapeDoubleT import ShapeDoubleT
from shapes.shapeRectangle import ShapeRectangle
from shapes.shapeT import ShapeT


class CrossSection(GridLayout):
    
    '''
    the cross-section-object contains all shapes. the object manage which shape-should
    will be show
    '''
    
    # cross section editor
    csEditor = ObjectProperty()
    
    # reinforcement editor
    reEditor = ObjectProperty()
    
    # cross section view
    view = ObjectProperty()
    
    # explorer to show the strain-stress-behavior
    explorer = ObjectProperty()
    
    #rectangle-shape
    csRectangle = ObjectProperty(ShapeRectangle())
    
    #doubleT/I-shape
    csDoubleT = ObjectProperty(ShapeDoubleT())
    
    #T-shape
    csT = ObjectProperty(ShapeT())
    
    #circle-shape
    csCircle = ObjectProperty(ShapeCircle())
    
    ###################################
    # here you can add more shapes    #
    ###################################
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.allMaterials = MaterialList.Instance()
        self.view = self.csRectangle.view
    
    ######################################################
    # When you add more shapes, make sure that the shapes#
    # has a show-method like show_rectangle_view         #
    ######################################################
    
    '''
    show the rectangle-view
    '''
    
    def show_rectangle_shape(self):
        self.remove_widget(self.view)
        self.view = self.csRectangle.view
        self.reEditor.change_cross_section(self.view)
        
    '''
    show the doubleT-view
    '''
        
    def show_doublet_shape(self):
        self.remove_widget(self.view)
        self.view = self.csDoubleT.view
        self.reEditor.change_cross_section(self.csDoubleT)
        
    '''
    show the T-view
    '''
        
    def show_tshape(self):
        self.remove_widget(self.view)
        self.view = self.csT.view
        self.reEditor.change_cross_section(self.view)
    
    '''
    show the circle-View
    '''
        
    def show_circle_shape(self):
        self.remove_widget(self.view)
        self.view = self.csCircle.view
        self.reEditor.change_cross_section(self.view)
        
    '''
    set the reinforcement editor
    '''
        
    def set_reinforcement_editor(self, reEditor):
        self.reEditor = reEditor
        self.csRectangle.information = reEditor
        self.csDoubleT.information = reEditor
        self.csT.information = reEditor
        self.csCircle.information = reEditor
