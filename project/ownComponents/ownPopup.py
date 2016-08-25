'''
Created on 27.07.2016

@author: mkennert
'''

from kivy.uix.popup import Popup

from ownComponents.design import Design


class OwnPopup(Popup):
    
    '''
    ownpopup has properties for the color.
    this class make sure, that the popups in the application
    has the same properties and make it easier to change popup-properties
    '''
    
    background_color_normal = Design.foregroundColor
    def __init__(self, **kwargs):
        super(OwnPopup, self).__init__(**kwargs)
        self.background='(1,1,1,1)'
        self.title_color=self.background_color_normal
