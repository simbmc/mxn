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
    
    # important components
    cs = ObjectProperty()
    
    # strings
    circle, rectangle = StringProperty('circle'), StringProperty('rectangle')
    ishape, tshape = StringProperty('I-shape'), StringProperty('T-shape')
    shapeStr = StringProperty('shape')
    
    # constructor
    def __init__(self, **kwargs):
        super(CrossSectionEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.btnSize = Design.btnHeight
        self.firstTimeCircle, self.firstTimeDoubleT = True, True
        self.firstTimeT, self.containsView = True, True
        self.content = GridLayout(cols=1, spacing=Design.spacing)
        self.add_widget(self.content)

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.crossSection = cs
        # default cross section rectangle
        self.csShape = cs.csRectangle
        self.rectangleInformation = RectangleInformation()
        self.shape = self.rectangleInformation
        self.rectangleInformation.csShape = self.csShape
        self.rectangleInformation.create_gui()
        self.focusInformation = self.rectangleInformation
        self.create_gui()

    '''
    create the gui
    '''

    def create_gui(self):
        self.create_popup_shape()
        self.create_selection_menu()
        self.content.add_widget(self.rectangleInformation, 0)

    '''
    create the layout where you can select the cross-section-shape
    '''

    def create_selection_menu(self):
        selectionContent = GridLayout(cols=2, spacing=Design.spacing,
                                      size_hint_y=None, row_force_default=True,
                                      row_default_height=self.btnSize,
                                      height=self.btnSize)
        self.lblSelection = OwnLabel(text=self.shapeStr)
        self.btnSelection = OwnButton(text=self.rectangle)
        self.btnSelection.bind(on_press=self.shapeSelection.open)
        selectionContent.add_widget(self.lblSelection)
        selectionContent.add_widget(self.btnSelection)
        self.content.add_widget(selectionContent)

    '''
    create popup where you can select the shape of the cross section
    '''

    def create_popup_shape(self):
        shapeContent = ShapeSelection()
        shapeContent.information = self
        shapeContent.create_gui()
        self.shapeSelection = OwnPopup(title=self.shapeStr, content=shapeContent)
    
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
        self.view = self.crossSection.view
        self.containsView = True
        self.add_widget(self.view, 1)

    '''
    update the view when the shape has changes
    '''

    def update_view(self):
        if self.containsView:
            self.remove_widget(self.view)
            self.view = self.crossSection.view
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
        self.csShape = self.crossSection.csRectangle
        self.crossSection.view = self.csShape
        self.remove_widget(self.shape)
        self.shape = self.rectangleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.rectangleInformation, 0)
        self.focusInformation = self.rectangleInformation
        self.crossSection.show_rectangle_shape()
        self.update_view()

    '''
    show the doubleT-shape
    '''

    def show_double_t(self, btn):
        self.csShape = self.crossSection.csDoubleT
        self.crossSection.view = self.csShape
        if self.firstTimeDoubleT:
            self.doubleTInformation = DoubleTInformation()
            self.doubleTInformation.csShape = self.csShape
            self.doubleTInformation.create_gui()
            self.firstTimeDoubleT = False
        self.remove_widget(self.shape)
        self.shape = self.doubleTInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.doubleTInformation, 0)
        self.focusInformation = self.doubleTInformation
        self.crossSection.show_doublet_shape()
        self.update_view()

    '''
    show the circle-shape
    '''

    def show_circle_shape(self, btn):
        self.csShape = self.crossSection.csCircle
        self.crossSection.view = self.csShape
        if self.firstTimeCircle:
            self.circleInformation = CircleInformation()
            self.circleInformation.csShape = self.csShape
            self.circleInformation.create_gui()
            self.firstTimeCircle = False
        self.remove_widget(self.shape)
        self.shape = self.circleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.circleInformation, 0)
        self.focusInformation = self.circleInformation
        self.crossSection.show_circle_shape()
        self.update_view()
    
    '''
    show the t-shape
    '''
    def show_t(self, btn):
        self.csShape = self.crossSection.csT
        self.crossSection.view = self.csShape
        if self.firstTimeT:
            self.tInformation = TInformation()
            self.tInformation.csShape = self.csShape
            self.tInformation.create_gui()
            self.firstTimeT = False
        self.remove_widget(self.shape)
        self.shape = self.tInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.tInformation, 0)
        self.focusInformation = self.tInformation
        self.crossSection.show_tshape()
        self.update_view()
