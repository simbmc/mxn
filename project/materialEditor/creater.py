'''
Created on 04.04.2016

@author: mkennert
'''
from kivy.properties import  ObjectProperty
from kivy.uix.gridlayout import GridLayout

from materialEditor.aeditor import AEditor
from materials.ownMaterial import OwnMaterial
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from plot.line import LinePlot


class MaterialCreater(GridLayout, AEditor):
    
    '''
    the material-creater is the component, where the user 
    can add new material
    '''
    
    # parent of the creater
    _parent = ObjectProperty()
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(MaterialCreater, self).__init__(**kwargs)
        print('create material-creater')
        self.cols, self.spacing = 2, Design.spacing
        self.create_gui()

    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''

    def create_gui(self):
        self.create_base_popups()
        self.create_buttons()
        self.create_information()
        self.information.add_widget(self.cancelBtn)
        self.information.add_widget(self.createBtn)
        self.graph = OwnGraph(xlabel=self.strainStr, ylabel=self.stressStr,
                              y_grid_label=True, x_grid_label=True)
        self.p = LinePlot(color=[0, 0, 0, 1])
        self.graph.add_plot(self.p)
        self.add_widget(self.information)
        self.add_widget(self.graph)
    
    '''
    the method create_buttons create all buttons of the class
    '''

    def create_buttons(self):
        self.create_base_btns()
        # create material and cancel
        self.createBtn = OwnButton(text=self.okStr)
        self.createBtn.bind(on_press=self.create_material)
        self.cancelBtn = OwnButton(text=self.cancelStr)
        self.cancelBtn.bind(on_press=self.cancel_create)
    
    '''
    the method create material create a own_material and update the 
    materiallist allMaterials and the layout where you can choose 
    the materials
    '''

    def create_material(self, button):
        # if the material has now material-law it will be not possible 
        # to create a material
        if self.materialLaw.text == self.defaultFStr:
            return
        curMaterial = OwnMaterial(self.nameBtn.text, self.priceBtn.text,
                                  self.densityBtn.text, self.materialLawEditor.f)
        self._parent.allMaterials.add_material(curMaterial)
        self._parent.cancel_edit_material()

    '''
    the method reset_editor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''

    def reset_editor(self):
        self.nameBtn.text = self.nameStr
        self.priceBtn.text = self.defaultValueStr
        self.densityBtn.text = self.defaultValueStr
        self.materialLaw.text = self.defaultFStr
        
    '''
    cancel the create-process
    '''
    def cancel_create(self, btn):
        self._parent.cancel_edit_material()

    '''
    open the popLawEditor
    '''
    def show_material_law_editor(self, btn):
        self.popupLawEditor.open()
