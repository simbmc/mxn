'''
Created on 04.04.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.lawEditor import MaterialLawEditor
from materials.ownMaterial import OwnMaterial
from ownComponents.design import Design
from ownComponents.keyboard import Keyboard
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from kivy.properties import ObjectProperty

class MaterialCreater(GridLayout):
    _parent=ObjectProperty()
    # Constructor

    def __init__(self, **kwargs):
        super(MaterialCreater, self).__init__(**kwargs)
        self.cols,self.spacing = 2,Design.spacing
        self.create_gui()
        self.row_force_default = True
        self.row_default_height = Design.btnHeight

    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''

    def create_gui(self):
        self.create_popups()
        self.create_buttons()
        self.add_widget(OwnLabel(text='name: '))
        self.add_widget(self.nameBtn)
        self.add_widget(OwnLabel(text='price[euro/kg]:'))
        self.add_widget(self.priceBtn)
        self.add_widget(OwnLabel(text='density[kg/m^3]:'))
        self.add_widget(self.densityBtn)
        self.add_widget(OwnLabel(text='material-law'))
        self.add_widget(self.materialLaw)
        self.add_widget(self.cancelBtn)
        self.add_widget(self.createBtn)

    '''
    the method create_buttons create all buttons of the class
    '''

    def create_buttons(self):
        # materialname
        self.nameBtn = OwnButton(text='name')
        self.nameBtn.bind(on_press=self.show_keyboard)
        # materialprice
        self.priceBtn = OwnButton(text='1.0')
        self.priceBtn.bind(on_press=self.show_numpad)
        # materialdensity
        self.densityBtn = OwnButton(text='1.0')
        self.densityBtn.bind(on_press=self.show_numpad)
        # material law
        self.materialLaw = OwnButton(text='-')
        self.materialLaw.bind(on_press=self.show_material_law_editor)
        # create material and cancel
        self.createBtn = OwnButton(text='ok')
        self.createBtn.bind(on_press=self.create_material)
        self.cancelBtn = OwnButton(text='cancel')
        self.cancelBtn.bind(on_press=self.cancel_create)

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
    the method create_popups create the popups 
    and sign in by the keyboard and numpad 
    '''

    def create_popups(self):
        self.materialLawEditor = MaterialLawEditor()
        self.materialLawEditor.sign_in(self)
        self.popupLawEditor = OwnPopup(title='material law', 
                                       content=self.materialLawEditor)
        self.numpad = Numpad()
        self.keyboard = Keyboard()
        self.popupKeyboard = OwnPopup(title='name:', content=self.keyboard)
        self.popupNumpad = OwnPopup(title='numpad', content=self.numpad)
        self.numpad.sign_in_parent(self)
        self.keyboard.sign_in_parent(self)

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

    def close_numpad(self):
        self.popupNumpad.dismiss()
    
#     '''
#     the method sign_in_parent to set the parent of 
#     the object. the parent must have the method update_materials
#     '''
# 
#     def sign_in_parent(self, parent):
#         self._parent = parent

    '''
    the method reset_editor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''

    def reset_editor(self):
        self.nameBtn.text = 'name'
        self.priceBtn.text = '0.0'
        self.densityBtn.text = '0.0'

    '''
    the method create material create a own_material and update the 
    materiallist allMaterials and the layout where you can choose 
    the materials
    '''

    def create_material(self, button):
        curMaterial = OwnMaterial(
            self.nameBtn.text, self.priceBtn.text, self.densityBtn.text,self.materialLawEditor.f)
        self._parent.allMaterials.add_material(curMaterial)
        self._parent.cancel_edit_material()
        
    '''
    cancel the create-law-process
    '''

    def cancel(self, button):
        self.popupLawEditor.dismiss()
        
    # not finished yet

    def cancel_create(self, btn):
        self._parent.cancel_edit_material()

    # not finished yet
    def show_material_law_editor(self, btn):
        self.popupLawEditor.open()
    
    #not finished yet
    def close_material_law_editor(self, btn):
        self.popupLawEditor.dismiss()
