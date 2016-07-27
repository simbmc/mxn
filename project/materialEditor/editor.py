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
    # Constructor

    def __init__(self, **kwargs):
        super(MaterialEditor, self).__init__(**kwargs)
        self.btnSize = Design.btnSize
    '''
    the method create gui create the gui of 
    the materialEditor and create the popups
    '''

    def create_gui(self):
        self.create_material_information()
        self.materialLayout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.materialLayout.bind(
            minimum_height=self.materialLayout.setter('height'))
        for i in self.allMaterials.allMaterials:
            btn = Button(text=i.name, size_hint_y=None, height=self.btnSize)
            btn.bind(on_press=self.show_material_information)
            self.materialLayout.add_widget(btn)
        self.btnMaterialEditor = Button(
            text='create material', size_hint_y=None, height=self.btnSize)
        self.btnMaterialEditor.bind(on_press=self.create_material)
        self.materialLayout.add_widget(self.btnMaterialEditor)
        self.add_widget(self.materialLayout)

    '''
    create the popups: 
    popupInfo to show the material information
    popupCreate to create new material
    '''

    def create_popups(self):
        creater = MaterialCreater()
        creater.sign_in_parent(self)
        self.popupInfo = Popup(title='material', content=self.content)
        self.popupCreate = Popup(title='create new material', content=creater)

    '''
    create the gui which is necessary for the show of the 
    material-information
    '''

    def create_material_information(self):
        self.name = Label()
        self.price = Label()
        self.density = Label()
        self.material_law = Label()
        self.content = GridLayout(cols=2)
        self.content.add_widget(Label(text='name:'))
        self.content.add_widget(self.name)
        self.content.add_widget(Label(text='price[euro/kg]:'))
        self.content.add_widget(self.price)
        self.content.add_widget(Label(text='density[kg/m^3]:'))
        self.content.add_widget(self.density)
        self.content.add_widget(Label(text='material-law:'))
        self.content.add_widget(self.material_law)
        btnBack = Button(text='back', size_hint_y=None, height=self.btnSize)
        btnBack.bind(on_press=self.cancel_show)
        self.content.add_widget(btnBack)
        self.create_popups()

    '''
    set the labeltext with the materialproperties
    '''

    def show_material_information(self, button):
        for i in range(0, self.csShape.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name == button.text:
                self.name.text = self.allMaterials.allMaterials[i].name
                self.price.text = str(self.allMaterials.allMaterials[i].price)
                self.density.text = str(
                    self.allMaterials.allMaterials[i].density)
                self.material_law.text = self.allMaterials.allMaterials[
                    i].material_law.f_toString()
                self.popupInfo.open()

    '''
    close the popup, which shows the information from
    the choosen material
    '''

    def cancel_show(self, button):
        self.popupInfo.dismiss()

    '''
    open the popup, which has the creator as content
    '''

    def create_material(self, button):
        print('create new material')
        self.popupCreate.open()

    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''

    def update(self):
        self.materialLayout.remove_widget(self.btnMaterialEditor)
        btnMaterialA = Button(
            text=self.allMaterials.allMaterials[-1].name, size_hint_y=None, height=40)
        btnMaterialA.bind(on_press=self.show_material_information)
        self.materialLayout.add_widget(btnMaterialA)
        self.materialLayout.add_widget(self.btnMaterialEditor)

    '''
    cancel the create-process. this method 
    is necessary, because editor is the parent 
    of the creator and creator call the method cancel_edit_material
    from the parent
    '''

    def cancel_edit_material(self):
        print('cancel editor-class')
        self.popupCreate.dismiss()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.csShape = cs
        self.allMaterials = self.csShape.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
