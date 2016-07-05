# -*- coding: utf-8 -*-
'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from materialEditor.numpad import Numpad
from designClass.design import Design


class QuadraticFunctionInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionInformation, self).__init__(**kwargs)
        self.cols = 2
        self.btnSize=Design.btnSize
        self.focusBtn=None
        self.create_information()
    
    '''
    create the gui
    '''
    def create_information(self):
        self.add_widget(Label(text='function:'))
        self.add_widget(Label(text='f(x)=ax^2+bx+c'))
        self.add_widget(Label(text='a'))
        self.aBtn=Button(text='1:',size_hint_y=None, height=self.btnSize)
        self.aBtn.bind(on_press=self.show_popup)
        self.add_widget(self.aBtn)
        self.add_widget(Label(text='b',))        
        self.bBtn=Button(text='0',size_hint_y=None, height=self.btnSize)
        self.bBtn.bind(on_press=self.show_popup)
        self.add_widget(self.bBtn)
        self.add_widget(Label(text='c'))
        self.cBtn=Button(text='0',size_hint_y=None, height=self.btnSize)
        self.add_widget(self.cBtn)
        self.cBtn.bind(on_press=self.show_popup)
        self.h=Button(text='10',size_hint_y=None, height=self.btnSize)
        self.w=Button(text='10',size_hint_y=None, height=self.btnSize)
        self.h.bind(on_press=self.show_popup)
        self.w.bind(on_press=self.show_popup)
        self.add_widget(Label(text='strain-limit:'))
        self.add_widget(self.h)
        self.add_widget(Label(text='stress-limit'))
        self.add_widget(self.w)
        self.create_popup()
    
    
    '''
    create the popup with the numpad as content
    '''
    def create_popup(self):
        self.numpad=Numpad()
        self.numpad.sign_in_parent(self)
        self.popupNumpad=Popup(title='numpad', content=self.numpad)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()
        
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popupNumpad.dismiss()
        if self.focusBtn==self.aBtn:
            self.aBtn.text=self.numpad.textinput.text
            self.editor.set_a(float(self.aBtn.text))
        elif self.focusBtn==self.bBtn:
            self.bBtn.text=self.numpad.textinput.text
            self.editor.set_b(float(self.bBtn.text))
        elif self.focusBtn==self.cBtn:
            self.cBtn.text=self.numpad.textinput.text
            self.editor.set_c(float(self.cBtn.text))
        elif self.focusBtn==self.h:
            self.editor.set_height(float(self.h.text))
        elif self.focusBtn==self.w:
            self.editor.set_width(float(self.w.text))
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