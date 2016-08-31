'''
Created on 13.06.2016

@author: mkennert
'''

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from kivy.properties import StringProperty

class CircleInformation(GridLayout):
    
    '''
    create the component, where you can change the diameter
    of the cross-section-circle
    '''
    
    # important components
    csShape = ObjectProperty()
    
    # strings
    diameter = StringProperty('diameter [m]')
    
    # Constructor
    def __init__(self, **kwargs):
        super(CircleInformation, self).__init__(**kwargs)
        print('create circle-information')
        self.cols, self.spacing = 2, Design.spacing
        self.height, self.size_hint_y = Design.btnHeight, None
    
    '''
    create the gui of the circle-information
    '''
    def create_gui(self):
        # create the popup where you can set the diamter
        self.numpad = Numpad(p=self)
        self.popup = OwnPopup(title=self.diameter, content=self.numpad)
        # create the information        
        self.add_widget(OwnLabel(text=self.diameter))
        self.btnDiameter = OwnButton(text=str(self.csShape.d))
        self.btnDiameter.bind(on_press=self.popup.open)
        self.add_widget(self.btnDiameter)
    
    '''
    close the numpad. this method will be call from the numpad
    '''
    def close_numpad(self):
        self.popup.dismiss()
        
    '''
    set the text of the button
    '''
    def finished_numpad(self):
        self.btnDiameter.text = self.numpad.lblTextinput.text
        d = float(self.btnDiameter.text)
        self.csShape.d = d
        self.csShape.view.update_circle(d)
        self.popup.dismiss()
