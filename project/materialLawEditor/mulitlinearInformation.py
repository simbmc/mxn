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
from kivy.properties import  StringProperty
from materialLawEditor.ainformation import AInformation

class MultilinearInformation(GridLayout, AInformation):
    
    '''
    with the MultilinearInformation you can set the properties of the linear-function
    '''
    
    # string multi-linear
    mulitlinearStr = StringProperty('multi-linear')
    
    # string points
    pointsStr = StringProperty('points:')
    
    # string x-coordinate
    xStr = StringProperty('x-coordinate [m]:')
    
    # string y-coordinate
    yStr = StringProperty('y-coordinate [m]:')
    
    # string stress-upper-limit  [MPa]
    stressULStr = StringProperty('stress-upper-limit [MPa]:')
    
    # string stress-lower-limit [MPa]
    stressLLStr = StringProperty('stress-lower-limit [MPa]:')
    
    '''
    constructor
    '''
    
    def __init__(self, **kwargs):
        super(MultilinearInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.create_information()
        # create the numpad
        self.numpad = Numpad(sign=True, p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
    '''
    create the gui of the information
    '''
    
    def create_information(self):
        self.create_btns()
        self.add_widget(OwnLabel(text=self.functionStr))
        self.add_widget(self.btnMultiLinear)
        self.add_widget(OwnLabel(text=self.pointsStr))
        self.add_widget(self.pointsBtn)
        self.add_widget(OwnLabel(text=self.xStr))
        self.add_widget(self.btnX)
        self.add_widget(OwnLabel(text=self.yStr))
        self.add_widget(self.btnY)
        self.add_widget(OwnLabel(text=self.stressULStr))
        self.add_widget(self.btnStressUL)
        self.add_widget(OwnLabel(text=self.stressLLStr))
        self.add_widget(self.btnStressLL)
        self.add_base_btns()
    
    '''
    create the btns
    '''
    
    def create_btns(self):
        self.btnStressUL = OwnButton(text=str(self.editor.upperStress))
        self.btnStressUL.bind(on_press=self.show_popup)
        self.btnStressLL = OwnButton(text=str(self.editor.lowerStress))
        self.btnStressLL.bind(on_press=self.show_popup)
        self.pointsBtn = OwnButton(text=str(self.editor._points))
        self.pointsBtn.bind(on_press=self.show_popup)
        self.btnMultiLinear = OwnButton(text=self.mulitlinearStr)
        self.btnMultiLinear.bind(on_press=self.show_type_selection)
        self.btnX = OwnButton(text='-')
        self.btnY = OwnButton(text='-')
        self.btnX.bind(on_press=self.show_popup)
        self.btnY.bind(on_press=self.show_popup)
        self.create_base_btns()
    
    '''
    open the numpad popup
    '''
    
    def show_popup(self, btn):
        self.focusBtn = btn
        if self.focusBtn == self.pointsBtn:
            self.popupNumpad.title = self.pointsStr
        elif self.focusBtn == self.btnX:
            self.popupNumpad.title = self.xStr
        elif self.focusBtn == self.btnY:
            self.popupNumpad.title = self.yStr
        elif self.focusBtn == self.btnStressUL:
            self.popupNumpad.title = self.stressULStr
        elif self.focusBtn == self.btnStressLL:
            self.popupNumpad.title = self.stressLLStr
        self.set_popup_title()
        self.popupNumpad.open()
        
    '''
    the method finished_numpad close the numpad_popup
    '''
    
    def finished_numpad(self):
        v = float(self.numpad.lblTextinput.text)
        if self.focusBtn == self.pointsBtn:
            if v > 0:
                self.editor._points = int(v)
                self.editor.view.update_points()
            else:
                return
        elif self.focusBtn == self.btnStressUL:
            if v > self.editor.lowerStress:
                self.editor.upperStress = v
                self.editor.view.update_graph()
            else:
                return
        elif self.focusBtn == self.btnStrainUL:
            if v > self.editor.minStrain:
                self.editor.maxStrain = v
                self.editor.view.update_graph()
            else:
                return
        elif self.focusBtn == self.btnX:
            self.editor.view.update_point_position(float(self.btnX.text), float(self.btnY.text))
        elif self.focusBtn == self.btnY:
                self.editor.view.update_point_position(float(self.btnX.text), float(self.btnY.text))
        elif self.focusBtn == self.btnStrainLL:
            if v < self.editor.maxStrain:
                self.editor.minStrain = v
                self.editor.view.update_graph()
            else:
                return
        elif self.focusBtn == self.btnStressLL:
            if v < self.editor.maxStrain:
                self.editor.lowerStress = v
                self.editor.view.update_graph()
            else:
                return
        self.focusBtn.text = str(v)
        self.numpad.reset_text()
        self.popupNumpad.dismiss()

    '''
    update the coordinates of the btn by the given coordinate
    '''
    
    def update_coordinates(self, x, y):
        self.btnX.text = str(x)
        self.btnY.text = str(y)
    
    '''
    update the complete information by the given function-properties
    '''
    
    def update_function(self, points, minStress, maxStress, minStrain, maxStrain):
        self.pointsBtn.text = str(len(points) - 1)
        self.btnStrainLL.text = str(minStrain)
        self.btnStrainUL.text = str(maxStrain)
        self.btnStressLL.text = str(minStress)
        self.btnStressUL.text = str(maxStress)
        self.btnX.text = str(0)
        self.btnY.text = str(0)
    
