'''
Created on 15.08.2016

@author: mkennert
'''
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from materialEditor.materiallist import MaterialList
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
from plot.line import LinePlot

# not used yet
class MaterialSelector(GridLayout):
    
    '''
    with the material-selector you can see the material-information and the material-law and
    select one material. 
    '''
    
    # important components
    p = ObjectProperty()
    
    # constructor
    def __init__(self, **kwargs):
        super(MaterialSelector, self).__init__(**kwargs)
        self.cols = 1
        self.content = GridLayout(cols=2)
        self.allMaterials = MaterialList.Instance()
        self.create_gui()
    
    '''
    create the gui of the material-selcetor
    '''
    def create_gui(self):
        self.create_material_selection()
        self.create_information()
        self.add_widget(self.content)
        self.create_confirm_cancel()
        self.add_widget(self.editLayout)
        
    '''
    create the graph to show the stress-strain-behavior of the 
    material
    '''
    def create_information(self):
        information = GridLayout(cols=1)
        self.nameLbl = OwnLabel(text='-')
        self.priceLbl = OwnLabel(text='-')
        information.add_widget(self.nameLbl)
        information.add_widget(self.priceLbl)
        self.graph = OwnGraph(xlabel='strain', ylabel='stress',
                              y_grid_label=True, x_grid_label=True)
        # default material is steel
        steel = self.allMaterials.allMaterials[0]
        self.graph.xmin = steel.materialLaw.minStress
        self.graph.xmax = steel.materialLaw.maxStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.ymin = steel.materialLaw.minStrain
        self.graph.ymax = steel.materialLaw.maxStrain
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        self.plot = LinePlot(points=steel.materialLaw.points, color=[0, 0, 0, 1])
        self.graph.add_plot(self.plot)
        information.add_widget(self.graph)
        self.content.add_widget(information)
    
    '''
    create the btns to see the material-information by the selected material
    '''
    def create_material_selection(self):
        self.materialLayout = GridLayout(cols=1, spacing=Design.spacing)
        # Make sure the height is such that there is something to scroll.
        self.materialLayout.bind(minimum_height=self.materialLayout.setter('height'))
        for i in self.allMaterials.allMaterials:
            btn = OwnButton(text=i.name)
            btn.bind(on_press=self.show_material_information)
            self.materialLayout.add_widget(btn)
        self.content.add_widget(self.materialLayout)
    
    '''
    create the area, where you confirm or cancel the material-selection
    '''
    def create_confirm_cancel(self):
        self.editLayout = GridLayout(cols=2, row_force_default=True, height=Design.btnHeight,
                              row_default_height=Design.btnHeight, size_hint_y=None,
                              spacing=Design.spacing)
        confirmBtn = OwnButton(text='confirm')
        confirmBtn.bind(on_press=self.confirm)
        cancelBtn = OwnButton(text='cancel')
        cancelBtn.bind(on_press=self.cancel)
        self.editLayout.add_widget(confirmBtn)
        self.editLayout.add_widget(cancelBtn)
    
    '''
    show the material-information of the selected material
    '''
    def show_material_information(self, btn):
        self.focus_btn = btn
        for i in self.allMaterials.allMaterials:
            if i.name == btn.text:
                material = i
        self.graph.xmin = material.materialLaw.minStress
        self.graph.xmax = material.materialLaw.maxStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        self.graph.ymin = material.materialLaw.minStrain
        self.graph.ymax = material.materialLaw.maxStrain
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        self.plot = LinePlot(points=material.materialLaw.points, color=[0, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.nameLbl.text = 'name: ' + material.name
        self.priceLbl.text = 'price: ' + str(material.price) + ' [Euro]'
    
    '''
    the method confirm the material selection. 
    make sure, that the parent have the method confirm_material_selection()
    '''
    def confirm(self, btn):
        self.p.confirm_material_selection(btn.text)
    
    '''
    the method cancel the material selection. 
    make sure, that the parent have the method cancel_material_selection()
    '''
    def cancel(self, btn):
        self.p.cancel_material_selection()
        
    
# just for testing
class TestApp(App):
    Window.clearcolor = (1, 1, 1, 1)
    def build(self):
        return MaterialSelector()


if __name__ == '__main__':
    TestApp().run()
