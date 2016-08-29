'''
Created on 03.06.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class TInformation(GridLayout):
    
    '''
    create the component, where you can change the size properties
    of the cross-section-t-shape
    '''
    
    # important components
    csShape = ObjectProperty()
    
    # strings
    twStr, thStr = StringProperty('top-width [m]'), StringProperty('top-height [m]')
    bwStr, bhStr = StringProperty('bottom-width [m]'), StringProperty('bottom-height [m]')
    
    # constructor
    def __init__(self, **kwargs):
        super(TInformation, self).__init__(**kwargs)
        self.cols, self.size_hint_y = 2, None
        self.spacing = Design.spacing
        
    '''
    create the gui
    '''
        
    def create_gui(self):
        self.create_all_btns()
        self.add_widget(OwnLabel(text=self.twStr))
        self.add_widget(self.topWidth)
        self.add_widget(OwnLabel(text=self.bwStr))
        self.add_widget(self.bottomWidth)
        self.add_widget(OwnLabel(text=self.thStr))
        self.add_widget(self.topHeight)
        self.add_widget(OwnLabel(text=self.bhStr))
        self.add_widget(self.bottomHeight)
        # create the numpad
        self.numpad = Numpad(p=self)
        self.popup = OwnPopup(content=self.numpad)
        
    '''
    create all buttons of this component
    '''
        
    def create_all_btns(self):
        self.topWidth = OwnButton(text=str(self.csShape.tw))
        self.bottomWidth = OwnButton(text=str(self.csShape.bw))
        self.topHeight = OwnButton(text=str(self.csShape.th))
        self.bottomHeight = OwnButton(text=str(self.csShape.bh))
        self.topWidth.bind(on_press=self.show_numpad)
        self.topHeight.bind(on_press=self.show_numpad)
        self.bottomWidth.bind(on_press=self.show_numpad)
        self.bottomHeight.bind(on_press=self.show_numpad)
        
    
    '''
    open the popup and set the title of the popup
    '''
        
    def show_numpad(self, btn):
        self.focusBtn = btn
        if self.focusBtn == self.topHeight:
            self.popup.title = self.thStr
        elif self.focusBtn == self.topWidth:
            self.popup.title = self.twStr
        elif self.focusBtn == self.bottomHeight:
            self.popup.title = self.bhStr
        elif self.focusBtn == self.bottomWidth:
            self.popup.title = self.bwStr
        self.popup.open()
    
    '''
    close the numpad. this method will be call from the numpad
    '''
    def close_numpad(self):
        self.popup.dismiss()
        
    '''
    set the text of the button
    '''
    def finished_numpad(self):
        s = self.numpad.lblTextinput.text
        self.focusBtn.text, value = s, float(s)
        self.popup.dismiss()
        if self.focusBtn == self.topHeight:
            self.csShape.th = value
        elif self.focusBtn == self.topWidth:
            self.csShape.tw = value
        elif self.focusBtn == self.bottomHeight:
            self.csShape.bh = value
        elif self.focusBtn == self.bottomWidth:
            self.csShape.bw = value
        self.csShape.view.update()
