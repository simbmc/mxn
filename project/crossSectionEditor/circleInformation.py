'''
Created on 13.06.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from designClass.design import Design
from materialEditor.numpad import Numpad


class CircleInformation(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(CircleInformation, self).__init__(**kwargs)
        self.cols=2
        self.size_hint_y=None
        self.spacing=10
        self.btnSize=Design.btnSize
    
    def createGui(self):
        self.createPopup()
        self.add_widget(Label(text='radius: '))
        self.btnRadius=Button(text=str(self.csShape.getRadius()), size_hint_y=None, height=self.btnSize)
        self.btnRadius.bind(on_press=self.showNumpad)
        self.add_widget(self.btnRadius)
    '''
    set the cross section
    '''
    def set_crossSection(self, cs):
        self.csShape=cs
        self.createGui()
    
    '''
    create the popup
    '''
    def createPopup(self):
        self.numpad=Numpad()
        self.numpad.signInParent(self)
        self.popup=Popup(content=self.numpad)
    
    '''
    close the numpad
    '''
    def closeNumpad(self):
        self.popup.dismiss()
        
    '''
    open the popup
    '''
    def showNumpad(self,btn):
        self.focusBtn=btn
        self.popup.open()
    
    '''
    set the text of the button
    '''
    def finishedNumpad(self):
        self.btnRadius.text=self.numpad.textinput.text
        self.popup.dismiss()