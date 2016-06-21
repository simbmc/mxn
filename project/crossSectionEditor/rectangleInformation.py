'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from designClass.design import Design
from materialEditor.numpad import Numpad
from kivy.uix.popup import Popup
class RectangleInformation(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(RectangleInformation, self).__init__(**kwargs)
        self.cols=2
        self.size_hint_y=None
        self.spacing=10
        self.btnSize=Design.btnSize
        self.focusbtn=None
    
    '''
    create the gui
    '''
    def create_gui(self):
        #create Numpad
        self.numpad=Numpad()
        self.numpad.sign_in_parent(self)
        self.popUp=Popup(content=self.numpad)
        #adding_material_area to manage the height-area
        self.heightValue=Label(text='height: 0.5 m',size_hint_x=None, width=100)
        self.btnHeight=Button(text='0.5',size_hint_y=None, height=self.btnSize)
        self.btnHeight.bind(on_press=self.show_numpad)
        self.add_widget(self.heightValue)
        self.add_widget(self.btnHeight)
        #adding_material_area to manage the width-area
        self.widthValue=Label(text='width: 0.25 m',size_hint_x=None, width=100)
        self.btnWidth=Button(text='0.25',size_hint_y=None, height=self.btnSize)
        self.btnWidth.bind(on_press=self.show_numpad)
        self.add_widget(self.widthValue)
        self.add_widget(self.btnWidth)
    
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popUp.dismiss()
    
    def show_numpad(self,btn):
        self.focusbtn=btn
        self.popUp.open()
    
    def finished_numpad(self):
        self.focusbtn.text=self.numpad.textinput.text
        if self.focusbtn==self.btnHeight:
            self.set_height(float(self.focusbtn.text))
        else:
            self.set_width(float(self.focusbtn.text))
        self.popUp.dismiss()
        
    '''
    set the cross-section
    '''
    def set_cross_section(self,cs):
        self.csShape=cs
        self.create_gui()
    
    '''
    the method set_height change the height of the cs_view
    '''
    def set_height(self,value):
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.y_ticks_major=value/5.
        self.csShape.set_height(value)
        self.heightValue.text='height: '+str(value)+' m'
    
    '''
    the method set_width change the width of the cs_view
    '''
    def set_width(self,value):
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.x_ticks_major=value/5.
        self.csShape.set_width(value)
        self.widthValue.text='width: '+str(value)+' m'