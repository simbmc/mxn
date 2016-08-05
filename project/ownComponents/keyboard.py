'''
Created on 07.04.2016

@author: mkennert
'''

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from ownComponents.ownLabel import OwnLabel


class Keyboard(GridLayout):
    '''
    The class Keyboard was developed to give the user the possibility
    to write words with a keyboard. 
    the keyboard-object is a popup
    '''    
    # constructor

    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self.cols, self.p = 1, None
        self.alphabet = 'qwertzuiopasdfghjkl_.yxcvbnm'
        self.createKeyboard()
        self.add_widget(self.layout)

    '''
    the method createKeyboard create the
    gui of the keyboard
    '''

    def createKeyboard(self):
        self.lblTextinput = OwnLabel(text='')
        self.layout = GridLayout(cols=1)
        self.layout.add_widget(self.lblTextinput)
        self.smallKeyboard = GridLayout(cols=10)
        for i in range(0, len(self.alphabet)):
            cur = Button(text=self.alphabet[i])
            cur.bind(on_press=self.appending)
            self.smallKeyboard.add_widget(cur)
        btnDelete = Button(text='<<')
        btnDelete.bind(on_press=self.delete)
        btnFinished = Button(text='ok')
        btnFinished.bind(on_press=self.finished)
        self.smallKeyboard.add_widget(btnDelete)
        self.smallKeyboard.add_widget(btnFinished)
        self.layout.add_widget(self.smallKeyboard)
    '''
    the method appending appends character at the end.
    the method is called when the user use the keyboard
    '''

    def appending(self, button):
        self.lblTextinput.text += button.text

    '''
    the method delete delete character at the end.
    the method is called when the press the button '<<'
    '''

    def delete(self, button):
        self.lblTextinput.text = self.lblTextinput.text[:-1]

    '''
    the method finished close the popup when the user
    is finished and press the button 'ok'
    '''

    def finished(self, button):
        if len(self.lblTextinput.text)>0:
            self.p.finished_keyboard()

    '''
    the method reset_text reset the text of the label
    the method must be called from the developer when
    the text must be deleted
    '''

    def reset_text(self):
        self.lblTextinput.text = ''

    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method finishedKeyboard
    '''

    def sign_in_parent(self, parent):
        self.p = parent
