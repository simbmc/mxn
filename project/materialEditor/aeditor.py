'''
Created on 01.09.2016

@author: mkennert
'''
from kivy.properties import  StringProperty
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.lawEditor import MaterialLawEditor
from ownComponents.design import Design
from ownComponents.keyboard import Keyboard
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class AEditor:
    
    '''
    base class of the materialEditor and the materialCreater
    '''
    
    strainStr = StringProperty('strain ')
    
    stressStr = StringProperty('stress [MPa]')
    
    nameStr = StringProperty('name')
    
    materialStr = StringProperty('material')
    
    materialLawStr = StringProperty('material-law')
    
    createStr = StringProperty('create new material')
    
    priceStr = StringProperty('price[euro/kg]')
    
    densityStr = StringProperty('density[kg/m^3]')
    
    okStr = StringProperty('ok')
    
    cancelStr = StringProperty('cancel')
    
    defaultValueStr = StringProperty('1.0')
    
    defaultFStr = StringProperty('-')
    
    '''
    create the base btns
    '''
    def create_base_btns(self):
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
    
    '''
    create the information where you can input the name, price, density and the material law
    '''
    def create_information(self):
        self.information = GridLayout(cols=2, spacing=Design.spacing)
        self.information.add_widget(OwnLabel(text=self.nameStr))
        self.information.add_widget(self.nameBtn)
        self.information.add_widget(OwnLabel(text=self.priceStr))
        self.information.add_widget(self.priceBtn)
        self.information.add_widget(OwnLabel(text=self.densityStr))
        self.information.add_widget(self.densityBtn)
        self.information.add_widget(OwnLabel(text=self.materialLawStr))
        self.information.add_widget(self.materialLaw)
    
    '''
    create the base popups
    '''
    def create_base_popups(self):
        self.materialLawEditor = MaterialLawEditor(creater=self)
        self.popupLawEditor = OwnPopup(title=self.materialLawStr, content=self.materialLawEditor)
        self.numpad = Numpad(p=self)
        self.keyboard = Keyboard(p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
        self.popupKeyboard = OwnPopup(title=self.nameStr, content=self.keyboard)
        
    '''
    show the keyboard for the name-input
    '''
        
    def show_keyboard(self, btn):
        self.focusBtn = btn
        self.keyboard.lblTextinput.text = btn.text
        self.popupKeyboard.open()
    
    '''
    open the numpad for the input-value
    '''
        
    def show_numpad(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = btn.text
        if btn == self.priceBtn:
            self.popupNumpad.title = self.priceStr
        else:
            self.popupNumpad.title = self.densityStr
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
    cancel the material-law-editor
    '''
        
    def close_material_law_editor(self, btn):
        self.popupLawEditor.dismiss()
        
    '''
    update the graph by the given function-properties
    '''
    def update_graph(self, minStress, maxStress, minStrain, maxStrain, points):
        print('update graph (materialEditor.AEditor)')
        self.p.points = points
        self.graph.xmin = minStrain
        self.graph.xmax = maxStrain
        self.graph.ymin = minStress
        self.graph.ymax = maxStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
