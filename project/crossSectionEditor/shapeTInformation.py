'''
Created on 03.06.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from ownComponents.numpad import Numpad
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from kivy.properties import ObjectProperty

class TInformation(GridLayout):
    '''
    create the component, where you can change the size properties
    of the cross-section-t-shape
    '''
    csShape = ObjectProperty()
    # constructor
    def __init__(self, **kwargs):
        super(TInformation, self).__init__(**kwargs)
        self.cols = 2
        self.size_hint_y = None
        self.spacing = Design.spacing
        self.btnSize = Design.btnHeight
        
    '''
    create the gui
    '''
    def create_gui(self):
        self.create_all_btns()
        self.add_widget(OwnLabel(text='top-width'))
        self.add_widget(self.topWidth)
        self.add_widget(OwnLabel(text='bottom-width'))
        self.add_widget(self.bottomWidth)
        self.add_widget(OwnLabel(text='top-height'))
        self.add_widget(self.topHeight)
        self.add_widget(OwnLabel(text='bottom-height'))
        self.add_widget(self.bottomHeight)
        self.create_popup()
        
    '''
    create all buttons of this component
    '''
    def create_all_btns(self):
        self.topWidth = OwnButton(text=str(self.csShape.get_width_top()))
        self.bottomWidth = OwnButton(text=str(self.csShape.get_width_bottom()))
        self.topHeight = OwnButton(text=str(self.csShape.get_height_top()))
        self.bottomHeight = OwnButton(text=str(self.csShape.get_height_bottom()))
        self.topWidth.bind(on_press=self.show_numpad)
        self.topHeight.bind(on_press=self.show_numpad)
        self.bottomWidth.bind(on_press=self.show_numpad)
        self.bottomHeight.bind(on_press=self.show_numpad)
        
    '''
    create the popup
    '''
    def create_popup(self):
        self.numpad = Numpad()
        self.numpad.sign_in_parent(self)
        self.popup = OwnPopup(content=self.numpad)
    
    '''
    set the text of the button
    '''
    def finished_numpad(self):
        self.focusBtn.text = self.numpad.lblTextinput.text
        self.popup.dismiss()
        value = float(self.focusBtn.text)
        if self.focusBtn == self.topHeight:
            self.csShape.set_height_top(value)
        elif self.focusBtn == self.topWidth:
            self.csShape.set_width_top(value)
        elif self.focusBtn == self.bottomHeight:
            self.csShape.set_height_bottom(value)
        elif self.focusBtn == self.bottomWidth:
            self.csShape.set_width_bottom(value)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popup.dismiss()
        
    '''
    open the popup
    '''
    def show_numpad(self, btn):
        self.focusBtn = btn
        self.popup.open()
