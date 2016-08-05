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


class RectangleInformation(GridLayout):
    '''
    create the component, where you can change the height and 
    the width of the cross-section-rectangle
    '''
    csShape=ObjectProperty()
    #Constructor
    def __init__(self, **kwargs):
        super(RectangleInformation, self).__init__(**kwargs)
        self.cols=2
        self.spacing=Design.spacing
        self.size_hint_y=None
    
    '''
    create the gui
    '''
    def create_gui(self):
        #create Numpad
        self.numpad=Numpad()
        self.numpad.sign_in_parent(self)
        self.popUp=OwnPopup(content=self.numpad)
        #adding_material_area to manage the height-area
        self.heightValue=OwnLabel(text='height [m]')
        self.btnHeight=OwnButton(text='0.5')
        self.btnHeight.bind(on_press=self.show_numpad)
        self.add_widget(self.heightValue)
        self.add_widget(self.btnHeight)
        #adding_material_area to manage the width-area
        self.widthValue=OwnLabel(text='width [m]')
        self.btn_stress_upper_limit=OwnButton(text='0.25')
        self.btn_stress_upper_limit.bind(on_press=self.show_numpad)
        self.add_widget(self.widthValue)
        self.add_widget(self.btn_stress_upper_limit)
    
    '''
    the method update_height change the height of the cs_view
    '''
    def update_height(self,value):
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.y_ticks_major=value/5.
        self.csShape.update_height(value)
    
    '''
    the method update_width change the width of the cs_view
    '''
    def update_width(self,value):
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.x_ticks_major=value/5.
        self.csShape.update_width(value)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popUp.dismiss()
    
    '''
    show the numpad
    '''
    def show_numpad(self,btn):
        self.focusbtn=btn
        self.popUp.open()
    
    '''
    set the values
    '''
    def finished_numpad(self):
        self.focusbtn.text=self.numpad.lblTextinput.text
        if self.focusbtn==self.btnHeight:
            self.update_height(float(self.focusbtn.text))
        else:
            self.update_width(float(self.focusbtn.text))
        self.popUp.dismiss()