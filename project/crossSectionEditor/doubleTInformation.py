'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from designClass.design import Design
from materialEditor.numpad import Numpad


class DoubleTInformation(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(DoubleTInformation, self).__init__(**kwargs)
        self.focusBtn=None
        self.cols=2
        self.size_hint_y=None
        self.spacing=10
        self.btnSize=Design.btnSize
    '''
    create the gui
    '''
    def createGui(self):
        self.topWidth=Button(text=str(self.csShape.getWidthTop()),size_hint_y=None, height=self.btnSize)
        self.middleWidth=Button(text=str(self.csShape.getWidthMiddle()),size_hint_y=None, height=self.btnSize)
        self.bottomWidth=Button(text=str(self.csShape.getWidthBottom()),size_hint_y=None, height=self.btnSize)
        self.topHeight=Button(text=str(self.csShape.getHeightTop()),size_hint_y=None, height=self.btnSize)
        self.middleHeight=Button(text=str(self.csShape.getHeightMiddle()),size_hint_y=None, height=self.btnSize)
        self.bottomHeight=Button(text=str(self.csShape.getHeightBottom()),size_hint_y=None, height=self.btnSize)
        self.topWidth.bind(on_press=self.showNumpad)
        self.topHeight.bind(on_press=self.showNumpad)
        self.middleWidth.bind(on_press=self.showNumpad)
        self.middleHeight.bind(on_press=self.showNumpad)
        self.bottomWidth.bind(on_press=self.showNumpad)
        self.bottomHeight.bind(on_press=self.showNumpad)
        self.add_widget(Label(text='top-width'))
        self.add_widget(self.topWidth)
        self.add_widget(Label(text='middle-width'))
        self.add_widget(self.middleWidth)
        self.add_widget(Label(text='bottom-width'))
        self.add_widget(self.bottomWidth)
        self.add_widget(Label(text='top-height'))
        self.add_widget(self.topHeight)
        self.add_widget(Label(text='middle-height'))
        self.add_widget(self.middleHeight)
        self.add_widget(Label(text='bottom-height'))
        self.add_widget(self.bottomHeight)
        self.createPopup()
    
    '''
    set the cross section
    '''
    def setCrossSection(self, cs):
        self.csShape=cs
        self.createGui()
    
    '''
    create the popup
    '''
    def createPopup(self):
        self.numpad=Numpad()
        self.numpad.signInParent(self)
        self.popup=Popup(content=self.numpad)
    
    '''
    close the numpad
    '''
    def closeNumpad(self):
        self.popup.dismiss()
        
    '''
    open the popup
    '''
    def showNumpad(self,btn):
        self.focusBtn=btn
        self.popup.open()
        
    '''
    set the text of the button
    '''
    def finishedNumpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popup.dismiss()
        value=float(self.focusBtn.text)
        if self.focusBtn==self.topHeight:
            self.csShape.setHeightTop(value)
        elif self.focusBtn==self.topWidth:
            self.csShape.setWidthTop(value)
        elif self.focusBtn==self.middleHeight:
            self.csShape.setHeightMiddle(value)
        elif self.focusBtn==self.middleWidth:
            self.csShape.setWidthMiddle(value)
        elif self.focusBtn==self.bottomHeight:
            self.csShape.setHeightBottom(value)
        elif self.focusBtn==self.bottomWidth:
            self.csShape.setWidthBottom(value)