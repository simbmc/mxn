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
        self.add_base_btns()
    
    '''
    create the btns
    '''
    def create_btns(self):
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
        self.set_popup_title()
        self.popupNumpad.open()
        
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text = self.numpad.lblTextinput.text
        v = float(self.focusBtn.text)
        self.numpad.reset_text()
        self.popupNumpad.dismiss()
        if self.focusBtn == self.pointsBtn:
            self.editor._points = int(v)
            self.editor.view.update_points()
        elif self.focusBtn == self.btnStressUL:
            self.editor.upperStress = v
            self.editor.view.update_graph()
        elif self.focusBtn == self.strainULStr:
            self.editor.upperStrain = v
            self.editor.view.update_graph()
        elif self.focusBtn == self.btnX:
            self.editor.view.update_point_position(float(self.btnX.text), float(self.btnY.text))
        elif self.focusBtn == self.btnY:
                self.editor.view.update_point_position(float(self.btnX.text), float(self.btnY.text))
        elif self.focusBtn == self.btnStrainLL:
            self.editor.lowerStrain = v
            self.editor.view.update_graph()
        elif self.focusBtn == self.stressLLStr:
            self.editor.lowerStress = v
            self.editor.view.update_graph()

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
        self.btnStrainLL.text = str(minStrain)
        self.btnStrainUL.text = str(maxStrain)
        self.btnStressLL.text = str(minStress)
        self.btnStressUL.text = str(maxStress)
        self.btnX.text = str(0)
        self.btnY.text = str(0)
