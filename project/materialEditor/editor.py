'''
Created on 11.04.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot


class MaterialEditor(ScrollView, IObserver):
    # Constructor

    def __init__(self, **kwargs):
        super(MaterialEditor, self).__init__(**kwargs)
        self.btnSize = Design.btnHeight
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
            btn = OwnButton(text=i.name)
            btn.bind(on_press=self.show_material_information)
            self.materialLayout.add_widget(btn)
        self.btnMaterialEditor = OwnButton(text='create material')
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
        creater._parent = self  # sign_in_parent(self)
        self.popupInfo = OwnPopup(title='material', content=self.content)
        self.popupCreate = OwnPopup(title='create new material', content=creater)

    '''
    create the gui which is necessary for the show of the 
    material-information
    '''

    def create_material_information(self):
        self.name = OwnLabel()
        self.price = OwnLabel()
        self.density = OwnLabel()
        self.material_law = OwnLabel()
        self.content = GridLayout(cols=2,spacing=Design.spacing)
        self.information=GridLayout(cols=2)
        self.information.add_widget(OwnLabel(text='name:'))
        self.information.add_widget(self.name)
        self.information.add_widget(OwnLabel(text='price[euro/kg]:'))
        self.information.add_widget(self.price)
        self.information.add_widget(OwnLabel(text='density[kg/m^3]:'))
        self.information.add_widget(self.density)
        self.information.add_widget(OwnLabel(text='material-law:'))
        self.information.add_widget(self.material_law)
        btnBack = OwnButton(text='back')
        btnBack.bind(on_press=self.cancel_show)
        self.graph = OwnGraph(y_grid_label=True, x_grid_label=True)
        self.p=LinePlot()
        self.graph.add_plot(self.p)
        self.content.add_widget(self.information)
        self.content.add_widget(self.graph)
        self.content.add_widget(btnBack)
        self.create_popups()

    '''
    set the labeltext with the materialproperties
    '''

    def show_material_information(self, button):
        for i in range(0, self.csShape.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name == button.text:
                material = self.allMaterials.allMaterials[i]
                self.name.text = material.name
                self.price.text = str(material.price)
                self.density.text = str(material.density)
                self.material_law.text = material.material_law.f_toString()
                self.graph.remove_plot(self.p)
                self.p=LinePlot(points=material.material_law.points,color=[0,0,0,1])
                print(str(self.p.points))
                self.graph.add_plot(self.p)
                self.graph.xmin = material.material_law.minStress
                self.graph.xmax = material.material_law.maxStress
                self.graph.ymin = material.material_law.minStrain
                self.graph.ymax = material.material_law.maxStrain
                self.graph.x_ticks_major=self.graph.xmax/5.
                self.graph.y_ticks_major=self.graph.ymax/5.
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
        self.popupCreate.open()

    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''

    def update(self):
        self.materialLayout.remove_widget(self.btnMaterialEditor)
        btnMaterialA = OwnButton(text=self.allMaterials.allMaterials[-1].name)
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
