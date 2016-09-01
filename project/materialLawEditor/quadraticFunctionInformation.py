# -*- coding: utf-8 -*-
'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from materialLawEditor.ainformation import AInformation


class QuadraticFunctionInformation(GridLayout, AInformation):
    
    '''
    with the QuadraticFunctionInformation you can set the properties of the function
    '''
    
    # string quadratic
    quadraticStr = StringProperty('quadratic')
    
    # string parameter a
    aStr = StringProperty('a:')
    
    # string parameter b
    bStr = StringProperty('b:')
    
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(QuadraticFunctionInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.create_information()
        # create the numpad
        self.numpad = Numpad(sign=True, p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
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
        self.add_base_btns()
        
    '''
    create all btns of the gui
    '''
    def create_btns(self):
        self.aBtn = OwnButton(text=str(self.editor.a))
        self.aBtn.bind(on_press=self.show_popup)
        self.bBtn = OwnButton(text=str(self.editor.b))
        self.bBtn.bind(on_press=self.show_popup)
        self.btnQuadratic = OwnButton(text=self.quadraticStr)
        self.btnQuadratic.bind(on_press=self.show_type_selection)
        self.create_base_btns()

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
        elif self.focusBtn == self.btnStrainUL:
            self.editor.upperStrain = v
            self.editor.view.update_graph_sizeproperties()
        elif self.focusBtn == self.btnStressUL:
            self.editor.upperStress = v
            self.editor.view.update_graph_sizeproperties()
        elif self.focusBtn == self.btnStrainLL:
            self.editor.lowerStrain = v
            self.editor.view.update_graph_sizeproperties()
        elif self.focusBtn == self.btnStressLL:
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
        self.set_popup_title()
        self.popupNumpad.open()
    
    '''
    update the complete information by the given function-properties
    '''
    def update_function(self, points, minStress, maxStress, minStrain, maxStrain, a, b):
        self.btnStrainLL.text = str(minStrain)
        self.btnStrainUL.text = str(maxStrain)
        self.btnStressLL.text = str(minStress)
        self.btnStressUL.text = str(maxStress)
        self.aBtn.text = str(a)
        self.bBtn.text=str(b)