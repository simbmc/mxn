'''
Created on 06.05.2016

@author: mkennert
'''

from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class MultilinearInformation(GridLayout):
    # constructor
    def __init__(self, **kwargs):
        super(MultilinearInformation, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = Design.spacing
        self.btnSize = Design.btnHeight
        self.focusBtn = None
        self.row_force_default = True
        self.row_default_height = self.btnSize
        self.create_information()
    
    '''
    create the gui of the information
    '''
    def create_information(self):
        self.create_btns()
        self.add_widget(OwnLabel(text='function:'))
        self.add_widget(OwnLabel(text='multilinear'))
        self.add_widget(OwnLabel(text='points:'))
        self.add_widget(self.pointsBtn)
        self.add_widget(OwnLabel(text='strain-upper-limit:'))
        self.add_widget(self.heightBtn)
        self.add_widget(OwnLabel(text='stress-upper-limit:'))
        self.add_widget(self.widthBtn)
        self.add_widget(OwnLabel(text='strain-lower-limit:'))
        self.add_widget(self.strainlowerLimit)
        self.add_widget(OwnLabel(text='stress-lower-limit:'))
        self.add_widget(self.stresslowerLimit)
        self.add_widget(OwnLabel(text='x-coordinate: '))
        self.add_widget(self.btnX)
        self.add_widget(OwnLabel(text='y-coordinate: '))
        self.add_widget(self.btnY)
        btn_confirm = OwnButton(text='ok')
        btn_cancel = OwnButton(text='cancel')
        btn_confirm.bind(on_press=self.confirm)
        btn_cancel.bind(on_press=self.cancel)
        self.add_widget(btn_confirm)
        self.add_widget(btn_cancel)
        self.create_popup()
    
    '''
    create the btns
    '''
    def create_btns(self):
        self.pointsBtn = OwnButton(text='5')
        self.heightBtn = OwnButton(text='50')
        self.widthBtn = OwnButton(text='50')
        self.stresslowerLimit = OwnButton(text='0')
        self.strainlowerLimit = OwnButton(text='0')
        self.btnX = OwnButton(text='-')
        self.btnY = OwnButton(text='-')
        self.pointsBtn.bind(on_press=self.show_popup)
        self.heightBtn.bind(on_press=self.show_popup)
        self.widthBtn.bind(on_press=self.show_popup)
        self.strainlowerLimit.bind(on_press=self.show_popup)
        self.stresslowerLimit.bind(on_press=self.show_popup)
        self.btnX.bind(on_press=self.show_popup)
        self.btnY.bind(on_press=self.show_popup)
        
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
        self.popupNumpad.dismiss()
        
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.popupNumpad.dismiss()
        if self.focusBtn == self.pointsBtn:
            self.pointsBtn.text = self.numpad.lblTextinput.text
            self.editor.set_points(float(self.pointsBtn.text))
        elif self.focusBtn == self.widthBtn:
            self.widthBtn.text = self.numpad.lblTextinput.text
            self.editor.update_width(float(self.widthBtn.text))
        elif self.focusBtn == self.heightBtn:
            self.heightBtn.text = self.numpad.lblTextinput.text
            self.editor.update_height(float(self.heightBtn.text))
        elif self.focusBtn == self.btnX:
            self.btnX.text = self.numpad.lblTextinput.text
            self.editor.update_point_position_x(float(self.btnX.text))
        elif self.focusBtn == self.btnY:
            if self.editor.update_point_position_y(float(self.numpad.lblTextinput.text)):
                self.btnY.text = self.numpad.lblTextinput.text
        elif self.focusBtn == self.strainlowerLimit:
            self.strainlowerLimit.text = self.numpad.lblTextinput.text
            self.editor.update_lower_strain(float(self.strainlowerLimit.text))
        elif self.focusBtn == self.stresslowerLimit:
            self.stresslowerLimit.text = self.numpad.lblTextinput.text
            self.editor.update_lower_stress(float(self.stresslowerLimit.text))
        self.numpad.reset_text()
    
    # not finished yet
    def update_coordinates(self, x, y):
        self.btnX.text = str(x)
        self.btnY.text = str(y)
    
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
    
    
    def confirm(self, btn):
        self.editor.confirm()
    
    def cancel(self, btn):
        self.editor.cancel()
        
    
