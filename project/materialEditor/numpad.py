'''
Created on 01.03.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from designClass.design import Design


class Numpad(GridLayout):
    #Construktor
    def __init__(self, **kwargs):
        super(Numpad, self).__init__(**kwargs)
        self.btnSize = Design.btnSize
        self.createNumfield()
        self.cols=1
        self.add_widget(self.layout)
        self._parent=None
    
    '''
    the method createNumfield create the gui
    of the numpad
    '''
    def createNumfield(self):
        self.textinput=Label(text='')
        self.layout=GridLayout(cols=1)
        self.numfield=GridLayout(cols=3)
        for i in range(1,10):
            cur=Button(text=str(i))
            cur.bind(on_press=self.appending)
            self.numfield.add_widget(cur)
        btnDot=Button(text='.')
        btnDot.bind(on_press=self.appending)
        self.numfield.add_widget(btnDot)
        btnZero=Button(text='0')
        btnZero.bind(on_press=self.appending)
        btnDelete=Button(text='<<')
        btnDelete.bind(on_press=self.delete)
        self.numfield.add_widget(btnZero)
        self.numfield.add_widget(btnDelete)
        cur=GridLayout(cols=1)
        layout=GridLayout(cols=2,spacing=10)
        btnOK=Button(text='ok',size_hint_y=None, height=self.btnSize)
        btnOK.bind(on_press=self.finished)
        btnCancel=Button(text='cancel',size_hint_y=None, height=self.btnSize)
        btnCancel.bind(on_press=self.cancel)
        layout.add_widget(btnOK)
        layout.add_widget(btnCancel)
        cur.add_widget(layout)
        cur.add_widget(self.textinput)
        self.layout.add_widget(cur)
        self.layout.add_widget(self.numfield)
    
    '''
    the method appending appends the choosen digit at the end.
    the method is called when the user use the keyboard
    '''
    def appending(self,button): 
        self.textinput.text+=button.text
    
    '''
    the method delete delete the digit at the end.
    the method is called when the press the button '<<'
    '''
    def delete(self,button):
        self.textinput.text=self.textinput.text[:-1]
    
    '''
    the method resetText reset the text of the label
    the method must be called from the developer when
    the text must be deleted
    '''
    def resetText(self):
        self.textinput.text=''
    
    '''
    the method signInParent to set the parent of 
    the object. the parent must have the method finishedNumpad
    '''
    def signInParent(self, parent):
        self._parent=parent
    
    '''
    the method finished close the popup when the user
    is finished and press the button 'finished'
    '''
    def finished(self,button):
        if len(self.textinput.text)>0:
            self._parent.finishedNumpad()
        self.resetText()
    
    '''
    cancel the numpad input
    '''
    def cancel(self,btn):
        self._parent.closeNumpad()
        self.resetText()