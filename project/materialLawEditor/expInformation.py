'''
Created on 28.06.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup

class ExpInformation(GridLayout):
    # constructor
    def __init__(self, **kwargs):
        super(ExpInformation, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = Design.spacing
        self.btnSize = Design.btnHeight
        self.create_gui()
        self.row_force_default = True
        self.row_default_height = self.btnSize
        
    '''
    create the gui
    '''
    def create_gui(self):
        self.create_popup()
        self.add_widget(OwnLabel(text='function:'))
        self.add_widget(OwnLabel(text='f(x)=1-c*exp(-x)'))
        self.add_widget(OwnLabel(text='c'))
        self.btnA = OwnButton(text='1')
        self.btnA.bind(on_press=self.show_popup)
        self.add_widget(self.btnA)
    
    '''
    create the popup with the numpad as content
    '''
    def create_popup(self):
        self.numpad = Numpad()
        self.numpad.sign=True
        self.numpad.sign_in_parent(self)
        self.popupNumpad = OwnPopup(title='Numpad', content=self.numpad)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popup.dismiss()
        
    '''
    open the numpad popup
    '''
    def show_popup(self, btn):
        self.focusBtn = btn
        self.popupNumpad.open()
    
    '''
    sign in by the parent
    '''
    def sign_in(self, parent):
        self.editor = parent
    
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text = self.numpad.lblTextinput.text
        self.popupNumpad.dismiss()
        if self.focusBtn == self.btnA:
            self.focusBtn = self.btnA
            self.btnA.text = self.numpad.lblTextinput.text
            self.editor.update_graph(float(self.btnA.text))
        self.numpad.reset_text()
    
    '''
    update the slope
    '''
    def update_btn(self, value):
        self.btnA.text = str(value)
    
