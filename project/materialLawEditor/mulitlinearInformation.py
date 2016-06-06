'''
Created on 06.05.2016

@author: mkennert
'''

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from designClass.design import Design
from materialEditor.numpad import Numpad


class MultilinearInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(MultilinearInformation, self).__init__(**kwargs)
        self.cols = 2
        self.btnSize=Design.btnSize
        self.focusBtn=None
        self.createInformation()
    
    '''
    create the gui of the information
    '''
    def createInformation(self):
        self.add_widget(Label(text='function:',size_hint_x=None, width=200))
        self.add_widget(Label(text='multilinear',size_hint_x=None, width=200))
        self.pointsLbl=Label(text='points:',size_hint_x=None, width=200)
        self.pointsBtn=Button(text='5',size_hint_y=None, height=self.btnSize)
        self.pointsBtn.bind(on_press=self.showPopup)
        self.heightLbl=Label(text='height:',size_hint_x=None, width=200)
        self.heightBtn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.heightBtn.bind(on_press=self.showPopup)
        self.widthLbl=Label(text='width:',size_hint_x=None, width=200)
        self.widthBtn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.widthBtn.bind(on_press=self.showPopup)
        self.add_widget(self.pointsLbl)
        self.add_widget(self.pointsBtn)
        self.add_widget(self.heightLbl)
        self.add_widget(self.heightBtn)
        self.add_widget(self.widthLbl)
        self.add_widget(self.widthBtn)
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
        self.popupNumpad.dismiss()
        if self.focusBtn==self.pointsBtn:
            self.pointsBtn.text=self.numpad.textinput.text
            print(self.pointsBtn.text)
            self.editor.setPoints(float(self.pointsBtn.text))
        elif self.focusBtn==self.widthBtn:
            self.widthBtn.text=self.numpad.textinput.text
            self.editor.setWidth(float(self.widthBtn.text))
        elif self.focusBtn==self.heightBtn:
            self.heightBtn.text=self.numpad.textinput.text
            self.editor.setHeight(float(self.heightBtn.text))
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
    
    