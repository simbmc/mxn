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
from reinforcementEditor.editor import ReinforcementEditor


Window.clearcolor = (1, 1, 1, 1)

'''
create the Actionbar in the mainMenu with the kv.file screenmixapp
'''
class AppActionBar(ActionBar):
    pass

'''
create the ActionMenu in the mainMenu with the kv.file screenmixapp
'''
class ActionMenu(ActionPrevious):
    pass


class MXNApp(App):
    '''
    Build the application
    '''
    # constructor
    def build(self):
        self.content = GridLayout(cols=1, spacing=Design.spacing)
        bar = AppActionBar()
        self.content.add_widget(bar)
        self.crossSection = CrossSection()
        self.csShape = self.crossSection.csRectangle
        # cross-section-editor is the default view
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


    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.materialEditor = MaterialEditor()
        self.materialEditor.set_cross_section(self.crossSection)

    '''
    create the cross section-editor
    '''

    def create_cross_section_editor(self):
        self.csEditor = CrossSectionEditor()
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
starts the application
'''
if __name__ == '__main__':
    MXNApp().run()
