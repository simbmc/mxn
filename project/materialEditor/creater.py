'''
Created on 04.04.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from materialEditor.keyboard import Keyboard
from materialEditor.numpad import Numpad
from materials.ownMaterial import OwnMaterial
from designClass.design import Design


class MaterialCreater(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(MaterialCreater, self).__init__(**kwargs)
        self.cols=2
        self.btnSize=Design.btnSize
        self.createGui()
        self._parent=None
        self.focusBtn=None
    
    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''
    def createGui(self):
        self.createPopups()
        self.createButtons()
        self.add_widget(Label(text='name: '))
        self.add_widget(self.nameBtn)
        self.add_widget(Label(text='price[euro/kg]:'))
        self.add_widget(self.priceBtn)
        self.add_widget(Label(text='density[kg/m^3]:'))
        self.add_widget(self.densityBtn)
        self.add_widget(Label(text='stiffness[MPa]:'))
        self.add_widget(self.stiffnessBtn)
        self.add_widget(Label(text='strength[MPa]:'))
        self.add_widget(self.strengthBtn)
        self.add_widget(self.cancelBtn)
        self.add_widget(self.createBtn)
    
    '''
    the method createButtons create all buttons of the class
    '''
    def createButtons(self):
        #materialname
        self.nameBtn=Button(text='name',size_hint_y=None, height=self.btnSize)
        self.nameBtn.bind(on_press=self.useKeyboard)
        #materialprice
        self.priceBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.priceBtn.bind(on_press=self.useNumpad)
        #materialdensity
        self.densityBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.densityBtn.bind(on_press=self.useNumpad)
        #materialstiffness
        self.stiffnessBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.stiffnessBtn.bind(on_press=self.useNumpad)
        #materialstrength
        self.strengthBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.strengthBtn.bind(on_press=self.useNumpad)
        #create material and cancel 
        self.createBtn=Button(text='create',size_hint_y=None, height=self.btnSize)
        self.createBtn.bind(on_press=self.createMaterial)
        self.cancelBtn=Button(text='cancel',size_hint_y=None, height=self.btnSize)
        self.cancelBtn.bind(on_press=self.cancel)
        
    '''
    the method use_keyword open the keyboard_popup for the user
    '''
    def useKeyboard(self,button):
        self.keyboard.textinput.text=button.text
        self.popupKeyboard.open()
    
    '''
    the method useNumpad open the numpad_popup for the user
    '''
    def useNumpad(self,button):
        self.focusBtn=button
        self.numpad.textinput.text=button.text
        self.popupNumpad.open()
        
    '''
    the method createPopups create the popups 
    and sign in by the keyboard and numpad 
    '''
    def createPopups(self):
        self.numpad=Numpad()
        self.keyboard=Keyboard()
        self.popupKeyboard=Popup(title='name:',content=self.keyboard)
        self.popupNumpad=Popup(title='numpad', content=self.numpad)
        self.numpad.signInParent(self)
        self.keyboard.signInParent(self)
    
    
    '''
    the method finishedKeyboard close the keyboard_popup
    '''
    def finishedKeyboard(self):
        self.nameBtn.text=self.keyboard.textinput.text
        self.popupKeyboard.dismiss()
        self.keyboard.resetText()
    
    '''
    the method finishedNumpad close the numpad_popup
    '''
    def finishedNumpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popupNumpad.dismiss()
        self.numpad.resetText()
    
    def closeNumpad(self):
        self.popupNumpad.dismiss()
    '''
    the method signInParent to set the parent of 
    the object. the parent must have the method update_materials
    '''
    def signInParent(self, parent):
        self._parent=parent
    
    '''
    the method resetEditor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''
    def resetEditor(self):
        self.nameBtn.text='name'
        self.priceBtn.text='0.0'
        self.densityBtn.text='0.0'
        self.stiffnessBtn.text='0.0'
        self.strengthBtn.text='0.0'
    
    '''
    the method create material create a own_material and update the 
    materiallist allMaterials and the layout where you can choose 
    the materials
    '''
    def createMaterial(self,button):
        curMaterial=OwnMaterial(self.nameBtn.text,self.priceBtn.text,self.densityBtn.text,self.stiffnessBtn.text,self.strengthBtn.text)
        self._parent.allMaterials.addMaterial(curMaterial)
        self._parent.cancelEditMaterial()
    
    '''
    cancel the create-process
    '''
    def cancel(self,button):
        self._parent.cancelEditMaterial()