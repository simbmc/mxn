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


Window.clearcolor = (1, 1, 1, 1)

class AppActionBar(ActionBar):
    '''
    create the Actionbar in the mainMenu with the kv.file screenmixapp
    '''
    pass

class ActionMenu(ActionPrevious):
    '''
    create the ActionMenu in the mainMenu with the kv.file screenmixapp
    '''
    pass


class MXNApp(App):
    
    '''
    Build the application
    '''
    
    # constructor
    def build(self):
        print('build application')
        self.content = GridLayout(cols=1, spacing=Design.spacing)
        bar = AppActionBar()
        self.content.add_widget(bar)
        self.crossSection = CrossSection()
        self.csShape = self.crossSection.csRectangle
        # cross-section-editor is the default view
        # view is the focus-component
        self.view = self.crossSection
        self.create_componets()
        return self.content

    '''
    create all components of the Scrollview root
    '''

    def create_componets(self):
        self.create_material_editor()
        self.create_reinforcement_editor()
        self.create_cross_section_editor()
        self.create_explorer()
        self.create_mxnEmelope()

    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.materialEditor = MaterialEditor(csShape=self.crossSection)

    '''
    create the cross section-editor
    '''

    def create_cross_section_editor(self):
        self.csEditor = CrossSectionEditor(cs=self.crossSection)
        self.csEditor.set_cross_section(self.crossSection)
        self.csEditor.add_view()
        self.content.add_widget(self.csEditor)
        self.view = self.csEditor

    '''
    create the reinforcement-editor
    '''

    def create_reinforcement_editor(self):
        self.reEditor = ReinforcementEditor()
        self.reEditor.set_cross_section(self.crossSection)
    
    '''
    create the explorer where you can see the stress-strain-behavior of the
    cross section
    '''
        
    def create_explorer(self):
        self.explorer = Explorer(csShape=self.csShape, bars=self.csShape.bars,
                                 layers=self.csShape.layers)
        self.crossSection.explorer = self.explorer
    
    '''
    create the mxnEmelope
    '''
    def create_mxnEmelope(self):
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
        self.content.remove_widget(self.view)
        self.content.add_widget(self.materialEditor)
        self.view = self.materialEditor

    '''
    show the crossSection editor
    '''

    def show_cross_section_editor(self):
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
        self.csEditor.remove_view()
        if not self.reEditor.containsView:
            self.reEditor.add_view()
        self.content.remove_widget(self.view)
        self.content.add_widget(self.explorer)
        self.update_explorer()
        self.explorer.update_explorer()
        self.view = self.explorer
    
    '''
    show the mxn-emelope
    '''
    def show_mxnEmelope(self):
        self.csEditor.remove_view()
        if not self.reEditor.containsView:
            self.reEditor.add_view()
        self.content.remove_widget(self.view)
        self.content.add_widget(self.mxnEmelope)
        self.view = self.mxnEmelope
        self.update_explorer()
        self.mxnEmelope.calculation()
        
    '''
    update the cross-section-information of the explorer
    '''
        
    def update_explorer(self):
        if self.csEditor.csShape == self.crossSection.csDoubleT:
            self.explorer.update_csShape(self.crossSection.csDoubleT,
                                         self.crossSection.csDoubleT.get_total_height(),
                                         self.crossSection.csDoubleT.layers, self.crossSection.csDoubleT.bars)
        elif self.csEditor.csShape == self.crossSection.csCircle:
            self.explorer.update_csShape(self.crossSection.csCircle, self.crossSection.csCircle.d,
                                         self.crossSection.csCircle.layers, self.crossSection.csCircle.bars)
        elif self.csEditor.csShape == self.crossSection.csRectangle:
            self.explorer.update_csShape(self.crossSection.csRectangle, self.crossSection.csRectangle.ch,
                                         self.crossSection.csRectangle.layers, self.crossSection.csRectangle.bars)
        elif self.csEditor.csShape == self.crossSection.csT:
            self.explorer.update_csShape(self.crossSection.csT, self.crossSection.csT.get_total_height(),
                                         self.crossSection.csT.layers, self.crossSection.csT.bars)
'''
starts the application
'''
            
if __name__ == '__main__':
    MXNApp().run()
