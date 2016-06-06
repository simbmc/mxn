'''
Created on 12.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from materialEditor.materiallist import MaterialList
from shapes.shapeDoubleT import ShapeDoubleT
from shapes.shapeRectangle import ShapeRectangle
from shapes.shapeT import ShapeT


class CrossSection(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols=2
        self.allMaterials=MaterialList()
        self.csRectangle=ShapeRectangle()
        self.csDoubleT=ShapeDoubleT()
        self.csT=ShapeT()
        self.view=self.csRectangle.view
        #self.csRectangle.setInformation(self.information)
        #self.csDoubleT.setInformation(self.information)
        #circle not finished yet
    
    
    '''
    return the cs-rectangle-shape
    '''
    def getCSRectangle(self):
        return self.csRectangle
    
    '''
    return the cs-doubleT-shape
    '''
    def getCSDoubleT(self):
        return self.csDoubleT
    '''
    return the csT-shape
    '''
    def getCST(self):
        return self.csT
    '''
    set the rectangle-view
    '''
    def setRectangleView(self):
        self.remove_widget(self.view)
        self.view=self.csRectangle.view
        self.reEditor.changeCrossSection(self.view)
    
    '''
    set the doubleT-view
    '''
    def setDoubleTView(self):
        self.remove_widget(self.view)
        self.view=self.csDoubleT.view
        self.reEditor.changeCrossSection(self.view)
    
    '''
    set the T-view
    '''
    def setTView(self):
        self.remove_widget(self.view)
        self.view=self.csT.view
        self.reEditor.changeCrossSection(self.view)
    
    '''
    get the information-component
    '''
    def getInformation(self):
        return self.information
    
    '''
    set the cross section editor
    '''
    def setCrossSectionEditor(self, csEditor):
        self.csEditor=csEditor
    
    '''
    set the reinforcement editor
    '''
    def setReinforcementEditor(self,reEditor):
        self.reEditor=reEditor
        self.csRectangle.setInformation(reEditor)
        self.csDoubleT.setInformation(reEditor)
        self.csT.setInformation(reEditor)