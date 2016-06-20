'''
Created on 02.06.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from crossSectionEditor.doubleTInformation import DoubleTInformation
from crossSectionEditor.rectangleInformation import RectangleInformation
from crossSectionEditor.shapeSelection import ShapeSelection
from designClass.design import Design
from crossSectionEditor.shapeTInformation import TInformation
from crossSectionEditor.circleInformation import CircleInformation


class CrossSectionEditor(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(CrossSectionEditor, self).__init__(**kwargs)
        self.cols = 2
        self.spacing=20
        self.btnSize = Design.btnSize
        self.firstTimeCircle = True
        self.firstTimeDoubleT = True
        self.firstTimeT=True
        self.focusInformation = None
        self.content = GridLayout(cols=1)
        self.add_widget(self.content)
        self.containsView = True

    '''
    the method set_crossSection was developed to say the view, 
    which cross section should it use
    '''

    def set_crossSection(self, cs):
        self.crossSection = cs
        # default cross section rectangle
        self.csShape = cs.getCSRectangle()
        self.rectangleInformation = RectangleInformation()
        self.shape = self.rectangleInformation
        self.rectangleInformation.set_crossSection(self.csShape)
        self.focusInformation = self.rectangleInformation
        self.createGui()

    '''
    create the gui
    '''

    def createGui(self):
        self.createSelectionMenu()
        self.createPopUpShape()
        self.content.add_widget(self.rectangleInformation, 0)

    '''
    change the current cross section
    '''

    def changeCrossSection(self, shape):
        self.csShape = shape

    '''
    create the layout where you can select the cross-section-shape
    '''

    def createSelectionMenu(self):
        selectionContent = GridLayout(cols=1, spacing=10,
                                      size_hint_y=None, row_force_default=True,
                                      row_default_height=self.btnSize)
        self.btnSelection = Button(text='choose cross section shape', size_hint_y=None, height=self.btnSize,
                                   size_hint_x=None, width=200)
        self.btnSelection.bind(on_press=self.showShapeSelection)
        selectionContent.add_widget(self.btnSelection)
        self.content.add_widget(selectionContent)

    '''
    create popup where you can select the shape of the cross section
    '''

    def createPopUpShape(self):
        shapeContent = ShapeSelection()
        shapeContent.setInformation(self)
        self.shapeSelection = Popup(title='shape', content=shapeContent)

    '''
    look which shape the user has selected
    '''

    def finishedShapeSelection(self, btn):
        if btn.text == 'circle':
            self.setCircle(btn)
            pass
        elif btn.text == 'rectangle':
            self.setRectangle(btn)
        elif btn.text == 'I-shape':
            self.setDoubleT(btn)
        elif btn.text=='T-shape':
            self.setT(btn)
        self.shapeSelection.dismiss()
    
    def cancelShapeSelection(self):
        self.shapeSelection.dismiss()
        

    '''
    open the popup where the user can select the shape
    '''

    def showShapeSelection(self, btn):
        self.shapeSelection.open()

    '''
    show the rectangle shape
    '''

    def setRectangle(self, btn):
        #self.btnSelection.text = btn.text
        self.csShape = self.crossSection.getCSRectangle()
        self.crossSection.view = self.csShape
        self.remove_widget(self.shape)
        self.shape = self.rectangleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.rectangleInformation, 0)
        self.focusInformation = self.rectangleInformation
        self.crossSection.setRectangleView()
        self.updateView()
        self.crossSection.setRectangleView()

    '''
    show the doubleT shape
    '''

    def setDoubleT(self, btn):
        self.csShape = self.crossSection.getCSDoubleT()
        self.crossSection.view = self.csShape
        if self.firstTimeDoubleT:
            self.doubleTInformation = DoubleTInformation()
            self.doubleTInformation.set_crossSection(self.csShape)
            self.firstTimeDoubleT = False
        self.remove_widget(self.shape)
        self.shape = self.doubleTInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.doubleTInformation, 0)
        self.focusInformation = self.doubleTInformation
        self.crossSection.setDoubleTView()
        self.updateView()

    '''
    show the circle shape
    '''
    # not finished yet

    def setCircle(self, btn):
        self.csShape = self.crossSection.getCSCircle()
        self.crossSection.view = self.csShape
        if self.firstTimeCircle:
            self.circleInformation = CircleInformation()
            self.circleInformation.set_crossSection(self.csShape)
            self.firstTimeCircle = False
        self.remove_widget(self.shape)
        self.shape = self.circleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.circleInformation, 0)
        self.focusInformation = self.circleInformation
        self.crossSection.setCircle()
        self.updateView()
    
    def setT(self,btn):
        #self.btnSelection.text = btn.text
        self.csShape = self.crossSection.getCST()
        self.crossSection.view = self.csShape
        if self.firstTimeT:
            self.tInformation = TInformation()
            self.tInformation.set_crossSection(self.csShape)
            self.firstTimeT = False
        self.remove_widget(self.shape)
        self.shape = self.tInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.tInformation, 0)
        self.focusInformation = self.tInformation
        self.crossSection.setTView()
        self.updateView()

    '''
    add the view at the left side of the editor
    '''

    def addView(self):
        self.view = self.crossSection.view
        self.containsView = True
        self.add_widget(self.view, 1)

    '''
    update the view when the shape has changes
    '''

    def updateView(self):
        if self.containsView:
            self.remove_widget(self.view)
            self.view = self.crossSection.view
            self.add_widget(self.view, 1)
            self.containsView = True
    '''
    remove the view of the editor
    '''

    def removeView(self):
        if self.containsView:
            self.remove_widget(self.view)
            self.containsView = False
