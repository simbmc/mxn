'''
Created on 26.08.2016

@author: mkennert
'''
from kivy.metrics import sp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from crossSectionEditor.rectangleInformation import RectangleInformation
from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from reinforcementEditor.editBar import EditBar
from reinforcementEditor.editLayer import EditLayer


class ReinforcementEditor(GridLayout, IObserver):
    
    '''
    with the ReinforcementEditor you can add or edit new layer or bars to 
    the selected cross-section-shape
    '''
    
    # important components
    editLayer = ObjectProperty()
    editBar = ObjectProperty()
    
    # strings
    addLayerStr = StringProperty('add layer')
    deleteLayerStr = StringProperty('delete layer')
    addBarStr = StringProperty('add bar')
    deleteBarStr = StringProperty('delete bar')
    
    
    # constructor
    def __init__(self, **kwargs):
        super(ReinforcementEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.editLayer = EditLayer(p=self)
        self.editBar = EditBar(p=self)
        self.barAreaVisible = False
        self.layerAreaVisible = False
        self.error = False
        self.containsView = False
    
    def create_gui(self):
        self.errorLbl = OwnLabel(text='[color=ff3333]error: wrong parameters[/color]',
                                  markup=True, size_hint_y=None, height=sp(20))
        self.create_add_delete()
        self.create_material_options()

    '''
    the method create_add_delete create the area where you can 
    add new materials and delete materials from the cs_view
    '''

    def create_add_delete(self):
        self.btnArea = GridLayout(cols=2, row_force_default=True,
                                    row_default_height=Design.btnHeight,
                                    height=Design.btnHeight,
                                    spacing=Design.spacing)
        # create btns
        addBtnLayer = OwnButton(text=self.addLayerStr)
        deleteBtnLayer = OwnButton(text=self.deleteLayerStr)
        addBtnBar = OwnButton(text=self.addBarStr)
        deleteBtnBar = OwnButton(text=self.deleteBarStr)
        # bind btns
        addBtnLayer.bind(on_press=self.show_add_layer_area)
        deleteBtnLayer.bind(on_press=self.delete_layer)
        addBtnBar.bind(on_press=self.show_add_bar_area)
        deleteBtnBar.bind(on_press=self.delete_bar)
        # fill the are with content
        self.btnArea.add_widget(addBtnLayer)
        self.btnArea.add_widget(deleteBtnLayer)
        self.btnArea.add_widget(addBtnBar)
        self.btnArea.add_widget(deleteBtnBar)
        self.add_widget(self.btnArea)
    
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
        self.popupMaterial = OwnPopup(title='material', content=popupContent)
    
    '''
    the method add_layer add a new layer at the cross section
    it use the choosen percent value
    '''
    def add_layer(self, y, csArea, material):
        self.cancel_editing_layer(None)
        self.csShape.add_layer(y, csArea, material)
    
    '''
    edit the selected layer in the view
    '''
    def edit_layer(self, y, csArea, material):
        self.cancel_editing_layer(None)
        self.csShape.edit_layer(y, csArea, material)
        
    '''
    delete the selected layer in the focus view
    '''
    def delete_layer(self):
        self.view.delete_layer()
    
    '''
    the method add_bar add a new layer at the cross section
    it use the choosen percent value
    '''
    def add_bar(self, x, y, csArea, material):
        self.cancel_editing_bar(None)
        self.csShape.add_bar(x, y, csArea, material)
    
    '''
    edit the selected bar in the view
    '''
    def edit_bar(self, x, y, csArea, material):
        self.cancel_editing_bar(None)
        self.csShape.edit_bar(x, y, csArea, material)
                
    '''
    delete the selected bar in the focus view
    '''
    def delete_bar(self):
        self.view.delete_bar()
    
    '''
    show the area where you can add layers
    '''
    def show_add_layer_area(self, btn):
        if not self.layerAreaVisible:
            self.layerAreaVisible = True
            self.editLayer.add = True
            self.remove_widget(self.btnArea)
            self.add_widget(self.editLayer.addArea)
    
    '''
    cancel the editing
    '''
    def cancel_editing_layer(self, btn):
        if self.layerAreaVisible:
            self.layerAreaVisible = False
            self.remove_widget(self.editLayer.addArea)
            self.add_widget(self.btnArea)
        
    '''
    show the area where you can add bars
    '''
    def show_add_bar_area(self, btn):
        if not self.barAreaVisible:
            self.barAreaVisible = True
            self.editBar.add = True
            self.remove_widget(self.btnArea)
            self.add_widget(self.editBar.addArea)
    
    '''
    cancel the editing
    '''
    def cancel_editing_bar(self, btn):
        if self.barAreaVisible:
            self.barAreaVisible = False
            self.remove_widget(self.editBar.addArea)
            self.add_widget(self.btnArea)
    
    '''
    show the error message
    '''

    def show_error_message(self):
        if not self.error:
            self.btnArea.add_widget(self.errorLbl)
            self.error = True
    '''
    hide the error message
    '''

    def hide_error_message(self):
        if self.error:
            self.btnArea.remove_widget(self.errorLbl)
            self.error = False
    
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

    def select_material(self, btn):
        self.popupMaterial.dismiss()
        self.editLayer.materialBtn.text = btn.text
        self.editBar.materialBtn.text = btn.text
    
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
    change the current cross section
    '''

    def change_cross_section(self, shape):
        self.csShape = shape
    
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
        self.crossSection.set_reinforcement_editor(self)
