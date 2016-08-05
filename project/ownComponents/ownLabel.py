'''
Created on 27.07.2016

@author: mkennert
'''
from kivy.uix.label import Label
from ownComponents.design import Design


class OwnLabel(Label):
    '''
    ownlabel has properties for the color and the size.
    this class make sure, that the labels in the application
    has the same properties and make it easier to change lbl-properties
    '''
    background_color_normal = Design.foregroundColor
    
    def __init__(self, **kwargs):
        super(OwnLabel, self).__init__(**kwargs)
        self.color = self.background_color_normal
        self.size_hint=(1.,0.1)
        self.height=Design.lblHeight
        self.font_size = Design.font_size

     
    