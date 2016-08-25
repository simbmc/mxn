'''
Created on 02.06.2016
@author: mkennert
'''
from kivy.metrics import sp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from crossSectionEditor.rectangleInformation import RectangleInformation
from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class ReinforcementEditor(GridLayout, IObserver):
    # Constructor

    def __init__(self, **kwargs):
        super(ReinforcementEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.btnSize = Design.btnHeight
        self.content = GridLayout(cols=1, spacing=Design.spacing)
        self.containsView = False
        self.add_widget(self.content)
        self.error = False
        self.barAreaVisible = False
        self.layerAreaVisible = False

    '''
    create the gui
    '''

    def create_gui(self):
        self.numpad = Numpad(p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
        self.create_add_delete()
        self.content.add_widget(self.btnsLayer)
        self.create_add_layer_area()
        self.create_add_bar_area()
        self.create_confirm_cancel()
        self.create_edit_area_layer()
        self.create_edit_area_bar()
        self.errorLbl = OwnLabel(text='[color=ff3333]error: wrong parameters[/color]',
                              markup=True, size_hint_y=None, height=sp(20))

    '''
    change the current cross section
    '''

    def change_cross_section(self, shape):
        self.csShape = shape

    '''
    the method create_add_delete create the area where you can 
    add new materials and delete materials from the cs_view
    '''

    def create_add_delete(self):
        self.btnsLayer = GridLayout(cols=2, row_force_default=True,
                                    row_default_height=Design.btnHeight,
                                    size_hint_y=None, height=Design.btnHeight,
                                    spacing=Design.spacing)
        addBtn = OwnButton(text='add layer')
        deleteBtn = OwnButton(text='delete layer')
        addBtn.bind(on_press=self.show_add_layer_area)
        deleteBtn.bind(on_press=self.delete_layer)
        addBtnBar = OwnButton(text='add bar')
        deleteBtnBar = OwnButton(text='delete bar')
        addBtnBar.bind(on_press=self.show_add_bar_area)
        deleteBtnBar.bind(on_press=self.delete_bar)
        self.btnsLayer.add_widget(addBtn)
        self.btnsLayer.add_widget(deleteBtn)
        self.btnsLayer.add_widget(addBtnBar)
        self.btnsLayer.add_widget(deleteBtnBar)
    
    def delete_layer(self, btn):
        self.view.delete_layer()
    
    def delete_bar(self, btn):
        self.view.delete_bar()
        
    '''
    the method create_add_layer_area create the area where you can 
    add new materials
    '''

    def create_add_layer_area(self):
        self.create_material_options()
        self.addingMaterialArea = GridLayout(cols=2, row_force_default=True,
                                             row_default_height=Design.btnHeight,
                                             size_hint_y=None, height=3 * Design.btnHeight,
                                             spacing=Design.spacing)
        self.addingMaterialArea.add_widget(OwnLabel(text='material:'))
        self.materialOption = OwnButton(text='steel')
        self.materialOption.bind(on_release=self.popup.open)
        self.addingMaterialArea.add_widget(self.materialOption)
        self.stressUpperLimit = OwnButton(text='0.0')
        self.strainUpperLimit = OwnButton(text='0.0')
        self.btn_strain_upper_limit = OwnButton(text='0.0')
        self.btn_stress_upper_limit = OwnButton(text='0.0')
        self.stressUpperLimit.bind(on_press=self.show_numpad)
        self.strainUpperLimit.bind(on_press=self.show_numpad)
        self.btn_strain_upper_limit.bind(on_press=self.show_numpad)
        self.btn_stress_upper_limit.bind(on_press=self.show_numpad)
        self.addingMaterialArea.add_widget(OwnLabel(text='y-coordinate:'))
        self.addingMaterialArea.add_widget(self.strainUpperLimit)
        self.addingMaterialArea.add_widget(OwnLabel(text='cross-sectional area:'))
        self.addingMaterialArea.add_widget(self.stressUpperLimit)

    '''
    the method create_add_layer_area create the area where you can 
    add new materials
    '''

    def create_add_bar_area(self):
        self.addingMaterialAreaBar = GridLayout(cols=2, row_force_default=True,
                                                row_default_height=Design.btnHeight,
                                                size_hint_y=None, height=3 * Design.btnHeight,
                                                spacing=Design.spacing)
        self.addingMaterialAreaBar.add_widget(OwnLabel(text='material:'))
        self.materialOptionBar = OwnButton(text='steel')
        self.materialOptionBar.bind(on_release=self.popup.open)
        self.addingMaterialAreaBar.add_widget(self.materialOptionBar)
        self.barX = OwnButton(text='0.0')
        self.barY = OwnButton(text='0.0')
        self.csArea = OwnButton(text='0.0')
        self.csArea.bind(on_press=self.show_numpad)
        self.barX.bind(on_press=self.show_numpad)
        self.barY.bind(on_press=self.show_numpad)
        self.addingMaterialAreaBar.add_widget(OwnLabel(text='x-coordinate:'))
        self.addingMaterialAreaBar.add_widget(self.barX)
        self.addingMaterialAreaBar.add_widget(OwnLabel(text='y-coordinate:'))
        self.addingMaterialAreaBar.add_widget(self.barY)
        self.addingMaterialAreaBar.add_widget(OwnLabel(text='cross-sectional area:'))
        self.addingMaterialAreaBar.add_widget(self.csArea)

    '''
    the method create_material_options create the popup where you can 
    select the materials for the new layer
    '''

    def create_material_options(self):
        self.layoutMaterials = GridLayout(cols=1, spacing=Design.spacing)
        self.materialEditor = MaterialCreater()
        self.materialEditor._parent = self
        self.popupMaterialEditor = OwnPopup(title='editor', content=self.materialEditor)
        for i in range(0, len(self.allMaterials.allMaterials)):
            btnMaterialA = OwnButton(text=self.allMaterials.allMaterials[i].name)
            btnMaterialA.bind(on_press=self.select_material)
            self.layoutMaterials.add_widget(btnMaterialA)
        self.btnMaterialEditor = OwnButton(text='create material')
        self.btnMaterialEditor.bind(on_press=self.popupMaterialEditor.open)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)
        self.root = ScrollView()
        self.root.add_widget(self.layoutMaterials)
        popupContent = GridLayout(cols=1)
        popupContent.add_widget(self.root)
        self.popup = OwnPopup(title='material', content=popupContent)

    '''
    the method create_confirm_cancel_layer create the area where you can 
    confirm your creation of the new materials or cancel the creation
    '''

    def create_confirm_cancel(self):
        # for layers
        self.confirmCancelArea = GridLayout(cols=2, row_force_default=True,
                                            row_default_height=Design.btnHeight, size_hint_y=None,
                                            height=Design.btnHeight, spacing=Design.spacing)
        confirmBtn = OwnButton(text='ok')
        confirmBtn.bind(on_press=self.add_layer)
        cancelBtn = OwnButton(text='cancel')
        cancelBtn.bind(on_press=self.finished_adding)
        self.confirmCancelArea.add_widget(confirmBtn)
        self.confirmCancelArea.add_widget(cancelBtn)
        # for bars
        self.confirmCancelAreaBar = GridLayout(cols=2, row_force_default=True,
                                               row_default_height=Design.btnHeight, size_hint_y=None,
                                               height=Design.btnHeight, spacing=Design.spacing)
        confirmBar = OwnButton(text='ok')
        confirmBar.bind(on_press=self.add_bar)
        cancelBar = OwnButton(text='cancel')
        cancelBar.bind(on_press=self.finished_adding_bar)
        self.confirmCancelAreaBar.add_widget(confirmBar)
        self.confirmCancelAreaBar.add_widget(cancelBar)
    
    '''
    create the edit layer area
    '''
    def create_edit_area_layer(self):
        self.editArea = GridLayout(cols=2, row_force_default=True,
                                               row_default_height=Design.btnHeight, size_hint_y=None,
                                               height=Design.btnHeight, spacing=Design.spacing)
        cancelBtn = OwnButton(text='cancel')
        cancelBtn.bind(on_press=self.cancel_editing_layer)
        editLayer = OwnButton(text='ok')
        editLayer.bind(on_press=self.edit_layer)
        self.editArea.add_widget(editLayer)
        self.editArea.add_widget(cancelBtn)
    
    '''
    create the edit bar area
    '''
    def create_edit_area_bar(self):
        self.editAreaBar = GridLayout(cols=2, row_force_default=True,
                                               row_default_height=self.btnSize, size_hint_y=None,
                                               height=self.btnSize, spacing=Design.spacing)
        cancelBar = OwnButton(text='cancel')
        cancelBar.bind(on_press=self.cancel_editing_bar)
        editBar = OwnButton(text='ok')
        editBar.bind(on_press=self.edit_bar)
        self.editAreaBar.add_widget(editBar)
        self.editAreaBar.add_widget(cancelBar)
    
    '''
    the method show_add_layer_area was developed to show the 
    the addingMaterialArea and hide the material_information
    '''

    def show_add_layer_area(self, button):
        self.content.remove_widget(self.btnsLayer)
        self.content.add_widget(self.addingMaterialArea, 0)
        self.content.add_widget(self.confirmCancelArea, 1)

    '''
    the method show_add_layer_area was developed to show the 
    the addingMaterialArea and hide the material_information
    '''

    def show_add_bar_area(self, button):
        self.content.remove_widget(self.btnsLayer)
        self.content.add_widget(self.addingMaterialAreaBar, 0)
        self.content.add_widget(self.confirmCancelAreaBar, 1)

    '''
    the method finished_adding was developed to hide the 
    the addingMaterialArea and show the materialArea
    '''

    def finished_adding(self, btn):
        self.content.remove_widget(self.addingMaterialArea)
        self.content.remove_widget(self.confirmCancelArea)
        self.content.add_widget(self.btnsLayer)

    def finished_adding_bar(self, btn):
        self.content.remove_widget(self.addingMaterialAreaBar)
        self.content.remove_widget(self.confirmCancelAreaBar)
        self.content.add_widget(self.btnsLayer)
        
    '''
    the method add_layer add a new layer at the cross section
    it use the choosen percent value
    '''

    def add_layer(self, button):
        self.finished_adding(None)
        for i in range(0, len(self.allMaterials.allMaterials)):
            if self.allMaterials.allMaterials[i].name == self.materialOption.text:
                self.csShape.add_layer(float(self.stressUpperLimit.text), float(self.strainUpperLimit.text),
                                       self.allMaterials.allMaterials[i])
                return
    
    '''
    the method add_layer add a new layer at the cross section
    it use the choosen percent value
    '''

    def add_bar(self, button):
        self.finished_adding_bar(None)
        for i in range(0, len(self.allMaterials.allMaterials)):
            if self.allMaterials.allMaterials[i].name == self.materialOptionBar.text:
                self.csShape.add_bar(float(self.barX.text), float(self.barY.text),
                                     self.allMaterials.allMaterials[i])
                return

    '''
    the method update_layer_information was developed to update
    the information, when the user selected a other rectangle in the view
    '''

    def update_layer_information(self, y, material, csArea):
        self.strainUpperLimit.text = str(y)
        self.materialOption.text = material.name
        self.stressUpperLimit.text = str(csArea)
    
    # not finished yet
    def update_bar_information(self, x, y, material, csArea):
        self.barX.text = str(x)
        self.barY.text = str(y)
        self.materialOptionBar.text = material.name
        self.csArea.text = str(csArea)
    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''

    def update(self):
        self.layoutMaterials.remove_widget(self.btnMaterialEditor)
        btnMaterialA = OwnButton(text=self.allMaterials.allMaterials[-1].name)
        btnMaterialA.bind(on_press=self.select_material)
        self.layoutMaterials.add_widget(btnMaterialA)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)
    
    '''
    the method cancel_edit_material cancel the editing of the material
    and reset the values of the materialEditor
    '''

    def cancel_edit_material(self):
        self.popupMaterialEditor.dismiss()
        self.materialEditor.reset_editor()

    '''
    the method will be called when the user selected a material
    the popup will be closed and the button text change to the material
    name
    '''

    def select_material(self, Button):
        self.popup.dismiss()
        self.materialOption.text = Button.text
        self.materialOptionBar.text = Button.text
    
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
        self.numpad = Numpad(p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)

    '''
    open the numpad popup
    '''

    def show_numpad(self, btn):
        if btn == self.strainUpperLimit:
            self.popupNumpad.title = 'y-coordinate [m]:'
        elif btn == self.stressUpperLimit:
            self.popupNumpad.title = 'cross-section-area:'
        elif btn == self.barX:
            self.popupNumpad.title = 'x-coordinate [m]:'
        elif btn == self.barY:
            self.popupNumpad.title = 'y-coordinate [m]:'
        elif btn == self.csArea:
            self.popupNumpad.title = 'cross-section-area:'
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
        self.btnFocus.text = self.numpad.lblTextinput.text
        self.popupNumpad.dismiss()

    '''
    show the error message
    '''

    def show_error_message(self):
        if not self.error:
            self.btnsLayer.add_widget(self.errorLbl)
            self.error = True
    '''
    hide the error message
    '''

    def hide_error_message(self):
        if self.error:
            self.btnsLayer.remove_widget(self.errorLbl)
            self.error = False
    
    # not finished yet
    def show_edit_layer_area(self):
        if not self.layerAreaVisible:
            self.layerAreaVisible = True
            self.content.add_widget(self.addingMaterialArea, 0)
            self.content.add_widget(self.editArea, 1)
            self.content.remove_widget(self.btnsLayer)
    
    '''
    cancel the editing
    '''
    def cancel_editing_layer(self, btn):
        if self.layerAreaVisible:
            self.layerAreaVisible = False
            self.content.remove_widget(self.addingMaterialArea)
            self.content.remove_widget(self.editArea)
            self.content.add_widget(self.btnsLayer)
    
    # not finished yet
    def show_edit_bar_area(self):
        if not self.barAreaVisible:
            self.barAreaVisible = True
            self.content.add_widget(self.addingMaterialAreaBar, 0)
            self.content.add_widget(self.editAreaBar, 1)
            self.content.remove_widget(self.btnsLayer)
    
    '''
    cancel the editing
    '''
    def cancel_editing_bar(self, btn):
        if self.barAreaVisible:
            self.barAreaVisible = False
            self.content.remove_widget(self.addingMaterialAreaBar)
            self.content.remove_widget(self.editAreaBar)
            self.content.add_widget(self.btnsLayer)
        
    # not finished yet
    def edit_layer(self, btn):
        self.cancel_editing_layer(btn)
        for i in range(0, len(self.allMaterials.allMaterials)):
            if self.allMaterials.allMaterials[i].name == self.materialOption.text:
                self.csShape.edit_layer(float(self.strainUpperLimit.text), self.allMaterials.allMaterials[i], 0)
    
    # not finished yet
    def edit_bar(self, btn):
        self.cancel_editing_bar(btn)
        for i in range(0, len(self.allMaterials.allMaterials)):
            if self.allMaterials.allMaterials[i].name == self.materialOption.text:
                self.csShape.edit_bar(float(self.barX.text), float(self.barY.text),
                                      self.allMaterials.allMaterials[i], 0)
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.crossSection = cs
        self.allMaterials = self.crossSection.allMaterials
        self.allMaterials.add_listener(self)
        # default cross section rectangle
        self.csShape = cs.csRectangle
        self.rectangleInformation = RectangleInformation()
        self.shape = self.rectangleInformation
        self.rectangleInformation.csShape = self.csShape
        self.rectangleInformation.create_gui()
        self.create_gui()
        self.sign_in()
