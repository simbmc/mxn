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
        self.row_force_default=True
        self.row_default_height=self.btnSize
        self.create_information()
    
    '''
    create the gui of the information
    '''
    def create_information(self):
        self.add_widget(Label(text='function:',size_hint_x=None, width=200))
        self.add_widget(Label(text='multilinear',size_hint_x=None, width=200))
        self.pointsBtn=Button(text='5',size_hint_y=None, height=self.btnSize)
        self.pointsBtn.bind(on_press=self.show_popup)
        self.heightBtn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.heightBtn.bind(on_press=self.show_popup)
        self.widthBtn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.widthBtn.bind(on_press=self.show_popup)
        self.add_widget(Label(text='points:',size_hint_x=None, width=200))
        self.add_widget(self.pointsBtn)
        self.add_widget(Label(text='strain-limit:',size_hint_x=None, width=200))
        self.add_widget(self.heightBtn)
        self.add_widget(Label(text='stress-limit:',size_hint_x=None, width=200))
        self.add_widget(self.widthBtn)
        self.add_widget(Label(text='x-coordinate: '))
        self.btnX=Button(text='-')
        self.btnX.bind(on_press=self.show_popup)
        self.add_widget(self.btnX)
        self.btnY=Button(text='-')
        self.btnY.bind(on_press=self.show_popup)
        self.add_widget(Label(text='y-coordinate: '))
        self.add_widget(self.btnY)
        btn_confirm=Button(text='ok',size_hint_y=None, height=self.btnSize)
        btn_cancel=Button(text='cancel',size_hint_y=None, height=self.btnSize)
        btn_confirm.bind(on_press=self.confirm)
        btn_cancel.bind(on_press=self.cancel)
        self.add_widget(btn_confirm)
        self.add_widget(btn_cancel)
        self.create_popup()
        
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
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.popupNumpad.dismiss()
        if self.focusBtn==self.pointsBtn:
            self.pointsBtn.text=self.numpad.textinput.text
            self.editor.set_points(float(self.pointsBtn.text))
        elif self.focusBtn==self.widthBtn:
            self.widthBtn.text=self.numpad.textinput.text
            self.editor.set_width(float(self.widthBtn.text))
        elif self.focusBtn==self.heightBtn:
            self.heightBtn.text=self.numpad.textinput.text
            self.editor.set_height(float(self.heightBtn.text))
        elif self.focusBtn==self.btnX:
            self.btnX.text=self.numpad.textinput.text
            self.editor.update_point_position_x(float(self.btnX.text))
        elif self.focusBtn==self.btnY:
            if self.editor.update_point_position_y(float(self.numpad.textinput.text)):
                self.btnY.text=self.numpad.textinput.text
        self.numpad.reset_text()
    
    #not finished yet
    def update_coordinates(self,x,y):
        self.btnX.text=str(x)
        self.btnY.text=str(y)
    
    
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
        
    