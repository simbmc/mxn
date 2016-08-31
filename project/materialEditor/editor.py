'''
Created on 11.04.2016

@author: mkennert
'''
from kivy.properties import  StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from functions.exponentialFunction import ExponentialFunction
from functions.linearFunction import Linear
from functions.multilinear import Multilinear
from functions.quadraticFunction import QuadraticFunction
from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from materialLawEditor.lawEditor import MaterialLawEditor
from ownComponents.design import Design
from ownComponents.keyboard import Keyboard
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot


class MaterialEditor(ScrollView, IObserver):
    
    '''
    the material-edit is the component, where the user 
    can see the materials and create new material with 
    the material-creater
    '''
    
    # strings
    strainStr, stressStr = StringProperty('strain'), StringProperty('stress [MPa]')
    nameStr, materialStr = StringProperty('name'), StringProperty('material')
    materialLawStr = StringProperty('material-law')
    createStr = StringProperty('create new material')
    priceStr, densityStr = StringProperty('price[euro/kg]'), StringProperty('density[kg/m^3]')
    backStr, editStr = StringProperty('back'), StringProperty('edit')
    okStr, cancelStr = StringProperty('ok'), StringProperty('cancel')
    
    # constructor
    def __init__(self, **kwargs):
        super(MaterialEditor, self).__init__(**kwargs)
        print('create material-editor')
        self.btnSize = Design.btnHeight
        self.firstPlot = True
        
    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''

    def create_gui(self):
        self.create_material_information()
        self.materialLayout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.materialLayout.bind(minimum_height=self.materialLayout.setter('height'))
        for i in self.allMaterials.allMaterials:
            btn = OwnButton(text=i.name)
            btn.bind(on_press=self.show_material_information)
            self.materialLayout.add_widget(btn)
        self.btnMaterialEditor = OwnButton(text=self.createStr)
        self.btnMaterialEditor.bind(on_press=self.create_material)
        self.materialLayout.add_widget(self.btnMaterialEditor)
        self.add_widget(self.materialLayout)
        
    '''
    create the popups: 
    popupInfo to show the material information
    popupCreate to create new material
    '''

    def create_popups(self):
        self.materialLawEditor = MaterialLawEditor(creater=self)
        self.popupLawEditor = OwnPopup(title=self.materialLawStr,
                                       content=self.materialLawEditor)
        creater = MaterialCreater(_parent=self)
        self.numpad = Numpad(p=self)
        self.keyboard = Keyboard(p=self)
        self.popupInfo = OwnPopup(title=self.materialStr, content=self.content)
        self.popupCreate = OwnPopup(title=self.createStr, content=creater)
        self.popupNumpad = OwnPopup(content=self.numpad)
        self.popupKeyboard = OwnPopup(title=self.nameStr, content=self.keyboard)

    '''
    create the gui which is necessary for the show of the 
    material-information
    '''

    def create_material_information(self):
        self.create_btns()
        self.content = GridLayout(cols=2, spacing=Design.spacing)
        self.information = GridLayout(cols=2, spacing=Design.spacing)
        self.information.add_widget(OwnLabel(text=self.nameStr))
        self.information.add_widget(self.name)
        self.information.add_widget(OwnLabel(text=self.priceStr))
        self.information.add_widget(self.price)
        self.information.add_widget(OwnLabel(text=self.densityStr))
        self.information.add_widget(self.density)
        self.information.add_widget(OwnLabel(text=self.materialLawStr))
        self.information.add_widget(self.materialLaw)
        self.information.add_widget(self.btnBack)
        self.information.add_widget(self.btnEdit)
        self.graph = OwnGraph(xlabel=self.strainStr, ylabel=self.stressStr,
                              y_grid_label=True, x_grid_label=True)
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.graph.add_plot(self.p)
        self.content.add_widget(self.information)
        self.content.add_widget(self.graph)
        self.create_popups()
    
    '''
    create all btns of the component
    '''
    def create_btns(self):
        self.name, self.price = OwnButton(), OwnButton()
        self.name.bind(on_press=self.show_keyboard)
        self.price.bind(on_press=self.show_numpad)
        self.density, self.materialLaw = OwnButton(), OwnButton()
        self.density.bind(on_press=self.show_numpad)
        self.materialLaw.bind(on_press=self.show_material_law)
        self.btnBack, self.btnEdit = OwnButton(text=self.cancelStr), OwnButton(text=self.okStr)
        self.btnBack.bind(on_press=self.cancel_show)
        self.btnEdit.bind(on_press=self.edit_material)
    
    '''
    update the graph-size-properties
    '''
    
    def update_graph(self, minStress, maxStress, minStrain, maxStrain, points):
        self.p.points = points
        self.graph.xmin = minStrain
        self.graph.xmax = maxStrain
        self.graph.ymin = minStress
        self.graph.ymax = maxStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.

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
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.csShape = cs
        self.allMaterials = self.csShape.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
    
    
    '''
    edit the selected material. all components which use 
    this material will have the new properties
    '''
        
    def edit_material(self, btn):
        self.focusBtnMaterial.text = self.name.text
        self.focusMaterial.name = self.name.text
        self.focusMaterial.density = float(self.density.text)
        self.focusMaterial.price = float(self.price.text)
        self.focusMaterial.materialLaw = self.materialLawEditor.f
        self.cancel_show(None)
    
    '''
    set the labeltext with the materialproperties
    '''

    def show_material_information(self, btn):
        print('show_material_information (editor)')
        for i in range(0, len(self.allMaterials.allMaterials)):
            material = self.allMaterials.allMaterials[i]
            self.materialLawEditor.f = material.materialLaw
            if material.name == btn.text:
                self.focusBtnMaterial = btn
                self.focusMaterial = material
                self.name.text = material.name
                self.price.text = str(material.price)
                self.density.text = str(material.density)
                self.materialLaw.text = material.materialLaw.f_toString()
                self.update_graph(material.materialLaw.minStress, material.materialLaw.maxStress,
                            material.materialLaw.minStrain, material.materialLaw.maxStrain,
                            material.materialLaw.points)
                self.popupInfo.open()
                return
    
    '''
    open the numpad for the input-value
    '''
        
    def show_numpad(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = btn.text
        if btn == self.price:
            self.popupNumpad.title = self.priceStr
        else:
            self.popupNumpad.title = self.densityStr
        self.popupNumpad.open()
    
    '''
    show the keyboard for the name-input
    '''
        
    def show_keyboard(self, btn):
        self.focusBtn = btn
        self.keyboard.lblTextinput.text = btn.text
        self.popupKeyboard.open()

    '''
    show the material-law
    '''
        
    def show_material_law(self, btn):
        print('show_material_law (editor)')
        f = self.focusMaterial.materialLaw
        self.materialLawEditor.f = f
        self.popupLawEditor.open()
        if isinstance(f, Linear):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnLinear
            self.materialLawEditor.linearEditor.update_function(f.points, f.minStress, f.maxStress,
                                                                f.minStrain, f.maxStrain, f.a)
            self.materialLawEditor.confirm(None)
        elif isinstance(f, Multilinear):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnMultiLinear
            self.materialLawEditor.confirm(None)
        elif isinstance(f, QuadraticFunction):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnQuadratic
            self.materialLawEditor.confirm(None)
        elif isinstance(f, ExponentialFunction):
            self.materialLawEditor.focusBtn = self.materialLawEditor.btnExponentiell
            self.materialLawEditor.confirm(None)
        
    '''
    when the user confirm his name-input
    '''
            
    def finished_keyboard(self):
        self.name.text = self.keyboard.lblTextinput.text
        self.popupKeyboard.dismiss()
    
    '''
    when the user confirm his value-input
    '''
        
    def finished_numpad(self):
        self.focusBtn.text = self.numpad.lblTextinput.text
        self.popupNumpad.dismiss()
    
    '''
    when the user cancel the value-input
    '''
        
    def close_numpad(self):
        self.popupNumpad.dismiss()
    
    '''
    cancel the material-law-editor
    '''
        
    def close_material_law_editor(self, x):
        # for the material-law-editor
        self.popupLawEditor.dismiss()
        
    '''
    cancel the create-process. this method is necessary, because editor creator-instance call 
    the method cancel_edit_materialfrom the parent
    '''

    def cancel_edit_material(self):
        self.popupCreate.dismiss()
    
    '''
    close the popup, which shows the information from
    the choosen material
    '''

    def cancel_show(self, button):
        self.popupInfo.dismiss()

    '''
    open the popup, which has the creator as content
    '''

    def create_material(self, button):
        self.popupCreate.open()
    
