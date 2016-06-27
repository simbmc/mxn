'''
Created on 02.06.2016

@author: mkennert

'''
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider

from crossSectionEditor.rectangleInformation import RectangleInformation
from designClass.design import Design
from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from materialEditor.numpad import Numpad


class ReinforcementEditor(GridLayout, IObserver):
    # Constructor

    def __init__(self, **kwargs):
        super(ReinforcementEditor, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 20
        self.btnSize = Design.btnSize
        self.content = GridLayout(cols=1)
        self.containsView = False
        self.add_widget(self.content)
        self.error = False

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.crossSection = cs
        self.allMaterials = self.crossSection.allMaterials
        self.allMaterials.add_listener(self)
        # default cross section rectangle
        self.csShape = cs.get_cs_rectangle()
        self.rectangleInformation = RectangleInformation()
        self.shape = self.rectangleInformation
        self.rectangleInformation.set_cross_section(self.csShape)
        self.create_gui()
        self.sign_in()

    '''
    create the gui
    '''

    def create_gui(self):
        self.create_cross_section_area()
        self.create_numpad()
        self.create_add_delete_layer()
        self.create_add_delete_bar()
        self.create_material_information()
        self.create_add_layer_area()
        self.create_add_bar_area()
        self.create_confirm_cancel_layer()
        self.create_confirm_cancel_bar()

    '''
    change the current cross section
    '''

    def change_cross_section(self, shape):
        self.csShape = shape

    '''
    the method create_add_delete_layer create the area where you can 
    add new materials and delete materials from the cs_view
    '''

    def create_add_delete_layer(self):
        self.btnsLayer = GridLayout(cols=2, row_force_default=True,
                                    row_default_height=self.btnSize,
                                    size_hint_y=None, height=self.btnSize)
        addBtn = Button(
            text='add layer', size_hint_y=None, height=self.btnSize)
        addBtn.bind(on_press=self.show_add_layer_area)
        deleteBtn = Button(
            text='delete layer', size_hint_y=None, height=self.btnSize)
        deleteBtn.bind(on_press=self.delete_layer)
        self.btnsLayer.add_widget(addBtn)
        self.btnsLayer.add_widget(deleteBtn)

    '''
    the method create_add_delete_layer create the area where you can 
    add new materials and delete materials from the cs_view
    '''

    def create_add_delete_bar(self):
        self.btnsBars = GridLayout(cols=2, row_force_default=True,
                                   row_default_height=self.btnSize,
                                   size_hint_y=None, height=self.btnSize)
        addBtn = Button(
            text='add bar', size_hint_y=None, height=self.btnSize)
        addBtn.bind(on_press=self.show_add_bar_area)
        deleteBtn = Button(
            text='delete bar', size_hint_y=None, height=self.btnSize)
        deleteBtn.bind(on_press=self.delete_layer)
        self.btnsBars.add_widget(addBtn)
        self.btnsBars.add_widget(deleteBtn)

    '''
    the method create_material_information create the area where you can 
    see the information about the selected materials
    '''

    def create_material_information(self):
        h = 20
        self.materialArea = GridLayout(cols=1)
        self.materialName = Label(text='-')
        self.materialPrice = Label(text='-')
        self.materialDensity = Label(text='-')
        self.materialStiffness = Label(text='-')
        self.materialStrength = Label(text='-')
        self.materialPercent = Label(text='10 %')
        labelLayout = GridLayout(
            cols=2, row_force_default=True,
            row_default_height=h, size_hint_y=None, height=3 * h)
        labelLayout.add_widget(Label(text='name:', size_hint_y=None, height=h))
        labelLayout.add_widget(self.materialName)
        labelLayout.add_widget(
            Label(text='price:', size_hint_y=None, height=h))
        labelLayout.add_widget(self.materialPrice)
        labelLayout.add_widget(
            Label(text='density:', size_hint_y=None, height=h))
        labelLayout.add_widget(self.materialDensity)
        labelLayout.add_widget(
            Label(text='stiffness:', size_hint_y=None, height=h))
        labelLayout.add_widget(self.materialStiffness)
        labelLayout.add_widget(
            Label(text='tensile strength:', size_hint_y=None, height=h))
        labelLayout.add_widget(self.materialStrength)
        self.errorLbl = Label(text='[color=ff3333]error: wrong parameters[/color]',
                              markup=True, size_hint_y=None, height=20)
        self.materialArea.add_widget(self.btnsLayer)
        self.materialArea.add_widget(self.btnsBars)
        self.content.add_widget(self.materialArea)

    '''
    the method create_cross_section_area create the area where you can 
    see the information of the cs_view
    '''

    def create_cross_section_area(self):
        h = 20
        self.crossSectionPrice = Label(text='-', size_hint_y=None, height=h)
        self.crossSectionWeight = Label(text='-', size_hint_y=None, height=h)
        self.crossSectionStrength = Label(text='-', size_hint_y=None, height=h)
        self.crossSectionArea = GridLayout(
            cols=2, row_force_default=True,
            row_default_height=h, size_hint_y=None, height=3 * h)
        self.crossSectionArea.add_widget(
            Label(text='price [Euro/m]:', size_hint_y=None, height=h))
        self.crossSectionArea.add_widget(self.crossSectionPrice)
        self.crossSectionArea.add_widget(
            Label(text='weight [kg]:', size_hint_y=None, height=h))
        self.crossSectionArea.add_widget(self.crossSectionWeight)
        self.crossSectionArea.add_widget(
            Label(text='tensile strength [MPa]:', size_hint_y=None, height=h))
        self.crossSectionArea.add_widget(self.crossSectionStrength)
        self.content.add_widget(self.crossSectionArea)

    '''
    the method create_add_layer_area create the area where you can 
    add new materials
    '''

    def create_add_layer_area(self):
        self.create_material_options()
        self.addingMaterialArea = GridLayout(
            cols=2, row_force_default=True,
            row_default_height=self.btnSize, size_hint_y=None, height=3 * self.btnSize)
        self.addingMaterialArea.add_widget(Label(text='Material:'))
        self.materialOption = Button(
            text='steel', size_hint_y=None, height=self.btnSize)
        self.materialOption.bind(on_release=self.popup.open)
        self.addingMaterialArea.add_widget(self.materialOption)
        self.btnX = Button(text='0.0', size_hint_y=None, height=self.btnSize)
        self.btnY = Button(text='0.0', size_hint_y=None, height=self.btnSize)
        self.btnHeight = Button(
            text='0.0', size_hint_y=None, height=self.btnSize)
        self.btnWidth = Button(
            text='0.0', size_hint_y=None, height=self.btnSize)
        self.btnX.bind(on_press=self.show_numpad)
        self.btnY.bind(on_press=self.show_numpad)
        self.btnHeight.bind(on_press=self.show_numpad)
        self.btnWidth.bind(on_press=self.show_numpad)
        self.addingMaterialArea.add_widget(Label(text='y-coordinate:'))
        self.addingMaterialArea.add_widget(self.btnY)
        self.addingMaterialArea.add_widget(Label(text='cross-sectional area:'))
        self.addingMaterialArea.add_widget(self.btnX)

    '''
    the method create_add_layer_area create the area where you can 
    add new materials
    '''

    def create_add_bar_area(self):
        self.addingMaterialAreaBar = GridLayout(
            cols=2, row_force_default=True,
            row_default_height=self.btnSize, size_hint_y=None, height=3 * self.btnSize)
        self.addingMaterialAreaBar.add_widget(Label(text='Material:'))
        self.materialOptionBar = Button(
            text='steel', size_hint_y=None, height=self.btnSize)
        self.materialOptionBar.bind(on_release=self.popup.open)
        self.addingMaterialAreaBar.add_widget(self.materialOptionBar)
        self.barX = Button(text='0.0', size_hint_y=None, height=self.btnSize)
        self.barY = Button(text='0.0', size_hint_y=None, height=self.btnSize)
        self.barHeight = Button(
            text='0.0', size_hint_y=None, height=self.btnSize)
        self.barWidth = Button(
            text='0.0', size_hint_y=None, height=self.btnSize)
        self.csArea=Button(text='0.0', size_hint_y=None, height=self.btnSize)
        self.csArea.bind(on_press=self.show_numpad)
        self.barX.bind(on_press=self.show_numpad)
        self.barY.bind(on_press=self.show_numpad)
        self.barHeight.bind(on_press=self.show_numpad)
        self.barWidth.bind(on_press=self.show_numpad)
        self.addingMaterialAreaBar.add_widget(Label(text='x-coordinate:'))
        self.addingMaterialAreaBar.add_widget(self.barX)
        self.addingMaterialAreaBar.add_widget(Label(text='y-coordinate:'))
        self.addingMaterialAreaBar.add_widget(self.barY)
        self.addingMaterialAreaBar.add_widget(Label(text='cross-sectional area:'))
        self.addingMaterialAreaBar.add_widget(self.csArea)

    '''
    the method create_material_options create the popup where you can 
    select the materials for the new layer
    '''

    def create_material_options(self):
        self.layoutMaterials = GridLayout(cols=3)
        self.materialEditor = MaterialCreater()
        self.materialEditor.sign_in_parent(self)
        self.popupMaterialEditor = Popup(
            title='editor', content=self.materialEditor)
        for i in range(0, self.allMaterials.get_length()):
            btnMaterialA = Button(text=self.allMaterials.allMaterials[i].name)
            btnMaterialA.bind(on_press=self.select_material)
            self.layoutMaterials.add_widget(btnMaterialA)
        self.btnMaterialEditor = Button(text='create material')
        self.btnMaterialEditor.bind(on_press=self.popupMaterialEditor.open)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)
        self.popup = Popup(title='materials', content=self.layoutMaterials)

    '''
    the method create_confirm_cancel_layer create the area where you can 
    confirm your creation of the new materials or cancel the creation
    '''

    def create_confirm_cancel_layer(self):
        self.confirmCancelArea = GridLayout(cols=2, row_force_default=True,
                                            row_default_height=self.btnSize, size_hint_y=None,
                                            height=self.btnSize)
        confirmBtn = Button(
            text='confirm', size_hint_y=None, height=self.btnSize)
        confirmBtn.bind(on_press=self.add_layer)
        cancelBtn = Button(
            text='cancel', size_hint_y=None, height=self.btnSize)
        cancelBtn.bind(on_press=self.cancel_adding)
        self.confirmCancelArea.add_widget(confirmBtn)
        self.confirmCancelArea.add_widget(cancelBtn)

    '''
    the method create_confirm_cancel_layer create the area where you can 
    confirm your creation of the new materials or cancel the creation
    '''

    def create_confirm_cancel_bar(self):
        self.confirmCancelAreaBar = GridLayout(cols=2, row_force_default=True,
                                               row_default_height=self.btnSize, size_hint_y=None,
                                               height=self.btnSize)
        confirmBar = Button(
            text='confirm', size_hint_y=None, height=self.btnSize)
        confirmBar.bind(on_press=self.add_bar)
        cancelBar = Button(
            text='cancel', size_hint_y=None, height=self.btnSize)
        cancelBar.bind(on_press=self.cancel_adding_bar)
        self.confirmCancelAreaBar.add_widget(confirmBar)
        self.confirmCancelAreaBar.add_widget(cancelBar)

    '''
    the method show_add_layer_area was developed to show the 
    the addingMaterialArea and hide the material_information
    '''

    def show_add_layer_area(self, button):
        self.content.remove_widget(self.crossSectionArea)
        self.content.remove_widget(self.materialArea)
        self.content.remove_widget(self.btnsLayer)
        self.content.add_widget(self.addingMaterialArea, 0)
        self.content.add_widget(self.confirmCancelArea, 1)

    '''
    the method show_add_layer_area was developed to show the 
    the addingMaterialArea and hide the material_information
    '''

    def show_add_bar_area(self, button):
        self.content.remove_widget(self.crossSectionArea)
        self.content.remove_widget(self.materialArea)
        self.content.remove_widget(self.btnsLayer)
        self.content.add_widget(self.addingMaterialAreaBar, 0)
        self.content.add_widget(self.confirmCancelAreaBar, 1)

    '''
    the method finished_adding was developed to hide the 
    the addingMaterialArea and show the materialArea
    '''

    def finished_adding(self):
        self.content.remove_widget(self.addingMaterialArea)
        self.content.remove_widget(self.confirmCancelArea)
        self.content.add_widget(self.materialArea, 0)
        self.content.add_widget(self.crossSectionArea, 1)

    def finished_adding_bar(self):
        self.content.remove_widget(self.addingMaterialAreaBar)
        self.content.remove_widget(self.confirmCancelAreaBar)
        self.content.add_widget(self.materialArea, 0)
        self.content.add_widget(self.crossSectionArea, 1)
    '''
    the method add_layer add a new layer at the cross section
    it use the choosen percent value
    '''

    def add_layer(self, button):
        self.finished_adding()
        for i in range(0, self.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name == self.materialOption.text:
                self.csShape.add_layer(
                    float(self.btnX.text), float(self.btnY.text),
                    self.allMaterials.allMaterials[i])
                return
        
    '''
    the method add_layer add a new layer at the cross section
    it use the choosen percent value
    '''

    def add_bar(self, button):
        self.finished_adding_bar()
        for i in range(0, self.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name == self.materialOptionBar.text:
                self.csShape.add_bar(
                    float(self.barX.text), float(self.barY.text),
                    self.allMaterials.allMaterials[i])
                return

    '''
    the method cancel_adding would be must call when the user wouldn't 
    add a new layer
    '''

    def cancel_adding(self, button):
        self.finished_adding()

    '''
    the method cancel_adding would be must call when the user wouldn't 
    add a new bar
    '''

    def cancel_adding_bar(self, btn):
        self.finished_adding_bar()

    '''
    the method delete_layer was developed to delete a existing
    layer
    '''

    def delete_layer(self, button):
        self.csShape.delete_layer()

    '''
    the method update_layer_information was developed to update
    the information, when the user selected a other rectangle in the view
    '''

    def update_layer_information(self, name, price, density, stiffness, strength):
        self.materialName.text = str(name)
        self.materialPrice.text = str(price)
        self.materialDensity.text = str(density)
        self.materialStiffness.text = str(stiffness)
        self.materialStrength.text = str(strength)

    '''
    the method update_cross_section_information update the cross section information.
    '''

    def update_cross_section_information(self, price, weight, strength):
        self.crossSectionPrice.text = str(0)
        self.crossSectionWeight.text = str(0)
        self.crossSectionStrength.text = str(0)

    '''
    the method cancel_edit_material cancel the editing of the material
    and reset the values of the materialEditor
    '''

    def cancel_edit_material(self):
        self.popupMaterialEditor.dismiss()
        self.materialEditor.reset_editor()

    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''

    def update(self):
        self.layoutMaterials.remove_widget(self.btnMaterialEditor)
        btnMaterialA = Button(text=self.allMaterials.allMaterials[-1].name)
        btnMaterialA.bind(on_press=self.select_material)
        self.layoutMaterials.add_widget(btnMaterialA)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)

    '''
    the method will be called when the user selected a material
    the popup will be closed and the button text change to the material
    name
    '''

    def select_material(self, Button):
        self.popup.dismiss()
        self.materialOption.text = Button.text

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

    '''
    sign in by the cross section. so the cross section has the 
    instance as a attribute
    '''

    def sign_in(self):
        self.crossSection.set_reinforcement_editor(self)

    '''
    create the numpad
    '''

    def create_numpad(self):
        self.numpad = Numpad()
        self.numpad.sign_in_parent(self)
        self.popupNumpad = Popup(content=self.numpad)

    '''
    open the numpad popup
    '''

    def show_numpad(self, btn):
        self.popupNumpad.open()
        self.btnFocus = btn

    '''
    close the numpad popup
    '''

    def close_numpad(self):
        self.popupNumpad.dismiss()

    '''
    close the numpad popup and 
    set the choosen text with the numpad input
    '''

    def finished_numpad(self):
        self.btnFocus.text = self.numpad.textinput.text
        self.popupNumpad.dismiss()

    '''
    show the error message
    '''

    def show_error_message(self):
        if not self.error:
            self.materialArea.add_widget(self.errorLbl, 3)
            self.error = True
    '''
    hide the error message
    '''

    def hide_error_message(self):
        if self.error:
            self.materialArea.remove_widget(self.errorLbl)
            self.error = False
    
    def edit_layer(self):
        pass
    
    def create_edit_area_layer(self):
        self.edit_delete_area=GridLayout(cols=2, row_force_default=True,
                                               row_default_height=self.btnSize, size_hint_y=None,
                                               height=self.btnSize)
        cancelBtn = Button(
            text='cancel', size_hint_y=None, height=self.btnSize)
        editLayer = Button(
            text='edit', size_hint_y=None, height=self.btnSize)
        self.confirmCancelAreaBar.add_widget(editLayer)
        self.confirmCancelAreaBar.add_widget(cancelBtn)
        