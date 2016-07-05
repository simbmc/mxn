'''
Created on 14.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from crossSection.cs import CrossSection
from designClass.design import Design
from materialEditor.editor import MaterialEditor
from crossSectionEditor.editor import CrossSectionEditor
from reinforcementEditor.editor import ReinforcementEditor


Window.size = (900, 600)
#Window.clearcolor = (1, 1, 1, 1)


class MainWindow(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 1
        self.btnSize = Design.btnSize
        self.crossSection = CrossSection()
        self.csShape = self.crossSection.get_cs_rectangle()
        # Cross Section is the default view
        self.content = self.crossSection
        self.create_popup()
        self.create_menu_bar()
        self.create_componets()

    '''
    create all components of the Scrollview root
    '''

    def create_componets(self):
        self.create_material_editor()
        self.create_reinforcement_editor()
        self.create_cross_section_editor()

    '''
    create the list_view. here you can add more menu-options for the app
    '''

    def create_list_view(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        # cross section editor
        csEditor = Button(text='cross section editor',
                          size_hint_y=None, height=self.btnSize)
        csEditor.bind(on_press=self.show_cross_section_editor)
        layout.add_widget(csEditor)
        # reEditor
        reEditor = Button(text='reinforcement editor',
                          size_hint_y=None, height=self.btnSize)
        reEditor.bind(on_press=self.show_reinforcement_editor)
        layout.add_widget(reEditor)
        # material-editor
        me = Button(
            text='material editor', size_hint_y=None, height=self.btnSize)
        me.bind(on_press=self.show_material_editor)
        layout.add_widget(me)
        ##################################################################
        #Here you can add more menu-parts                                #
        #Attention: it's necessary that the button have the follow       #
        #properties: size_hint_y=None, height=40                         #
        ##################################################################
        self.root = ScrollView()
        self.root.add_widget(layout)

    '''
    create the popup with the menu options
    '''

    def create_popup(self):
        self.create_list_view()
        self.popup = Popup(title='Menu', content=self.root, size_hint=(None, None), size=(
            300, 400), pos_hint=({'x': 0, 'top': 1}), pos=(0, 0))

    '''
    create the menu bar where you can select the 
    menu button to show the menu
    '''

    def create_menu_bar(self):
        bar = GridLayout(cols=3, row_force_default=True,
                         row_default_height=self.btnSize, size_hint_y=None, height=self.btnSize)
        menuButton = Button(
            text='menu', size_hint_y=None, height=self.btnSize, size_hint_x=None, width=100)
        menuButton.bind(on_press=self.popup.open)
        bar.add_widget(menuButton)
        self.add_widget(bar)

    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.materialEditor = MaterialEditor()
        # sign in by the cross section
        self.materialEditor.set_cross_section(self.crossSection)

    '''
    create the cross section-editor
    '''

    def create_cross_section_editor(self):
        self.csEditor = CrossSectionEditor()
        self.csEditor.set_cross_section(self.crossSection)
        self.csEditor.add_view()
        self.add_widget(self.csEditor)
        self.content = self.csEditor

    '''
    create the reinforcement-editor
    '''

    def create_reinforcement_editor(self):
        self.reEditor = ReinforcementEditor()
        self.reEditor.set_cross_section(self.crossSection)
        # self.reEditor.add_view(self.csShape.view)

    ##########################################################################
    #Attention:When you want write a new show-method than you must make sure    #
    #that actually component is remove from the widget and set                  #
    #the content to the showed component                                        #
    ##########################################################################

    '''
    show the material-editor
    '''

    def show_material_editor(self, btn):
        self.remove_widget(self.content)
        self.add_widget(self.materialEditor)
        self.content = self.materialEditor
        self.popup.dismiss()

    '''
    show the crossSection editor
    '''

    def show_cross_section_editor(self, btn):
        self.reEditor.remove_view()
        if not self.csEditor.containsView:
            self.csEditor.add_view()
        self.remove_widget(self.content)
        self.add_widget(self.csEditor)
        self.content = self.csEditor
        self.popup.dismiss()

    '''
    show the reinforcement-editor
    '''

    def show_reinforcement_editor(self, btn):
        self.csEditor.remove_view()
        if not self.reEditor.containsView:
            self.reEditor.add_view()
        self.remove_widget(self.content)
        self.add_widget(self.reEditor)
        self.content = self.reEditor
        self.popup.dismiss()

class CSIApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    CSIApp().run()
