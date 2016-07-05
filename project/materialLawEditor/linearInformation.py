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
        self.row_force_default=True
        self.row_default_height=self.btnSize
        
    '''
    create the gui
    '''
    def create_gui(self):
        self.create_popup()
        self.add_widget(Label(text='function:'))
        self.add_widget(Label(text='f(x)=mx+b'))
        self.add_widget(Label(text='m'))
        self.btnM=Button(text='1',size_hint_y=None, height=self.btnSize)
        self.add_widget(self.btnM)
        self.add_widget(Label(text='b'))
        self.btnB=Button(text='0',size_hint_y=None, height=self.btnSize)
        self.add_widget(self.btnB)
        self.add_widget(Label(text='strain-limit:'))
        #heigth represents strain
        self.btnHeight=Button(text='10',size_hint_y=None, height=self.btnSize)
        self.add_widget(self.btnHeight)
        self.add_widget(Label(text='stress-limit:'))
        #width represents stress
        self.btnWidth=Button(text='10',size_hint_y=None, height=self.btnSize)
        self.add_widget(self.btnWidth)
        self.btnM.bind(on_press=self.show_popup)
        self.btnB.bind(on_press=self.show_popup)
        self.btnHeight.bind(on_press=self.show_popup)
        self.btnWidth.bind(on_press=self.show_popup)
    
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
        self.popupNumpad.dismiss()
        
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
            self.btnM.text=self.numpad.textinput.text
            self.editor.update_graph(float(self.btnM.text))
        elif self.focusBtn==self.btnB:
            self.btnB.text=self.numpad.textinput.text
            self.editor.update_b(float(self.btnB.text))
        elif self.focusBtn==self.btnHeight:
            self.btnHeight.text=self.numpad.textinput.text
            self.editor.update_strain_limit(float(self.btnHeight.text))
        elif self.focusBtn==self.btnWidth:
            self.btnWidth.text=self.numpad.textinput.text
            self.editor.update_stress_limit(float(self.btnWidth.text))
        self.numpad.reset_text()
    
    '''
    update the slope
    '''
    def update_btn(self,value):
        self.btnM.text=str(value)
    