'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class DoubleTInformation(GridLayout):
    '''
    create the component, where you can change the size-properties 
    of the cross-section-double-t
    '''
    csShape = ObjectProperty()
    # Constructor
    def __init__(self, **kwargs):
        super(DoubleTInformation, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = Design.spacing
        
    '''
    create the gui
    '''
    def create_gui(self):
        self.create_btns()
        self.add_widget(OwnLabel(text='top-width'))
        self.add_widget(self.topWidth)
        self.add_widget(OwnLabel(text='middle-width'))
        self.add_widget(self.middleWidth)
        self.add_widget(OwnLabel(text='bottom-width'))
        self.add_widget(self.bottomWidth)
        self.add_widget(OwnLabel(text='top-height'))
        self.add_widget(self.topHeight)
        self.add_widget(OwnLabel(text='middle-height'))
        self.add_widget(self.middleHeight)
        self.add_widget(OwnLabel(text='bottom-height'))
        self.add_widget(self.bottomHeight)
        self.create_popup()
        
    '''
    create all btns of this component
    '''
    def create_btns(self):
        self.topWidth = OwnButton(text=str(self.csShape.tw))
        self.middleWidth = OwnButton(text=str(self.csShape.mw))
        self.bottomWidth = OwnButton(text=str(self.csShape.bw))
        self.topHeight = OwnButton(text=str(self.csShape.th))
        self.middleHeight = OwnButton(text=str(self.csShape.mh))
        self.bottomHeight = OwnButton(text=str(self.csShape.bh))
        self.topWidth.bind(on_press=self.show_numpad)
        self.topHeight.bind(on_press=self.show_numpad)
        self.middleWidth.bind(on_press=self.show_numpad)
        self.middleHeight.bind(on_press=self.show_numpad)
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
        elif self.focusBtn == self.middleHeight:
            self.csShape.set_height_middle(value)
        elif self.focusBtn == self.middleWidth:
            self.csShape.set_width_middle(value)
        elif self.focusBtn == self.bottomHeight:
            self.csShape.set_height_bottom(value)
        elif self.focusBtn == self.bottomWidth:
            self.csShape.set_width_bottom(value)