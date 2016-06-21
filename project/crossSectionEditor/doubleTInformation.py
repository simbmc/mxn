'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from designClass.design import Design
from materialEditor.numpad import Numpad


class DoubleTInformation(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(DoubleTInformation, self).__init__(**kwargs)
        self.focusBtn=None
        self.cols=2
        self.size_hint_y=None
        self.spacing=10
        self.btnSize=Design.btnSize
    '''
    create the gui
    '''
    def create_gui(self):
        self.topWidth=Button(text=str(self.csShape.get_width_top()),size_hint_y=None, height=self.btnSize)
        self.middleWidth=Button(text=str(self.csShape.get_width_middle()),size_hint_y=None, height=self.btnSize)
        self.bottomWidth=Button(text=str(self.csShape.get_width_bottom()),size_hint_y=None, height=self.btnSize)
        self.topHeight=Button(text=str(self.csShape.get_height_top()),size_hint_y=None, height=self.btnSize)
        self.middleHeight=Button(text=str(self.csShape.get_height_middle()),size_hint_y=None, height=self.btnSize)
        self.bottomHeight=Button(text=str(self.csShape.get_height_bottom()),size_hint_y=None, height=self.btnSize)
        self.topWidth.bind(on_press=self.show_numpad)
        self.topHeight.bind(on_press=self.show_numpad)
        self.middleWidth.bind(on_press=self.show_numpad)
        self.middleHeight.bind(on_press=self.show_numpad)
        self.bottomWidth.bind(on_press=self.show_numpad)
        self.bottomHeight.bind(on_press=self.show_numpad)
        self.add_widget(Label(text='top-width'))
        self.add_widget(self.topWidth)
        self.add_widget(Label(text='middle-width'))
        self.add_widget(self.middleWidth)
        self.add_widget(Label(text='bottom-width'))
        self.add_widget(self.bottomWidth)
        self.add_widget(Label(text='top-height'))
        self.add_widget(self.topHeight)
        self.add_widget(Label(text='middle-height'))
        self.add_widget(self.middleHeight)
        self.add_widget(Label(text='bottom-height'))
        self.add_widget(self.bottomHeight)
        self.create_popup()
    
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
        self.focusBtn.text=self.numpad.textinput.text
        self.popup.dismiss()
        value=float(self.focusBtn.text)
        if self.focusBtn==self.topHeight:
            self.csShape.set_height_top(value)
        elif self.focusBtn==self.topWidth:
            self.csShape.set_width_top(value)
        elif self.focusBtn==self.middleHeight:
            self.csShape.set_height_middle(value)
        elif self.focusBtn==self.middleWidth:
            self.csShape.set_width_middle(value)
        elif self.focusBtn==self.bottomHeight:
            self.csShape.set_height_bottom(value)
        elif self.focusBtn==self.bottomWidth:
            self.csShape.set_width_bottom(value)