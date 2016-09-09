'''
Created on 26.08.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from materialEditor.materiallist import MaterialList
from ownComponents.ownPopup import OwnPopup


class EditBar(GridLayout):
    
    '''
    the class EditBar contains the components where you
    can add or edit layers in the reinforcement-editor 
    '''
    
    # reinforcement editor
    p = ObjectProperty()
    
    materialStr = StringProperty('material')
    
    steelStr = StringProperty('steel')
    
    xCoordinateStr = StringProperty('x-coordinate [m]')
    
    yCoordinateStr = StringProperty('y-coordinate [m]')
    
    csAreaStr = StringProperty('cross-sectional area')
    
    defaultValueStr = StringProperty('0.0')
    
    confirmStr = StringProperty('ok')
    
    cancelStr = StringProperty('cancel')
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(EditBar, self).__init__(**kwargs)
        self.allMaterial = MaterialList.Instance()
        self.numpad = Numpad(p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)
        self.create_add_area()
        
    '''
    create the area where you can add new layers to the focus-shape
    '''
    def create_add_area(self):
        self.addArea = GridLayout(cols=2, row_force_default=True,
                                    row_default_height=Design.btnHeight,
                                    height=Design.btnHeight,
                                    spacing=Design.spacing)
        self.create_btns()
        # fill the addArea with content
        self.addArea.add_widget(OwnLabel(text=self.materialStr))
        self.addArea.add_widget(self.materialBtn)
        self.addArea.add_widget(OwnLabel(text=self.xCoordinateStr))
        self.addArea.add_widget(self.xCoordinateBtn)
        self.addArea.add_widget(OwnLabel(text=self.yCoordinateStr))
        self.addArea.add_widget(self.yCoordinateBtn)
        self.addArea.add_widget(OwnLabel(text=self.csAreaStr))
        self.addArea.add_widget(self.csAreaBtn)
        self.addArea.add_widget(self.confirmBtn)
        self.addArea.add_widget(self.cancelBtn)
    
    '''
    create all btns of the component
    '''
        
    def create_btns(self):
        # create btns
        self.materialBtn = OwnButton(text=self.steelStr)
        self.xCoordinateBtn = OwnButton(text=self.defaultValueStr)
        self.yCoordinateBtn = OwnButton(text=self.defaultValueStr)
        self.csAreaBtn = OwnButton(text=self.defaultValueStr)
        self.confirmBtn = OwnButton(text=self.confirmStr)
        self.cancelBtn = OwnButton(text=self.cancelStr)
        # bind the btns
        self.materialBtn.bind(on_press=self.show_material_selection)   
        self.confirmBtn.bind(on_press=self.confirm_input)
        self.cancelBtn.bind(on_press=self.cancel_input)
        self.xCoordinateBtn.bind(on_press=self.show_numpad)
        self.yCoordinateBtn.bind(on_press=self.show_numpad)
        self.csAreaBtn.bind(on_press=self.show_numpad)
        
    '''
    open the popup where the user can the select the 
    material of the bar
    '''
    def show_material_selection(self, btn):
        self.p.popupMaterial.open()
    
    '''
    open the numpad and set the title of the popup
    '''
    def show_numpad(self, btn):
        self.focusBtn = btn
        if btn == self.yCoordinateBtn:
            self.popupNumpad.title = self.yCoordinateStr
        elif btn == self.csAreaBtn:
            self.popupNumpad.title = self.csAreaStr
        elif btn == self.xCoordinateBtn:
            self.popupNumpad.title = self.xCoordinateStr
        self.popupNumpad.open()
    
    '''
    finished the numpad-input and save the value
    '''
    def finished_numpad(self):
        s = self.numpad.lblTextinput.text
        if self.focusBtn == self.yCoordinateBtn:
            self.yCoordinateBtn.text = s
        elif self.focusBtn == self.csAreaBtn:
            self.csAreaBtn.text = s
        elif self.focusBtn == self.xCoordinateBtn:
            self.xCoordinateBtn.text = s
        self.popupNumpad.dismiss()
    
    '''
    cancel the numpad-input
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()
    
    '''
    when the user confirm the input
    '''
    def confirm_input(self, btn):
        if self.add:
            # when the user add a layer
            x = float(self.xCoordinateBtn.text)
            y = float(self.yCoordinateBtn.text)
            csArea = float(self.csAreaBtn.text)
            for i in range(0, len(self.allMaterial.allMaterials)):
                material = self.allMaterial.allMaterials[i]
                if material.name == self.materialBtn.text:
                    self.p.add_bar(x, y, csArea, material)
                    return
        else:
            # when the user want edit
            x = float(self.xCoordinateBtn.text)
            y = float(self.yCoordinateBtn.text)
            csArea = float(self.csAreaBtn.text)
            for i in range(0, len(self.allMaterial.allMaterials)):
                material = self.allMaterial.allMaterials[i]
                if material.name == self.materialBtn.text:
                    self.p.edit_bar(x, y, csArea, material)
                    return
    
    '''
    when the user cancel the input
    '''
    def cancel_input(self, btn):
        self.p.cancel_editing_bar(btn)
    
    '''
    the method update_layer_information was developed to update
    the information, when the user select a bar in the view
    '''
    def update_bar_information(self, x, y, csArea, material):
        self.xCoordinateBtn.text = str(x)
        self.yCoordinateBtn.text = str(y)
        self.csAreaBtn.text = str(csArea)
        self.materialBtn.text = material.name
