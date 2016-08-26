'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class RectangleInformation(GridLayout):
    
    '''
    create the component, where you can change the height and 
    the width of the cross-section-rectangle
    '''
    
    # important components
    csShape = ObjectProperty()
    
    # strings
    heightStr, widthStr = StringProperty('height [m]'), StringProperty('width [m]')
    
    # constructor
    def __init__(self, **kwargs):
        super(RectangleInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.size_hint_y = None
    
    '''
    create the gui
    '''
    def create_gui(self):
        # create Numpad
        self.numpad = Numpad(p=self)
        self.popUp = OwnPopup(content=self.numpad)
        self.heightValue = OwnLabel(text=self.heightStr)
        self.btnHeight = OwnButton(text=str(self.csShape.ch))
        self.btnHeight.bind(on_press=self.show_numpad)
        self.add_widget(self.heightValue)
        self.add_widget(self.btnHeight)
        self.widthValue = OwnLabel(text=self.widthStr)
        self.btnWidth = OwnButton(text=str(self.csShape.cw))
        self.btnWidth.bind(on_press=self.show_numpad)
        self.add_widget(self.widthValue)
        self.add_widget(self.btnWidth)
    
    '''
    show the numpad
    '''
    def show_numpad(self, btn):
        self.focusbtn = btn
        if btn == self.btnHeight:
            self.popUp.title = self.heightStr
        else:
            self.popUp.title = self.widthStr
        self.popUp.open()
    
    '''
    close the numpad. this method will be call from the numpad
    '''
    def close_numpad(self):
        self.popUp.dismiss()
    
    '''
    set the values
    '''
    def finished_numpad(self):
        v = float(self.numpad.lblTextinput.text)
        self.focusbtn.text = str(v)
        if self.focusbtn == self.btnHeight:
            self.csShape.ch = v
            self.csShape.view.update_height(v)
        else:
            self.csShape.cw = v
            self.csShape.view.update_width(v)
        self.popUp.dismiss()
