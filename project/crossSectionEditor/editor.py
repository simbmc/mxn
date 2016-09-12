'''
Created on 02.06.2016

@author: mkennert
'''
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionEditor.circleInformation import CircleInformation
from crossSectionEditor.doubleTInformation import DoubleTInformation
from crossSectionEditor.rectangleInformation import RectangleInformation
from crossSectionEditor.shapeSelection import ShapeSelection
from crossSectionEditor.shapeTInformation import TInformation
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class CrossSectionEditor(GridLayout):
    
    '''
    the cross section editor is the component where you can 
    select the shape with the shape-selection-component and set 
    the size-properties of the shapes
    '''
    
    # application-main
    app = ObjectProperty()
    
    # cross section
    cs = ObjectProperty()
    
    # cross-section-shape
    csShape = ObjectProperty()
    
    circle = StringProperty('circle')
    
    rectangle = StringProperty('rectangle')
    
    ishape = StringProperty('I-shape')
    
    tshape = StringProperty('T-shape')
    
    shapeStr = StringProperty('shape')
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(CrossSectionEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.content = GridLayout(cols=1, spacing=Design.spacing)
        self.create_gui()
        self.add_widget(self.content)

    '''
    create the gui
    '''

    def create_gui(self):
        self.create_informations()
        shapeContent = ShapeSelection(information=self)
        self.shapeSelection = OwnPopup(title=self.shapeStr, content=shapeContent)
        self.create_selection_menu()
        self.content.add_widget(self.rectangleInformation, 0)
    
    '''
    create all informations of the shapes
    '''
        
    def create_informations(self):
        # create the rectangle-information
        self.rectangleInformation = RectangleInformation(csShape=self.cs.csRectangle)
        self.rectangleInformation.create_gui()
        self.focusInformation = self.rectangleInformation
        self.shape = self.rectangleInformation
        # create double-t-information
        self.doubleTInformation = DoubleTInformation(csShape=self.cs.csDoubleT)
        self.doubleTInformation.create_gui()
        # create circle-information
        self.circleInformation = CircleInformation(csShape=self.cs.csCircle)
        self.circleInformation.create_gui()
        # create t-information
        self.tInformation = TInformation(csShape=self.cs.csT)
        self.tInformation.create_gui()
    
    '''
    create the layout where you can select the cross-section-shape
    '''

    def create_selection_menu(self):
        selectionContent = GridLayout(cols=2, spacing=Design.spacing,
                                      size_hint_y=None, row_force_default=True,
                                      row_default_height=Design.btnHeight,
                                      height=Design.btnHeight)
        self.lblSelection = OwnLabel(text=self.shapeStr)
        self.btnSelection = OwnButton(text=self.rectangle)
        self.btnSelection.bind(on_press=self.shapeSelection.open)
        selectionContent.add_widget(self.lblSelection)
        selectionContent.add_widget(self.btnSelection)
        self.content.add_widget(selectionContent)
    
    '''
    cancel the shape selection and close the shape-editor-popup
    '''
        
    def cancel_shape_selection(self, btn):
        self.shapeSelection.dismiss()
    
    '''
    look which shape the user has selected
    '''

    def finished_shape_selection(self, btn):
        if btn.text == self.circle:
            self.show_circle_shape(btn)
        elif btn.text == self.rectangle:
            self.show_rectangle(btn)
        elif btn.text == self.ishape:
            self.show_double_t(btn)
        elif btn.text == self.tshape:
            self.show_t(btn)
        self.btnSelection.text = btn.text
        self.shapeSelection.dismiss()
    
    '''
    change the current cross section
    '''

    def change_cross_section(self, shape):
        self.view = shape.view
        self.csShape = shape
        
    '''
    add the view at the left side of the editor
    '''

    def add_view(self):
        self.view = self.cs.view
        self.containsView = True
        self.add_widget(self.view, 1)

    '''
    update the view when the shape has changes
    '''

    def update_view(self):
        if self.containsView:
            self.remove_widget(self.view)
            self.view = self.cs.view
            self.add_widget(self.view, 1)
            self.containsView = True
            
    '''
    remove the view of the editor
    '''

    def remove_view(self):
        if self.containsView:
            self.remove_widget(self.view)
            self.containsView = False
    
    
    #################################
    # show-methods of the shapes    #
    #################################
    
    '''
    show the rectangle-shape
    '''

    def show_rectangle(self, btn):
        self.csShape = self.cs.csRectangle
        self.cs.view = self.csShape
        self.remove_widget(self.shape)
        self.shape = self.rectangleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.rectangleInformation, 0)
        self.focusInformation = self.rectangleInformation
        self.cs.show_rectangle_shape()
        if self.app.boolExplorer:
            self.app.create_explorer()
            self.app.boolExplorer = False
        self.cs.explorer.update_csShape(self.cs.csRectangle, self.cs.csRectangle.ch,
                                         self.cs.csRectangle.layers, self.cs.csRectangle.bars)
        self.update_view()

    '''
    show the doubleT-shape
    '''

    def show_double_t(self, btn):
        self.csShape = self.cs.csDoubleT
        self.cs.view = self.csShape
        self.remove_widget(self.shape)
        self.shape = self.doubleTInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.doubleTInformation, 0)
        self.focusInformation = self.doubleTInformation
        self.cs.show_doublet_shape()
        if self.app.boolExplorer:
            self.app.create_explorer()
            self.app.boolExplorer = False
        self.cs.explorer.update_csShape(self.cs.csDoubleT,
                                         self.cs.csDoubleT.get_total_height(),
                                         self.cs.csDoubleT.layers, self.cs.csDoubleT.bars)
        self.update_view()

    '''
    show the circle-shape
    '''

    def show_circle_shape(self, btn):
        self.csShape = self.cs.csCircle
        self.cs.view = self.csShape
        self.remove_widget(self.shape)
        self.shape = self.circleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.circleInformation, 0)
        self.focusInformation = self.circleInformation
        self.cs.show_circle_shape()
        if self.app.boolExplorer:
            self.app.create_explorer()
            self.app.boolExplorer = False
        self.cs.explorer.update_csShape(self.cs.csCircle, self.cs.csCircle.d,
                                        self.cs.csCircle.layers, self.cs.csCircle.bars)
        self.update_view()
    
    '''
    show the t-shape
    '''
        
    def show_t(self, btn):
        self.csShape = self.cs.csT
        self.cs.view = self.csShape
        self.remove_widget(self.shape)
        self.shape = self.tInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.tInformation, 0)
        self.focusInformation = self.tInformation
        self.cs.show_tshape()
        if self.app.boolExplorer:
            self.app.create_explorer()
            self.app.boolExplorer = False
        self.cs.explorer.update_csShape(self.cs.csT, self.cs.csT.get_total_height(),
                                         self.cs.csT.layers, self.cs.csT.bars)
        self.update_view()
