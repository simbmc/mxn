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
from kivy.properties import  ObjectProperty, StringProperty

class LinearInformation(GridLayout):
    
    '''
    with the LinearInformation you can set the properties of the function
    '''
    
    # important components
    editor = ObjectProperty()
    
    # strings
    functionStr, linearStr = StringProperty('function:'), StringProperty('linear')
    aStr, strainULStr = StringProperty('a:'), StringProperty('strain-upper-limit:')
    strainLLStr, stressULStr = StringProperty('strain-lower-limit:'), StringProperty('stress-upper-limit  [MPa]:')
    stressLLStr = StringProperty('stress-lower-limit  [MPa]:')
    okStr, cancelStr = StringProperty('ok'), StringProperty('cancel')
    
    # constructor
    def __init__(self, **kwargs):
        super(LinearInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.row_force_default, self.row_default_height = True, Design.btnHeight
        self.create_gui()

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
        self.add_widget(OwnLabel(text=self.strainULStr))
        self.add_widget(self.btnStrainUL)
        self.add_widget(OwnLabel(text=self.stressULStr))
        self.add_widget(self.btnStressUL)
        self.add_widget(OwnLabel(text=self.strainLLStr))
        self.add_widget(self.btnStrainLL)
        self.add_widget(OwnLabel(text=self.stressLLStr))
        self.add_widget(self.btnStressLL)
        self.add_widget(self.btnConfirm)
        self.add_widget(self.btnCancel)
        # create the numpad for the input
        self.numpad = Numpad(sign=True, p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
    '''
    create all btns of the gui. this method to improve the code-overview
    '''
    def create_btns(self):
        self.btnStressUL = OwnButton(text=str(self.editor.upperStress))
        self.btnStressLL = OwnButton(text=str(self.editor.lowerStress))
        self.btnStrainUL = OwnButton(text=str(self.editor.upperStrain))
        self.btnStrainLL = OwnButton(text=str(self.editor.lowerStrain))
        self.btnA = OwnButton(text=str(self.editor.a))
        self.btnConfirm = OwnButton(text=self.okStr)
        self.btnCancel = OwnButton(text=self.cancelStr)
        self.btnLinear = OwnButton(text=self.linearStr)
        self.btnLinear.bind(on_press=self.show_type_selection)
        self.btnConfirm.bind(on_press=self.editor.confirm)
        self.btnStrainUL.bind(on_press=self.show_popup)
        self.btnStressUL.bind(on_press=self.show_popup)
        self.btnStressLL.bind(on_press=self.show_popup)
        self.btnStrainLL.bind(on_press=self.show_popup)
        self.btnCancel.bind(on_press=self.editor.cancel)
        self.btnA.bind(on_press=self.show_popup)
        
    '''
    close the numpad when the user cancel the input
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()

    '''
    open the numpad popup
    '''
    def show_popup(self, btn):
        self.focusBtn = btn
        if self.focusBtn == self.btnA:
            self.popupNumpad.title = self.aStr
        elif self.focusBtn == self.btnStrainUL:
            self.popupNumpad.title = self.strainULStr
        elif self.focusBtn == self.btnStressUL:
            self.popupNumpad.title = self.stressULStr
        elif self.focusBtn == self.btnStrainLL:
            self.popupNumpad.title = self.strainLLStr
        elif self.focusBtn == self.btnStressLL:
            self.popupNumpad.title = self.stressLLStr
        self.popupNumpad.open()
    
    def show_type_selection(self, btn):
        self.editor.lawEditor.editor.open()
    
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
