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
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.crossSection = cs
        # default cross section rectangle
        self.csShape = cs.get_cs_rectangle()
        self.rectangleInformation = RectangleInformation()
        self.shape = self.rectangleInformation
        self.rectangleInformation.set_cross_section(self.csShape)
        self.focusInformation = self.rectangleInformation
        self.create_gui()

    '''
    create the gui
    '''

    def create_gui(self):
        self.create_selection_menu()
        self.create_pop_up_shape()
        self.content.add_widget(self.rectangleInformation, 0)

    '''
    change the current cross section
    '''

    def change_cross_section(self, shape):
        self.csShape = shape

    '''
    create the layout where you can select the cross-section-shape
    '''

    def create_selection_menu(self):
        selectionContent = GridLayout(cols=1, spacing=10,
                                      size_hint_y=None, row_force_default=True,
                                      row_default_height=self.btnSize)
        self.btnSelection = Button(text='choose cross section shape', size_hint_y=None, height=self.btnSize,
                                   size_hint_x=None, width=200)
        self.btnSelection.bind(on_press=self.show_shape_selection)
        selectionContent.add_widget(self.btnSelection)
        self.content.add_widget(selectionContent)

    '''
    create popup where you can select the shape of the cross section
    '''

    def create_pop_up_shape(self):
        shapeContent = ShapeSelection()
        shapeContent.set_information(self)
        self.shapeSelection = Popup(title='shape', content=shapeContent)

    '''
    look which shape the user has selected
    '''

    def finished_shape_selection(self, btn):
        if btn.text == 'circle':
            self.set_circle(btn)
            pass
        elif btn.text == 'rectangle':
            self.set_rectangle(btn)
        elif btn.text == 'I-shape':
            self.set_double_t(btn)
        elif btn.text=='T-shape':
            self.set_t(btn)
        self.shapeSelection.dismiss()
    
    def cancel_shape_selection(self):
        self.shapeSelection.dismiss()
        

    '''
    open the popup where the user can select the shape
    '''

    def show_shape_selection(self, btn):
        self.shapeSelection.open()

    '''
    show the rectangle shape
    '''

    def set_rectangle(self, btn):
        #self.btnSelection.text = btn.text
        self.csShape = self.crossSection.get_cs_rectangle()
        self.crossSection.view = self.csShape
        self.remove_widget(self.shape)
        self.shape = self.rectangleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.rectangleInformation, 0)
        self.focusInformation = self.rectangleInformation
        self.crossSection.set_rectangle_view()
        self.update_view()
        self.crossSection.set_rectangle_view()

    '''
    show the doubleT shape
    '''

    def set_double_t(self, btn):
        self.csShape = self.crossSection.get_cs_double_t()
        self.crossSection.view = self.csShape
        if self.firstTimeDoubleT:
            self.doubleTInformation = DoubleTInformation()
            self.doubleTInformation.set_cross_section(self.csShape)
            self.firstTimeDoubleT = False
        self.remove_widget(self.shape)
        self.shape = self.doubleTInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.doubleTInformation, 0)
        self.focusInformation = self.doubleTInformation
        self.crossSection.set_doublet_view()
        self.update_view()

    '''
    show the circle shape
    '''
    # not finished yet

    def set_circle(self, btn):
        self.csShape = self.crossSection.get_cs_circle()
        self.crossSection.view = self.csShape
        if self.firstTimeCircle:
            self.circleInformation = CircleInformation()
            self.circleInformation.set_cross_section(self.csShape)
            self.firstTimeCircle = False
        self.remove_widget(self.shape)
        self.shape = self.circleInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.circleInformation, 0)
        self.focusInformation = self.circleInformation
        self.crossSection.set_circle()
        self.update_view()
    
    def set_t(self,btn):
        #self.btnSelection.text = btn.text
        self.csShape = self.crossSection.get_cs_t()
        self.crossSection.view = self.csShape
        if self.firstTimeT:
            self.tInformation = TInformation()
            self.tInformation.set_cross_section(self.csShape)
            self.firstTimeT = False
        self.remove_widget(self.shape)
        self.shape = self.tInformation
        self.content.remove_widget(self.focusInformation)
        self.content.add_widget(self.tInformation, 0)
        self.focusInformation = self.tInformation
        self.crossSection.set_t_view()
        self.update_view()

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
