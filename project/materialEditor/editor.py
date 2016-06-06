# -*- coding: utf-8 -*-
'''
Created on 11.04.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from materialEditor.creater import MaterialCreater
from designClass.design import Design
from materialEditor.iobserver import IObserver


class MaterialEditor(ScrollView, IObserver):
    #Constructor
    def __init__(self, **kwargs):
        super(MaterialEditor, self).__init__(**kwargs)
        self.btnSize=Design.btnSize
    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''
    def createGui(self):
        self.createMaterialInformation()
        self.materialLayout=GridLayout(cols=1,spacing=2, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.materialLayout.bind(minimum_height=self.materialLayout.setter('height'))
        for i in self.allMaterials.allMaterials:
            btn=Button(text=i.name,size_hint_y=None, height=self.btnSize)
            btn.bind(on_press=self.showMaterialInformation)
            self.materialLayout.add_widget(btn)
        self.btnMaterialEditor=Button(text='create material',size_hint_y=None, height=self.btnSize)
        self.btnMaterialEditor.bind(on_press=self.createMaterial)
        self.materialLayout.add_widget(self.btnMaterialEditor)
        self.add_widget(self.materialLayout)
    
    '''
    create the popups: 
    popupInfo to show the material information
    popupCreate to create new material
    '''
    def createPopups(self):
        creater=MaterialCreater()
        creater.signInParent(self)
        self.popupInfo=Popup(title='material',content=self.content)
        self.popupCreate=Popup(title='create new material', content=creater)
        
    '''
    create the gui which is necessary for the show of the 
    material-information
    '''
    def createMaterialInformation(self):
        self.name=Label()
        self.price=Label()
        self.density=Label()
        self.stiffness=Label()
        self.strenght=Label()
        self.content=GridLayout(cols=2)
        self.content.add_widget(Label(text='name:'))
        self.content.add_widget(self.name)
        self.content.add_widget(Label(text='price[euro/kg]:'))
        self.content.add_widget(self.price)
        self.content.add_widget(Label(text='density[kg/m^3]:'))
        self.content.add_widget(self.density)
        self.content.add_widget(Label(text='stiffness[MPa]:'))
        self.content.add_widget(self.stiffness)
        self.content.add_widget(Label(text='strength[MPa]:'))
        self.content.add_widget(self.strenght)
        btnBack=Button(text='back',size_hint_y=None,height=self.btnSize)
        btnBack.bind(on_press=self.cancelShow)
        self.content.add_widget(btnBack)
        self.createPopups()
    
    '''
    set the labeltext with the materialproperties
    '''
    def showMaterialInformation(self,button):
        for i in range(0,self.csShape.allMaterials.getLength()):
            if self.allMaterials.allMaterials[i].name==button.text:
                self.name.text=self.allMaterials.allMaterials[i].name
                self.price.text=str(self.allMaterials.allMaterials[i].price)
                self.density.text=str(self.allMaterials.allMaterials[i].density)
                self.stiffness.text=str(self.allMaterials.allMaterials[i].stiffness)
                self.strenght.text=str(self.allMaterials.allMaterials[i].strength)
                self.popupInfo.open()
    
    '''
    close the popup, which shows the information from
    the choosen material
    '''
    def cancelShow(self,button):
        self.popupInfo.dismiss()
        
    '''
    open the popup, which has the creator as content
    '''
    def createMaterial(self,button):
        self.popupCreate.open()
    
    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''
    def update(self):
        self.materialLayout.remove_widget(self.btnMaterialEditor)
        btnMaterialA=Button(text=self.allMaterials.allMaterials[-1].name,size_hint_y=None, height=40)
        btnMaterialA.bind(on_press=self.showMaterialInformation)
        self.materialLayout.add_widget(btnMaterialA)
        self.materialLayout.add_widget(self.btnMaterialEditor)
        
    '''
    cancel the create-process. this method 
    is necessary, because editor is the parent 
    of the creator and creator call the method cancelEditMaterial
    from the parent
    '''
    def cancelEditMaterial(self):
        self.popupCreate.dismiss()
    
    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''
    def setCrossSection(self,cs):
        self.csShape=cs
        self.allMaterials=self.csShape.allMaterials
        self.allMaterials.addListener(self)
        self.createGui()
        