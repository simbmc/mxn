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
        self.createGUI()
        
    '''
    create the gui
    '''
    def createGUI(self):
        self.createPopup()
        self.add_widget(Label(text='function:'))
        self.add_widget(Label(text='f(x)=mx+b'))
        self.add_widget(Label(text='m'))
        self.btnM=Button(text='1',size_hint_y=None, height=self.btnSize)
        self.btnM.bind(on_press=self.showPopup)
        self.add_widget(self.btnM)
    
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
    
    '''
    the method finishedNumpad close the numpad_popup
    '''
    def finishedNumpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popupNumpad.dismiss()
        if self.focusBtn==self.btnM:
            self.focusBtn=self.btnM
            self.btnM.text=self.numpad.textinput.text
        self.numpad.resetText()
    