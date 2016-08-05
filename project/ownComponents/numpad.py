'''
Created on 01.03.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.ownLabel import OwnLabel


class Numpad(GridLayout):
    '''
    the class keyboard was developed to give the user the possibility
    to input a value
    '''
    # construktor

    def __init__(self, **kwargs):
        super(Numpad, self).__init__(**kwargs)
        self.cols=1
        self.btnHeight = Design.btnHeight
        self.sign=False
    '''
    the method create_numfield create the gui
    of the numpad
    '''

    def create_numfield(self):
        self.lblTextinput = OwnLabel(text='')
        if self.sign:
            display=GridLayout(cols=2, spacing=Design.spacing)
            self.btnSign=Button(text='+',size_hint_y=None, height=self.btnHeight)
            self.btnSign.bind(on_press=self.set_sign)
            display.add_widget(self.btnSign)
        else:
            display=GridLayout(cols=1)
        display.add_widget(self.lblTextinput)
        self.numfieldLayout = GridLayout(cols=3)
        for i in range(1, 10):
            cur = Button(text=str(i))
            cur.bind(on_press=self.appending)
            self.numfieldLayout.add_widget(cur)
        btnDot = Button(text='.')
        btnDot.bind(on_press=self.appending)
        self.numfieldLayout.add_widget(btnDot)
        btnZero = Button(text='0')
        btnZero.bind(on_press=self.appending)
        btnDelete = Button(text='<<')
        btnDelete.bind(on_press=self.delete)
        self.numfieldLayout.add_widget(btnZero)
        self.numfieldLayout.add_widget(btnDelete)
        cur = GridLayout(cols=1)
        layout = GridLayout(cols=2, spacing=Design.spacing,
                            row_force_default=True,
                            row_default_height=self.btnHeight)
        btnOK = Button(text='ok', size_hint_y=None, height=self.btnHeight)
        btnOK.bind(on_press=self.finished)
        btnCancel = Button(
            text='cancel', size_hint_y=None, height=self.btnHeight)
        btnCancel.bind(on_press=self.cancel)
        layout.add_widget(btnOK)
        layout.add_widget(btnCancel)
        cur.add_widget(layout)
        cur.add_widget(display)
        self.add_widget(cur)
        self.add_widget(self.numfieldLayout)
    
    def set_sign(self,btn):
        if self.btnSign.text=='+':
            self.btnSign.text='-'
        else:
            self.btnSign.text='+'
    
    '''
    the method appending appends the choosen digit at the end.
    the method is called when the user use the keyboard
    '''

    def appending(self, button):
        self.lblTextinput.text += button.text

    '''
    the method delete delete the digit at the end.
    the method is called when the press the button '<<'
    '''

    def delete(self, button):
        self.lblTextinput.text = self.lblTextinput.text[:-1]

    '''
    the method reset_text reset the text of the label
    the method must be called from the developer when
    the text must be deleted
    '''

    def reset_text(self):
        self.lblTextinput.text = ''

    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method finished_numpad
    '''
    def sign_in_parent(self, parent):
        self.p = parent
        self.create_numfield()

    '''
    the method finished close the popup when the user
    is finished and made a correctly input
    '''

    def finished(self, button):
        #try to cast the string in a floatnumber
        try:
            #its not allowed that the value 
            #is 0
            x=float(self.lblTextinput.text)
            if self.sign:
                if self.btnSign.text=='-':
                    self.lblTextinput.text='-'+self.lblTextinput.text
            if x>0:
                self.p.finished_numpad()
            self.reset_text()
        #if the value is not a float
        #the lblTextinput will be reset
        except ValueError:
            self.reset_text()

    '''
    cancel the numpad input
    '''

    def cancel(self, btn):
        self.p.close_numpad()
        self.reset_text()
