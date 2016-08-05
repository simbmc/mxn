# -*- coding: utf-8 -*-
'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class QuadraticFunctionInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionInformation, self).__init__(**kwargs)
        self.cols = 2
        self.spacing=Design.spacing
        self.btnSize=Design.btnHeight
        self.focusBtn=None
        self.create_information()
    
    '''
    create the gui
    '''
    def create_information(self):
        self.create_btns()
        self.add_widget(OwnLabel(text='function:'))
        self.add_widget(OwnLabel(text='f(x)=ax^2+bx+c'))
        self.add_widget(OwnLabel(text='a'))
        self.add_widget(self.aBtn)
        self.add_widget(OwnLabel(text='b',))        
        self.add_widget(self.bBtn)
        self.add_widget(OwnLabel(text='strain-upper-limit:'))
        self.add_widget(self.h)
        self.add_widget(OwnLabel(text='stress-upper-limit'))
        self.add_widget(self.w)
        btn_confirm=OwnButton(text='ok')
        btn_cancel=OwnButton(text='cancel')
        btn_confirm.bind(on_press=self.confirm)
        btn_cancel.bind(on_press=self.cancel)
        self.add_widget(btn_confirm)
        self.add_widget(btn_cancel)
        self.create_popup()
    
    #not finished yet
    def create_btns(self):
        self.bBtn=OwnButton(text='0')
        self.bBtn.bind(on_press=self.show_popup)
        self.lowerStress=OwnButton(text='0')
        self.lowerStrain=OwnButton(text='0')
        self.h=OwnButton(text='10')
        self.w=OwnButton(text='10')
        self.lowerStrain.bind(on_press=self.show_popup)
        self.lowerStress.bind(on_press=self.show_popup)
        self.h.bind(on_press=self.show_popup)
        self.w.bind(on_press=self.show_popup)
        self.aBtn=OwnButton(text='1:')
        self.aBtn.bind(on_press=self.show_popup)
    
    '''
    create the popup with the numpad as content
    '''
    def create_popup(self):
        self.numpad=Numpad()
        self.numpad.sign=True
        self.numpad.sign_in_parent(self)
        self.popupNumpad=OwnPopup(title='numpad', content=self.numpad)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()
        
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text=self.numpad.lblTextinput.text
        self.popupNumpad.dismiss()
        if self.focusBtn==self.aBtn:
            self.aBtn.text=self.numpad.lblTextinput.text
            self.editor.set_a(float(self.aBtn.text))
        elif self.focusBtn==self.bBtn:
            self.bBtn.text=self.numpad.lblTextinput.text
            self.editor.set_b(float(self.bBtn.text))
        elif self.focusBtn==self.h:
            self.editor.update_height(float(self.h.text))
        elif self.focusBtn==self.w:
            self.editor.update_width(float(self.w.text))
        elif self.focusBtn==self.lowerStrain:
            self.editor.update_lower_strain(float(self.lowerStrain.text))
        elif self.focusBtn==self.lowerStress:
            self.editor.update_lower_strain(float(self.lowerStress.text))
        self.numpad.reset_text()
    
    '''
    open the numpad popup
    '''
    def show_popup(self,btn):
        self.focusBtn=btn
        self.popupNumpad.open()
    
    '''
    sign in by the parent
    '''
    def sign_in(self, parent):
        self.editor=parent
    
    def confirm(self,btn):
        self.editor.confirm()
    
    def cancel(self,btn):
        self.editor.cancel()