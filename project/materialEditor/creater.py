'''
Created on 04.04.2016

@author: mkennert
'''
from kivy.properties import  ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.lawEditor import MaterialLawEditor
from materials.ownMaterial import OwnMaterial
from ownComponents.design import Design
from ownComponents.keyboard import Keyboard
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot


class MaterialCreater(GridLayout):
    
    '''
    the material-creater is the component, where the user 
    can add new material
    '''
    
    # important components
    _parent = ObjectProperty()
    
    # strings
    strainStr, stressStr = StringProperty('strain '), StringProperty('stress [MPa]')
    nameStr, materialStr = StringProperty('name'), StringProperty('material')
    materialLawStr = StringProperty('material-law')
    createStr = StringProperty('create new material')
    priceStr, densityStr = StringProperty('price[euro/kg]'), StringProperty('density[kg/m^3]')
    defaultValueStr, defaultFStr = StringProperty('1.0'), StringProperty('-')
    okStr, cancelStr = StringProperty('ok'), StringProperty('cancel')
    
    # constructor
    def __init__(self, **kwargs):
        super(MaterialCreater, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.create_gui()

    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''

    def create_gui(self):
        self.create_popups()
        self.create_buttons()
        self.information = GridLayout(cols=2, spacing=Design.spacing)
        self.information.add_widget(OwnLabel(text=self.nameStr))
        self.information.add_widget(self.nameBtn)
        self.information.add_widget(OwnLabel(text=self.priceStr))
        self.information.add_widget(self.priceBtn)
        self.information.add_widget(OwnLabel(text=self.densityStr))
        self.information.add_widget(self.densityBtn)
        self.information.add_widget(OwnLabel(text=self.materialLawStr))
        self.information.add_widget(self.materialLaw)
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
        # materialname
        self.nameBtn = OwnButton(text=self.nameStr)
        self.nameBtn.bind(on_press=self.show_keyboard)
        # materialprice
        self.priceBtn = OwnButton(text=self.defaultValueStr)
        self.priceBtn.bind(on_press=self.show_numpad)
        # materialdensity
        self.densityBtn = OwnButton(text=self.defaultValueStr)
        self.densityBtn.bind(on_press=self.show_numpad)
        # material law
        self.materialLaw = OwnButton(text=self.defaultFStr)
        self.materialLaw.bind(on_press=self.show_material_law_editor)
        # create material and cancel
        self.createBtn = OwnButton(text=self.okStr)
        self.createBtn.bind(on_press=self.create_material)
        self.cancelBtn = OwnButton(text=self.cancelStr)
        self.cancelBtn.bind(on_press=self.cancel_create)
    
    '''
    the method create_popups create the popups 
    and sign in by the keyboard and numpad 
    '''

    def create_popups(self):
        self.materialLawEditor = MaterialLawEditor(creater=self)
        self.popupLawEditor = OwnPopup(title=self.materialLawStr, content=self.materialLawEditor)
        self.numpad = Numpad(p=self)
        self.keyboard = Keyboard(p=self)
        self.popupKeyboard = OwnPopup(title=self.nameStr, content=self.keyboard)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
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
    the method use_keyword open the keyboard_popup for the user
    '''
    def show_keyboard(self, button):
        self.keyboard.lblTextinput.text = button.text
        self.popupKeyboard.open()

    '''
    the method show_numpad open the numpad_popup for the user
    '''

    def show_numpad(self, button):
        self.focusBtn = button
        self.numpad.lblTextinput.text = button.text
        self.popupNumpad.open()

    '''
    the method finished_keyboard close the keyboard_popup
    '''

    def finished_keyboard(self):
        self.nameBtn.text = self.keyboard.lblTextinput.text
        self.popupKeyboard.dismiss()
        self.keyboard.reset_text()

    '''
    the method finished_numpad close the numpad_popup
    '''

    def finished_numpad(self):
        self.focusBtn.text = self.numpad.lblTextinput.text
        self.popupNumpad.dismiss()
        self.numpad.reset_text()
    
    '''
    close_numpad will be called from the numpad!
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()

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
        
    # not finished yet
    def cancel_create(self, btn):
        self._parent.cancel_edit_material()

    # not finished yet
    def show_material_law_editor(self, btn):
        self.popupLawEditor.open()
    
    # not finished yet
    def close_material_law_editor(self, btn):
        self.popupLawEditor.dismiss()
    
    '''
    update the graph by the given function-properties
    '''
    def update_graph(self, minStress, maxStress, minStrain, maxStrain, points):
        self.p.points = points
        self.graph.xmin = minStrain
        self.graph.xmax = maxStrain
        self.graph.ymin = minStress
        self.graph.ymax = maxStress
        self.graph.x_ticks_major = self.graph.xmax / 5.
        self.graph.y_ticks_major = self.graph.ymax / 5.
