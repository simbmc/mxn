'''
Created on 11.04.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from functions.exponential import Exponential
from functions.linear import Linear
from functions.logarithm import Logarithm
from functions.multilinear import Multilinear
from functions.quadratic import Quadratic
from materialEditor.aeditor import AEditor
from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot


class MaterialEditor(ScrollView, IObserver, AEditor):
    
    '''
    the material-edit is the component, where the user 
    can see the materials and create new material with 
    the material-creater
    '''
    
    # cross-section-shape
    csShape = ObjectProperty()
    
    # switch to proof whether the editor-gui was created
    boolEditor = BooleanProperty(True)
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(MaterialEditor, self).__init__(**kwargs)
        self.allMaterials = self.csShape.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
        
    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''

    def create_gui(self):
        # self.create_material_information()
        self.materialLayout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.materialLayout.bind(minimum_height=self.materialLayout.setter('height'))
        for i in self.allMaterials.allMaterials:
            btn = OwnButton(text=i.name)
            btn.bind(on_press=self.show_material_information)
            self.materialLayout.add_widget(btn)
        self.btnMaterialEditor = OwnButton(text=self.createStr)
        self.btnMaterialEditor.bind(on_press=self.show_creater)
        self.materialLayout.add_widget(self.btnMaterialEditor)
        self.add_widget(self.materialLayout)
        
    '''
    create the popups: 
    popupInfo to show the material information
    popupCreate to create new material
    '''

    def create_popups(self):
        self.create_base_popups()
        self.popupInfo = OwnPopup(title=self.materialStr, content=self.content)
        creater = MaterialCreater(_parent=self)
        self.popupCreate = OwnPopup(title=self.createStr, content=creater)
        
    '''
    create the gui which is necessary for the show of the 
    material-information
    '''

    def create_material_information(self):
        self.create_btns()
        self.content = GridLayout(cols=2, spacing=Design.spacing)
        self.create_information()
        self.information.add_widget(self.btnEdit)
        self.information.add_widget(self.btnBack)
        self.graph = OwnGraph(xlabel=self.strainStr, ylabel=self.stressStr,
                              y_grid_label=True, x_grid_label=True)
        self.p = LinePlot(color=[0, 0, 0])
        self.graph.add_plot(self.p)
        self.content.add_widget(self.graph)
        self.content.add_widget(self.information)
        self.create_popups()
    
    '''
    create all btns of the component
    '''
        
    def create_btns(self):
        self.create_base_btns()
        self.btnBack, self.btnEdit = OwnButton(text=self.cancelStr), OwnButton(text=self.okStr)
        self.btnBack.bind(on_press=self.cancel_show)
        self.btnEdit.bind(on_press=self.edit_material)

    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''

    def update(self):
        self.materialLayout.remove_widget(self.btnMaterialEditor)
        btnMaterialA = OwnButton(text=self.allMaterials.allMaterials[-1].name)
        btnMaterialA.bind(on_press=self.show_material_information)
        self.materialLayout.add_widget(btnMaterialA)
        self.materialLayout.add_widget(self.btnMaterialEditor)
    
    '''
    edit the selected material. all components which use 
    this material will have the new properties
    '''
        
    def edit_material(self, btn):
        self.focusBtnMaterial.text = self.nameBtn.text
        self.focusMaterial.name = self.nameBtn.text
        self.focusMaterial.density = float(self.densityBtn.text)
        self.focusMaterial.price = float(self.priceBtn.text)
        self.focusMaterial.materialLaw = self.materialLawEditor.f
        self.cancel_show(None)
    
    '''
    set the labeltext with the materialproperties and  open the popup
    to edit the material
    '''

    def show_material_information(self, btn):
        if self.boolEditor:
            self.create_material_information()
            self.boolEditor = False
        for material in self.allMaterials.allMaterials:
            if material.name == btn.text:
                self.focusBtnMaterial = btn
                self.focusMaterial = material
                self.materialLawEditor.f = material.materialLaw
                self.nameBtn.text = material.name
                self.priceBtn.text = str(material.price)
                self.densityBtn.text = str(material.density)
                self.materialLaw.text = material.materialLaw.f_toString()
                self.update_graph(material.materialLaw.minStrain, material.materialLaw.maxStrain,
                                  material.materialLaw.points)
                self.popupInfo.open()
                return

    '''
    show the material-law
    '''
        
    def show_material_law_editor(self, btn):
        f = self.focusMaterial.materialLaw
        self.materialLawEditor.f = f
        if isinstance(f, Linear):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnLinear
            self.materialLawEditor.linearEditor.update_function(f.points, f.minStrain,
                                                                f.maxStrain, f.a)
            self.materialLawEditor.confirm(None)
        elif isinstance(f, Multilinear):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnMultiLinear
            self.materialLawEditor.confirm(None)
        elif isinstance(f, Quadratic):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnQuadratic
            self.materialLawEditor.quadraticEditor.update_function(f.points, f.minStrain,
                                                                f.maxStrain, f.a, f.b)
            self.materialLawEditor.confirm(None)
        elif isinstance(f, Exponential):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnExponential
            self.materialLawEditor.exponentialEditor.update_function(f.points, f.minStrain,
                                                                f.maxStrain, f.a, f.b)
            self.materialLawEditor.confirm(None)
        elif isinstance(f, Logarithm):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnLogarithm
            self.materialLawEditor.logarithmEditor.update_function(f.points, f.minStrain,
                                                                f.maxStrain, f.a, f.b)
            self.materialLawEditor.confirm(None)
        self.popupLawEditor.open()
    
    '''
    open the material-creater
    '''
        
    def show_creater(self, btn):
        if self.boolEditor:
            self.create_material_information()
            self.boolEditor = False
        self.popupCreate.open()
                
    '''
    cancel the create-process. this method is necessary, because editor creator-instance call 
    the method cancel_edit_materialfrom the parent
    '''

    def cancel_edit_material(self):
        self.popupCreate.dismiss()
    
    '''
    close the popup, which shows the information from
    the chosen material
    '''

    def cancel_show(self, button):
        self.popupInfo.dismiss()
