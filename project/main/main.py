'''
Created on 14.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar, ActionPrevious
from kivy.uix.gridlayout import GridLayout

from crossSection.cs import CrossSection
from crossSectionEditor.editor import CrossSectionEditor
from materialEditor.editor import MaterialEditor
from ownComponents.design import Design
from reinforcementEditor.refEdit import ReinforcementEditorfrom explorer.stressStrainExplorer import Explorer
from mxnenvelope.envelope import MXNEnvelop
from kivy.properties import BooleanProperty

Window.clearcolor = (1, 1, 1, 1)

class AppActionBar(ActionBar):
    '''
    create the Actionbar in the mainMenu with the kv.file 
    '''
    pass

class ActionMenu(ActionPrevious):
    '''
    create the ActionMenu in the mainMenu with the kv.file 
    '''
    pass


class MXNApp(App):
    
    # switch to proof whether the explorer-component was created
    boolExplorer = BooleanProperty(True)
    
    # switch to proof whether the mxnEnvelope-component was created
    boolMXNEnvelope = BooleanProperty(True)
    
    # switch to proof whether the material-editor was created
    boolMaterialEditor = BooleanProperty(True)
    
    # switch to proof whether the reinforcement-editor was created
    boolReinforcementEditor = BooleanProperty(True)
    
    '''
    Build the application
    '''
    
    # constructor
    def build(self):
        self.content = GridLayout(cols=1, spacing=Design.spacing)
        bar = AppActionBar()
        self.content.add_widget(bar)
        self.cs = CrossSection(app=self)
        self.csShape = self.cs.csRectangle
        # cross-section-editor is the default view
        # view is the focus-component
        self.view = self.cs
        self.create_cross_section_editor()
        return self.content

    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.materialEditor = MaterialEditor(csShape=self.cs)

    '''
    create the cross section-editor
    '''

    def create_cross_section_editor(self):
        self.csEditor = CrossSectionEditor(cs=self.cs, csShape=self.cs.csRectangle, app=self)
        self.csEditor.add_view()
        self.content.add_widget(self.csEditor)
        self.view = self.csEditor

    '''
    create the reinforcement-editor
    '''

    def create_reinforcement_editor(self):
        self.reEditor = ReinforcementEditor()
        self.reEditor.set_cross_section(self.cs)
    
    '''
    create the explorer where you can see the stress-strain-behavior of the
    cross section
    '''
        
    def create_explorer(self):
        self.explorer = Explorer(csShape=self.csShape, bars=self.csShape.bars,
                                 layers=self.csShape.layers)
        self.cs.explorer = self.explorer
    
    '''
    create the mxnEmelope
    '''
    def create_mxnEnvelope(self):
        if self.boolExplorer:
            self.create_explorer()
            self.boolExplorer = False
        self.mxnEmelope = MXNEnvelop(explorer=self.explorer)
    
    #############################################################################
    # Attention:When you want write a new show-method than make sure             #
    # that actually component is remove from the widget and set                  #
    # the content to the showed component                                        #
    #############################################################################

    '''
    show the material-editor
    '''

    def show_material_editor(self):
        #if the material-editor has not been created
        if self.boolMaterialEditor:
            self.create_material_editor()
            #change the switch
            self.boolMaterialEditor = False
        self.content.remove_widget(self.view)
        self.content.add_widget(self.materialEditor)
        self.view = self.materialEditor

    '''
    show the cs editor
    '''

    def show_cross_section_editor(self):
        #if the reinforcement-editor has not been created
        if self.boolReinforcementEditor:
            self.create_reinforcement_editor()
            #change the switch
            self.boolReinforcementEditor = False
        self.reEditor.remove_view()
        if not self.csEditor.containsView:
            self.csEditor.add_view()
        self.content.remove_widget(self.view)
        self.content.add_widget(self.csEditor)
        self.view = self.csEditor

    '''
    show the reinforcement-editor
    '''

    def show_reinforcement_editor(self):
        #if the reinforcement-editor has not been created
        if self.boolReinforcementEditor:
            self.create_reinforcement_editor()
            #change the switch
            self.boolReinforcementEditor = False
        self.csEditor.remove_view()
        if not self.reEditor.containsView:
            self.reEditor.add_view()
        self.content.remove_widget(self.view)
        self.content.add_widget(self.reEditor)
        self.view = self.reEditor
    
    '''
    show the strain-stress-explorer
    '''
        
    def show_explorer(self):
        #if the explorer has not been created
        if self.boolExplorer:
            self.create_explorer()
            #change the switch
            self.boolExplorer = False
        self.csEditor.remove_view()
        self.content.remove_widget(self.view)
        self.content.add_widget(self.explorer)
        self.update_explorer()
        self.explorer.update_explorer()
        self.view = self.explorer
    
    '''
    show the mxn-emelope
    '''
    def show_mxnEmelope(self):
        #if the mxn-envelope has not been created
        if self.boolMXNEnvelope:
            self.create_mxnEnvelope()
            #change the switch
            self.boolMXNEnvelope = False
        self.csEditor.remove_view()
        self.content.remove_widget(self.view)
        self.content.add_widget(self.mxnEmelope)
        self.view = self.mxnEmelope
        self.update_explorer()
        self.mxnEmelope.calculation()
        
    '''
    update the cross-section-information of the explorer
    '''
        
    def update_explorer(self):
        if self.csEditor.csShape == self.cs.csDoubleT:
            self.explorer.update_csShape(self.cs.csDoubleT,
                                         self.cs.csDoubleT.get_total_height(),
                                         self.cs.csDoubleT.layers, self.cs.csDoubleT.bars)
        elif self.csEditor.csShape == self.cs.csCircle:
            self.explorer.update_csShape(self.cs.csCircle, self.cs.csCircle.d,
                                         self.cs.csCircle.layers, self.cs.csCircle.bars)
        elif self.csEditor.csShape == self.cs.csRectangle:
            self.explorer.update_csShape(self.cs.csRectangle, self.cs.csRectangle.ch,
                                         self.cs.csRectangle.layers, self.cs.csRectangle.bars)
        elif self.csEditor.csShape == self.cs.csT:
            self.explorer.update_csShape(self.cs.csT, self.cs.csT.get_total_height(),
                                         self.cs.csT.layers, self.cs.csT.bars)
'''
starts the application
'''
            
if __name__ == '__main__':
    MXNApp().run()
