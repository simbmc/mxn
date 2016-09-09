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


class QuadraticInformation(GridLayout, AInformation):
    
    '''
    with the QuadraticInformation you can set the properties of the function
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
        super(QuadraticInformation, self).__init__(**kwargs)
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
        v = float(self.numpad.lblTextinput.text)
        if self.focusBtn == self.aBtn:
            self.editor.a = v
            self.editor.view.update_points()
        elif self.focusBtn == self.bBtn:
            self.editor.b = v
        elif self.focusBtn == self.btnStrainUL:
            if v>self.editor.minStrain:
                self.editor.maxStrain = v
            else:
                return
        elif self.focusBtn == self.btnStrainLL:
            if v<self.editor.maxStrain:
                self.editor.minStrain = v
            else:
                return
        self.editor.view.update_graph_sizeproperties()
        self.focusBtn.text = str(v)
        self.popupNumpad.dismiss()
        self.numpad.reset_text()
    
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
        
    def update_function(self, points, minStrain, maxStrain, a, b):
        self.btnStrainLL.text = str(minStrain)
        self.btnStrainUL.text = str(maxStrain)
        self.aBtn.text = str(a)
        self.bBtn.text = str(b)