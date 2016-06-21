'''
Created on 07.04.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

'''
The class Keyboard was developed to give the user the possibility
to write words with a keyboard. 
the keyboard-object is a popup
'''
class Keyboard(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self.alphabet_small='qwertzuiopasdfghjkl_.yxcvbnm'
        self.create_small_keyboard()
        self.cols=1
        self.add_widget(self.layout)
        self._parent=None
        
    '''
    the method create_small_keyboard create the
    gui of the keyboard
    '''
    def create_small_keyboard(self):
        self.textinput = Label(text='')
        self.layout=GridLayout(cols=1)
        self.layout.add_widget(self.textinput)
        self.smallKeyboard=GridLayout(cols=10)
        for i in range(0,len(self.alphabet_small)):
            cur=Button(text=self.alphabet_small[i])
            cur.bind(on_press=self.appending)
            self.smallKeyboard.add_widget(cur)
        btnDelete=Button(text='<<')
        btnDelete.bind(on_press=self.delete)
        btnFinished=Button(text='ok')
        btnFinished.bind(on_press=self.finished)
        self.smallKeyboard.add_widget(btnDelete)
        self.smallKeyboard.add_widget(btnFinished)
        self.layout.add_widget(self.smallKeyboard)
    '''
    the method appending appends character at the end.
    the method is called when the user use the keyboard
    '''
    def appending(self,button): 
        self.textinput.text+=button.text
    
    '''
    the method delete delete character at the end.
    the method is called when the press the button '<<'
    '''
    def delete(self,button):
        self.textinput.text=self.textinput.text[:-1]
    
    '''
    the method finished close the popup when the user
    is finished and press the button 'ok'
    '''
    def finished(self,button):
        self._parent.finished_keyboard()
    
    '''
    the method reset_text reset the text of the label
    the method must be called from the developer when
    the text must be deleted
    '''
    def reset_text(self):
        self.textinput.text=''
    
    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method finished_keyboard
    '''
    def sign_in_parent(self, parent):
        self._parent=parent
        