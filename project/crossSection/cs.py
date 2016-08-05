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
from ownComponents.design import Design
from kivy.properties import ObjectProperty

class CrossSection(GridLayout):
    '''
    cross section contains all shapes. it manage which shape-should
    will be show
    '''
    csEditor, information = ObjectProperty(), ObjectProperty()
    reEditor, view = ObjectProperty(), ObjectProperty()
    ###################################
    # here you can add more shapes    #
    ###################################
    csRectangle, csDoubleT = ObjectProperty(ShapeRectangle()), ObjectProperty(ShapeDoubleT())
    csT, csCircle = ObjectProperty(ShapeT()), ObjectProperty(ShapeCircle())
    
    # constructor
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
        self.reEditor.change_cross_section(self.view)
    
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
        self.csRectangle.set_information(reEditor)
        self.csDoubleT.set_information(reEditor)
        self.csT.information = reEditor
        self.csCircle.set_information(reEditor)
