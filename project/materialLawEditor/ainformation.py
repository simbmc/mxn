'''
Created on 01.09.2016

@author: mkennert
'''
from kivy.properties import  ObjectProperty, StringProperty

from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel


class AInformation:
    
    '''
    base class of the function-informations
    '''
    
    # editor
    editor = ObjectProperty()
    
    # string function
    functionStr = StringProperty('function:')
    
    # string strain-upper-limit
    strainULStr = StringProperty('strain-upper-limit:')
    
    # string strain-lower-limit
    strainLLStr = StringProperty('strain-lower-limit:')
    
    # string ok
    okStr = StringProperty('ok')
    
    # string cancel
    cancelStr = StringProperty('cancel')
    
    '''
    show the popup where the user can select the function-type
    '''
    
    def show_type_selection(self, btn):
        self.editor.lawEditor.editor.open()
    
    '''
    close the numpad when the user cancel the input
    '''
        
    def close_numpad(self):
        self.popupNumpad.dismiss()
    
    '''
    create all btns, which are in all information the same
    '''
        
    def create_base_btns(self):
        self.btnStrainUL = OwnButton(text=str(self.editor.maxStrain))
        self.btnStrainLL = OwnButton(text=str(self.editor.minStrain))
        self.btnConfirm = OwnButton(text=self.okStr)
        self.btnCancel = OwnButton(text=self.cancelStr)
        self.btnConfirm.bind(on_press=self.editor.confirm)
        self.btnStrainUL.bind(on_press=self.show_popup)
        self.btnStrainLL.bind(on_press=self.show_popup)
        self.btnCancel.bind(on_press=self.editor.cancel)
    
    '''
    add the base_btns to the root-widget
    '''
    def add_base_btns(self):
        self.add_widget(OwnLabel(text=self.strainULStr))
        self.add_widget(self.btnStrainUL)
        self.add_widget(OwnLabel(text=self.strainLLStr))
        self.add_widget(self.btnStrainLL)
        self.add_widget(self.btnConfirm)
        self.add_widget(self.btnCancel)
    
    '''
    set the popup-titel when the focusbtn is a base-btn
    '''
    def set_popup_title(self):
        if self.focusBtn == self.btnStrainUL:
            self.popupNumpad.title = self.strainULStr
        elif self.focusBtn == self.btnStrainLL:
            self.popupNumpad.title = self.strainLLStr