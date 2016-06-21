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
    
    def create_gui(self):
        self.create_popup()
        self.add_widget(Label(text='radius: '))
        self.btnRadius=Button(text=str(self.csShape.get_radius()), size_hint_y=None, height=self.btnSize)
        self.btnRadius.bind(on_press=self.show_numpad)
        self.add_widget(self.btnRadius)
    '''
    set the cross section
    '''
    def set_cross_section(self, cs):
        self.csShape=cs
        self.create_gui()
    
    '''
    create the popup
    '''
    def create_popup(self):
        self.numpad=Numpad()
        self.numpad.sign_in_parent(self)
        self.popup=Popup(content=self.numpad)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popup.dismiss()
        
    '''
    open the popup
    '''
    def show_numpad(self,btn):
        self.focusBtn=btn
        self.popup.open()
    
    '''
    set the text of the button
    '''
    def finished_numpad(self):
        self.btnRadius.text=self.numpad.textinput.text
        self.popup.dismiss()