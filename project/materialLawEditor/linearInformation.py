'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from kivy.properties import  StringProperty
from materialLawEditor.ainformation import AInformation

class LinearInformation(GridLayout, AInformation):
    
    '''
    with the LinearInformation you can set the properties of the function
    '''
    
    linearStr = StringProperty('linear')
    
    aStr = StringProperty('a:')
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(LinearInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.create_gui()
        self.numpad = Numpad(sign=True, p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)

    '''
    create the gui of the linear-information, 
    where you can change the properties of the linear-function
    '''
    
    def create_gui(self):
        self.create_btns()
        self.add_widget(OwnLabel(text=self.functionStr))
        self.add_widget(self.btnLinear)
        self.add_widget(OwnLabel(text=self.aStr))
        self.add_widget(self.btnA)
        self.add_base_btns()
    
    '''
    create all btns of the gui
    '''
    
    def create_btns(self):
        self.btnLinear = OwnButton(text=self.linearStr)
        self.btnLinear.bind(on_press=self.show_type_selection)
        self.btnA = OwnButton(text=str(self.editor.a))
        self.btnA.bind(on_press=self.show_popup)
        self.create_base_btns()
       
    '''
    open the numpad popup
    '''
    
    def show_popup(self, btn):
        self.focusBtn = btn
        if self.focusBtn == self.btnA:
            self.popupNumpad.title = self.aStr
        self.set_popup_title()
        self.popupNumpad.open()

    '''
    when the user confirm his input
    '''
    
    def finished_numpad(self):
        v = float(self.numpad.lblTextinput.text)
        self.numpad.reset_text()
        if self.focusBtn == self.btnA:
            self.editor.a = v
        elif self.focusBtn == self.btnStrainUL:
            if v > self.editor.minStrain:
                self.editor.maxStrain = v
            else:
                return
        elif self.focusBtn == self.btnStrainLL:
            if v < self.editor.maxStrain:
                self.editor.minStrain = v
            else:
                return
        self.editor.view.update_graph_properties()
        self.focusBtn.text = str(v)
        self.popupNumpad.dismiss()
        
    '''
    update the complete information by the given function-properties
    '''
            
    def update_function(self, points, minStrain, maxStrain, a):
        self.btnStrainLL.text = str(minStrain)
        self.btnStrainUL.text = str(maxStrain)
        self.btnA.text = str(a)
