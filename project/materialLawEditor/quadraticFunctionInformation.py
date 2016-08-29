# -*- coding: utf-8 -*-
'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.properties import  ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class QuadraticFunctionInformation(GridLayout):
    
    '''
    with the QuadraticFunctionInformation you can set the properties of the function
    '''
    
    # important components
    editor = ObjectProperty()
    
    # strings
    functionStr, quadraticStr = StringProperty('function:'), StringProperty('quadratic')
    aStr, bStr = StringProperty('a:'), StringProperty('b:')
    strainULStr = StringProperty('strain-upper-limit :')
    strainLLStr, stressULStr = StringProperty('strain-lower-limit:'), StringProperty('stress-upper-limit [MPa]:')
    stressLLStr = StringProperty('stress-lower-limit [MPa]:')
    okStr, cancelStr = StringProperty('ok'), StringProperty('cancel')
    
    # constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.create_information()
    
    '''
    create the gui of the information, 
    where you can change the properties of the quadratic-function
    '''
    def create_information(self):
        self.create_btns()
        self.add_widget(OwnLabel(text=self.functionStr))
        self.add_widget(self.btnQuadratic)
        self.add_widget(OwnLabel(text=self.aStr))
        self.add_widget(self.aBtn)
        self.add_widget(OwnLabel(text=self.bStr))        
        self.add_widget(self.bBtn)
        self.add_widget(OwnLabel(text=self.strainULStr))
        self.add_widget(self.upperStrainBtn)
        self.add_widget(OwnLabel(text=self.stressULStr))
        self.add_widget(self.upperStressBtn)
        self.add_widget(OwnLabel(text=self.strainLLStr))
        self.add_widget(self.lowerStrain)
        self.add_widget(OwnLabel(text=self.stressLLStr))
        self.add_widget(self.lowerStress)
        self.add_widget(self.btn_confirm)
        self.add_widget(self.btn_cancel)
        # create the numpad
        self.numpad = Numpad(sign=True, p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
    # not finished yet
    def create_btns(self):
        self.aBtn = OwnButton(text=str(self.editor.a))
        self.aBtn.bind(on_press=self.show_popup)
        self.bBtn = OwnButton(text=str(self.editor.b))
        self.bBtn.bind(on_press=self.show_popup)
        self.lowerStress = OwnButton(text=str(self.editor.lowerStress))
        self.lowerStrain = OwnButton(text=str(self.editor.lowerStrain))
        self.upperStrainBtn = OwnButton(text=str(self.editor.upperStrain))
        self.upperStressBtn = OwnButton(text=str(self.editor.upperStress))
        self.btn_confirm = OwnButton(text=self.okStr)
        self.btn_cancel = OwnButton(text=self.cancelStr)
        self.btnQuadratic = OwnButton(text=self.quadraticStr)
        self.btnQuadratic.bind(on_press=self.show_type_selection)
        self.btn_confirm.bind(on_press=self.editor.confirm)
        self.btn_cancel.bind(on_press=self.editor.cancel)
        self.lowerStrain.bind(on_press=self.show_popup)
        self.lowerStress.bind(on_press=self.show_popup)
        self.upperStrainBtn.bind(on_press=self.show_popup)
        self.upperStressBtn.bind(on_press=self.show_popup)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()
        
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text = self.numpad.lblTextinput.text
        v = float(self.focusBtn.text)
        self.popupNumpad.dismiss()
        self.numpad.reset_text()
        if self.focusBtn == self.aBtn:
            self.editor.a = v
            self.editor.view.update_points()
        elif self.focusBtn == self.bBtn:
            self.editor.b = v
            self.editor.view.update_points()
        elif self.focusBtn == self.upperStrainBtn:
            self.editor.upperStrain = v
            self.editor.view.update_graph_sizeproperties()
        elif self.focusBtn == self.upperStressBtn:
            self.editor.upperStress = v
            self.editor.view.update_graph_sizeproperties()
        elif self.focusBtn == self.lowerStrain:
            self.editor.lowerStrain = v
            self.editor.view.update_graph_sizeproperties()
        elif self.focusBtn == self.lowerStress:
            self.editor.lowerStress = v
            self.editor.view.update_graph_sizeproperties()
    
    '''
    open the numpad popup
    '''
    def show_popup(self, btn):
        self.focusBtn = btn
        if self.focusBtn == self.aBtn:
            self.popupNumpad.title = self.aStr
        elif self.focusBtn == self.bBtn:
            self.popupNumpad.title = self.bStr
        elif self.focusBtn == self.upperStrainBtn:
            self.popupNumpad.title = self.strainULStr
        elif self.focusBtn == self.upperStressBtn:
            self.popupNumpad.title = self.stressULStr
        elif self.focusBtn == self.lowerStrain:
            self.popupNumpad.title = self.strainLLStr
        elif self.focusBtn == self.lowerStress:
            self.popupNumpad.title = self.stressLLStr
        self.popupNumpad.open()
    
    '''
    show the popup where the user can select the function-type
    '''
    def show_type_selection(self, btn):
        self.editor.lawEditor.editor.open()
