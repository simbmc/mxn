'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from designClass.design import Design
from materialEditor.numpad import Numpad


class LinearInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(LinearInformation, self).__init__(**kwargs)
        self.cols=2
        self.btnSize=Design.btnSize
        self.create_gui()
        
    '''
    create the gui
    '''
    def create_gui(self):
        self.create_popup()
        self.add_widget(Label(text='function:'))
        self.add_widget(Label(text='f(x)=mx+b'))
        self.add_widget(Label(text='m'))
        self.btnM=Button(text='1',size_hint_y=None, height=self.btnSize)
        self.btnM.bind(on_press=self.show_popup)
        self.add_widget(self.btnM)
    
    '''
    create the popup with the numpad as content
    '''
    def create_popup(self):
        self.numpad=Numpad()
        self.numpad.sign_in_parent(self)
        self.popupNumpad=Popup(title='Numpad', content=self.numpad)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popup.dismiss()
        
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
    
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popupNumpad.dismiss()
        if self.focusBtn==self.btnM:
            self.focusBtn=self.btnM
            self.btnM.text=self.numpad.textinput.text
        self.numpad.reset_text()
    