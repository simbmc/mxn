'''
Created on 06.05.2016

@author: mkennert
'''

from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from kivy.properties import  ObjectProperty, StringProperty

class MultilinearInformation(GridLayout):
    
    # important components
    editor = ObjectProperty()
    
    # strings
    functionStr, mulitlinearStr = StringProperty('function:'), StringProperty('multi-linear')
    pointsStr, strainULStr = StringProperty('points:'), StringProperty('strain-upper-limit [MPa]:')
    strainLLStr, stressULStr = StringProperty('strain-lower-limit [MPa]:'), StringProperty('stress-upper-limit[MPa]:')
    stressLLStr = StringProperty('stress-lower-limit [MPa]:')
    okStr, cancelStr = StringProperty('ok'), StringProperty('cancel')
    xStr, yStr = StringProperty('x-coordinate [m]:'), StringProperty('y-coordinate [m]:')
    
    # constructor
    def __init__(self, **kwargs):
        super(MultilinearInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.row_force_default = True
        self.row_default_height = Design.btnHeight
        self.create_information()
    
    '''
    create the gui of the information
    '''
    def create_information(self):
        self.create_btns()
        self.add_widget(OwnLabel(text=self.functionStr))
        self.add_widget(self.btnMultiLinear)
        self.add_widget(OwnLabel(text=self.pointsStr))
        self.add_widget(self.pointsBtn)
        self.add_widget(OwnLabel(text=self.strainULStr))
        self.add_widget(self.heightBtn)
        self.add_widget(OwnLabel(text=self.stressULStr))
        self.add_widget(self.widthBtn)
        self.add_widget(OwnLabel(text=self.strainLLStr))
        self.add_widget(self.strainlowerLimit)
        self.add_widget(OwnLabel(text=self.stressLLStr))
        self.add_widget(self.stresslowerLimit)
        self.add_widget(OwnLabel(text=self.xStr))
        self.add_widget(self.btnX)
        self.add_widget(OwnLabel(text=self.yStr))
        self.add_widget(self.btnY)
        self.add_widget(self.btnConfirm)
        self.add_widget(self.btnCancel)
        # create the popup
        self.numpad = Numpad(sign=True, p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
    '''
    create the btns
    '''
    def create_btns(self):
        self.pointsBtn = OwnButton(text=str(self.editor._points))
        self.heightBtn = OwnButton(text=str(self.editor.upperStrain))
        self.widthBtn = OwnButton(text=str(self.editor.upperStress))
        self.stresslowerLimit = OwnButton(text=str(self.editor.lowerStrain))
        self.strainlowerLimit = OwnButton(text=str(self.editor.lowerStress))
        self.btnX = OwnButton(text='-')
        self.btnY = OwnButton(text='-')
        self.btnConfirm = OwnButton(text=self.okStr)
        self.btnCancel = OwnButton(text=self.cancelStr)
        self.btnMultiLinear = OwnButton(text=self.mulitlinearStr)
        self.btnMultiLinear.bind(on_press=self.show_type_selection)
        self.btnConfirm.bind(on_press=self.editor.confirm)
        self.btnConfirm.bind(on_press=self.editor.confirm)
        self.btnCancel.bind(on_press=self.editor.cancel)
        self.pointsBtn.bind(on_press=self.show_popup)
        self.heightBtn.bind(on_press=self.show_popup)
        self.widthBtn.bind(on_press=self.show_popup)
        self.strainlowerLimit.bind(on_press=self.show_popup)
        self.stresslowerLimit.bind(on_press=self.show_popup)
        self.btnX.bind(on_press=self.show_popup)
        self.btnY.bind(on_press=self.show_popup)
        
    '''
    create the popup with the numpad as content
    '''
    def create_popup(self):
        self.numpad = Numpad(sign=True, p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
    '''
    update the coordinates of the btn by the given coordinate
    '''
    def update_coordinates(self, x, y):
        self.btnX.text = str(x)
        self.btnY.text = str(y)
    
    '''
    open the numpad popup
    '''
    def show_popup(self, btn):
        self.focusBtn = btn
        if self.focusBtn == self.pointsBtn:
            self.popupNumpad.title = self.pointsStr
        elif self.focusBtn == self.widthBtn:
            self.popupNumpad.title = self.stressULStr
        elif self.focusBtn == self.heightBtn:
            self.popupNumpad.title = self.strainULStr
        elif self.focusBtn == self.btnX:
            self.popupNumpad.title = self.xStr
        elif self.focusBtn == self.btnY:
            self.popupNumpad.title = self.yStr
        elif self.focusBtn == self.strainlowerLimit:
            self.popupNumpad.title = self.strainLLStr
        elif self.focusBtn == self.stresslowerLimit:
            self.popupNumpad.title = self.stressLLStr
        self.popupNumpad.open()
    
    def show_type_selection(self, btn):
        print('show type_selection (mulitlinearinformation)')
        self.editor.lawEditor.editor.open()
        
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()
        
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text = self.numpad.lblTextinput.text
        v = float(self.focusBtn.text)
        self.popupNumpad.dismiss()
        self.numpad.reset_text()
        if self.focusBtn == self.pointsBtn:
            self.editor._points = int(v)
            self.editor.view.update_points()
        elif self.focusBtn == self.widthBtn:
            self.editor.upperStress = v
            self.editor.view.update_graph()
        elif self.focusBtn == self.heightBtn:
            self.editor.upperStrain = v
            self.editor.view.update_graph()
        elif self.focusBtn == self.btnX:
            self.editor.view.update_point_position(float(self.btnX.text), float(self.btnY.text))
        elif self.focusBtn == self.btnY:
                self.editor.view.update_point_position(float(self.btnX.text), float(self.btnY.text))
        elif self.focusBtn == self.strainlowerLimit:
            self.editor.lowerStrain = v
            self.editor.view.update_graph()
        elif self.focusBtn == self.stresslowerLimit:
            self.editor.lowerStress = v
            self.editor.view.update_graph()
