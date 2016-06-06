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
    def createGUI(self):
        #create Numpad
        self.numpad=Numpad()
        self.numpad.signInParent(self)
        self.popUp=Popup(content=self.numpad)
        #adding_material_area to manage the height-area
        self.heightValue=Label(text='height: 0.5 m',size_hint_x=None, width=100)
        self.btnHeight=Button(text='0.5',size_hint_y=None, height=self.btnSize)
        self.btnHeight.bind(on_press=self.showNumpad)
        self.add_widget(self.heightValue)
        self.add_widget(self.btnHeight)
        #adding_material_area to manage the width-area
        self.widthValue=Label(text='width: 0.25 m',size_hint_x=None, width=100)
        self.btnWidth=Button(text='0.25',size_hint_y=None, height=self.btnSize)
        self.btnWidth.bind(on_press=self.showNumpad)
        self.add_widget(self.widthValue)
        self.add_widget(self.btnWidth)
    
    '''
    close the numpad
    '''
    def closeNumpad(self):
        self.popUp.dismiss()
    
    def showNumpad(self,btn):
        self.focusbtn=btn
        self.popUp.open()
    
    def finishedNumpad(self):
        self.focusbtn.text=self.numpad.textinput.text
        if self.focusbtn==self.btnHeight:
            self.setHeight(float(self.focusbtn.text))
        else:
            self.setWidth(float(self.focusbtn.text))
        self.popUp.dismiss()
        
    '''
    set the cross-section
    '''
    def setCrossSection(self,cs):
        self.csShape=cs
        self.createGUI()
    
    '''
    the method setHeight change the height of the cs_view
    '''
    def setHeight(self,value):
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.y_ticks_major=value/5.
        self.csShape.setHeight(value)
        self.heightValue.text='height: '+str(value)+' m'
    
    '''
    the method setWidth change the width of the cs_view
    '''
    def setWidth(self,value):
        self.csShape.view.graph._clear_buffer()
        self.csShape.view.graph.x_ticks_major=value/5.
        self.csShape.setWidth(value)
        self.widthValue.text='width: '+str(value)+' m'