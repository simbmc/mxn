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


class QuadraticFunctionInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionInformation, self).__init__(**kwargs)
        self.cols = 2
        self.focusBtn=None
        self.createInformation()
    
    '''
    create the gui
    '''
    def createInformation(self):
        self.add_widget(Label(text='function:'))
        self.add_widget(Label(text='f(x)=ax^2+bx+c'))
        self.add_widget(Label(text='a'))
        self.aBtn=Button(text='1:')
        self.aBtn.bind(on_press=self.showPopup)
        self.add_widget(self.aBtn)
        self.add_widget(Label(text='b'))        
        self.bBtn=Button(text='0')
        self.bBtn.bind(on_press=self.showPopup)
        self.add_widget(self.bBtn)
        self.add_widget(Label(text='c'))
        self.cBtn=Button(text='0')
        self.add_widget(self.cBtn)
        self.cBtn.bind(on_press=self.showPopup)
        self.h=Button(text='10')
        self.w=Button(text='10')
        self.h.bind(on_press=self.showPopup)
        self.w.bind(on_press=self.showPopup)
        self.add_widget(Label(text='height:'))
        self.add_widget(self.h)
        self.add_widget(Label(text='width'))
        self.add_widget(self.w)
        self.createPopup()
    
    
    '''
    create the popup with the numpad as content
    '''
    def createPopup(self):
        self.numpad=Numpad()
        self.numpad.signInParent(self)
        self.popupNumpad=Popup(title='Numpad', content=self.numpad)
    
    '''
    close the numpad
    '''
    def closeNumpad(self):
        self.popup.dismiss()
        
    '''
    the method finishedNumpad close the numpad_popup
    '''
    def finishedNumpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popupNumpad.dismiss()
        if self.focusBtn==self.aBtn:
            self.aBtn.text=self.numpad.textinput.text
            self.editor.setA(float(self.aBtn.text))
        elif self.focusBtn==self.bBtn:
            self.bBtn.text=self.numpad.textinput.text
            self.editor.setB(float(self.bBtn.text))
        elif self.focusBtn==self.cBtn:
            self.cBtn.text=self.numpad.textinput.text
            self.editor.setC(float(self.cBtn.text))
        elif self.focusBtn==self.h:
            self.editor.setHeight(float(self.h.text))
        elif self.focusBtn==self.w:
            self.editor.setWidth(float(self.w.text))
        self.numpad.resetText()
    
    '''
    open the numpad popup
    '''
    def showPopup(self,btn):
        self.focusBtn=btn
        self.popupNumpad.open()
    
    '''
    sign in by the parent
    '''
    def signIn(self, parent):
        self.editor=parent