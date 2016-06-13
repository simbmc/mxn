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

from ackModel.ack import Ack
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
        self.csShape = self.crossSection.getCSRectangle()
        # Cross Section is the default view
        self.content = self.crossSection
        self.createPopup()
        self.createMenuBar()
        self.createComponets()

    '''
    create all components of the Scrollview root
    '''

    def createComponets(self):
        self.createAckView()
        self.createMaterialEditor()
        self.createReinforcementEditor()
        self.createCrossSectionEditor()

    '''
    create the list_view. here you can add more menu-options for the app
    '''

    def createListView(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        # cross section editor
        csEditor = Button(text='cross section editor',
                          size_hint_y=None, height=self.btnSize)
        csEditor.bind(on_press=self.showCrossSectionEditor)
        layout.add_widget(csEditor)
        # reEditor
        reEditor = Button(text='reinforcement editor',
                          size_hint_y=None, height=self.btnSize)
        reEditor.bind(on_press=self.showReinforcementEditor)
        layout.add_widget(reEditor)
        # ack-view
        ackView = Button(text='ack', size_hint_y=None, height=self.btnSize)
        ackView.bind(on_press=self.showAckView)
        layout.add_widget(ackView)
        # material-editor
        me = Button(
            text='material editor', size_hint_y=None, height=self.btnSize)
        me.bind(on_press=self.showMaterialEditor)
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

    def createPopup(self):
        self.createListView()
        self.popup = Popup(title='Menu', content=self.root, size_hint=(None, None), size=(
            300, 400), pos_hint=({'x': 0, 'top': 1}), pos=(0, 0))

    '''
    create the menu bar where you can select the 
    menu button to show the menu
    '''

    def createMenuBar(self):
        bar = GridLayout(cols=3, row_force_default=True,
                         row_default_height=self.btnSize, size_hint_y=None, height=self.btnSize)
        menuButton = Button(
            text='menu', size_hint_y=None, height=self.btnSize, size_hint_x=None, width=100)
        menuButton.bind(on_press=self.popup.open)
        bar.add_widget(menuButton)
        self.add_widget(bar)

    '''
    create the ask_view
    '''

    def createAckView(self):
        self.ackView = Ack()
        self.csShape.setAck(self.ackView)
        # sign in by the cross section
        self.ackView.set_crossSection(self.csShape)

    '''
    create the material-editor
    '''

    def createMaterialEditor(self):
        self.materialEditor = MaterialEditor()
        # sign in by the cross section
        self.materialEditor.set_crossSection(self.crossSection)

    '''
    create the cross section-editor
    '''

    def createCrossSectionEditor(self):
        self.csEditor = CrossSectionEditor()
        self.csEditor.set_crossSection(self.crossSection)
        self.csEditor.addView()
        self.add_widget(self.csEditor)
        self.content = self.csEditor

    '''
    create the reinforcement-editor
    '''

    def createReinforcementEditor(self):
        self.reEditor = ReinforcementEditor()
        self.reEditor.set_crossSection(self.crossSection)
        # self.reEditor.addView(self.csShape.view)

    ##########################################################################
    #Attention:When you want write a new show-method than you must make sure    #
    #that actually component is remove from the widget and set                  #
    #the content to the showed component                                        #
    ##########################################################################

    '''
    show the ack-view
    '''

    def showAckView(self, button):
        self.ackView.update()
        self.remove_widget(self.content)
        self.add_widget(self.ackView)
        self.content = self.ackView
        self.ackView.update()
        self.popup.dismiss()

    '''
    show the material-editor
    '''

    def showMaterialEditor(self, btn):
        self.remove_widget(self.content)
        self.add_widget(self.materialEditor)
        self.content = self.materialEditor
        self.popup.dismiss()

    '''
    show the crossSection editor
    '''

    def showCrossSectionEditor(self, btn):
        self.reEditor.removeView()
        if not self.csEditor.containsView:
            self.csEditor.addView()
        self.remove_widget(self.content)
        self.add_widget(self.csEditor)
        self.content = self.csEditor
        self.popup.dismiss()

    '''
    show the reinforcement-editor
    '''

    def showReinforcementEditor(self, btn):
        self.csEditor.removeView()
        if not self.reEditor.containsView:
            self.reEditor.addView()
        self.remove_widget(self.content)
        self.add_widget(self.reEditor)
        self.content = self.reEditor
        self.popup.dismiss()


class CSIApp(App):

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    CSIApp().run()
