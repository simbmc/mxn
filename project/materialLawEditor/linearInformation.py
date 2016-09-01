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
    
    # string-linear
    linearStr = StringProperty('linear')
    
    # string parameter a
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
        print(self.focusBtn == self.btnA)
        self.focusBtn.text = self.numpad.lblTextinput.text
        # close and reset the numpad
        self.popupNumpad.dismiss()
        self.numpad.reset_text()
        v = float(self.focusBtn.text)
        if self.focusBtn == self.btnA:
            self.editor.a = v
            self.editor.view.update_graph(v)
        elif self.focusBtn == self.btnStrainUL:
            self.editor.upperStrain = v
            self.editor.view.update_strain_upper_limit(v)
        elif self.focusBtn == self.btnStressUL:
            self.editor.upperStress = v
            self.editor.view.update_stress_upper_limit(v)
        elif self.focusBtn == self.btnStrainLL:
            self.editor.lowerStrain = v
            self.editor.view.update_strain_lower_limit(v)
        elif self.focusBtn == self.btnStressLL:
            self.editor.lowerStress = v
            self.editor.view.update_stress_lower_limit(v)
        
    '''
    update the complete information by the given function-properties
    '''
    def update_function(self, points, minStress, maxStress, minStrain, maxStrain, a):
        self.btnStrainLL.text = str(minStrain)
        self.btnStrainUL.text = str(maxStrain)
        self.btnStressLL.text = str(minStress)
        self.btnStressUL.text = str(maxStress)
        self.btnA.text = str(a)