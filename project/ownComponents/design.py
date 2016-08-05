'''
Created on 29.04.2016

@author: mkennert
'''

from kivy.metrics import dp, sp


class Design:
    '''
    the class design contains just attributes for the design
    '''
    # size-properties
    btnHeight = dp(40)
    lblHeight = dp(10)
    barProcent = 70.
    spacing = 5
    font_size=sp(13)
    # color-properties
    focusColor = [0, 0, 0, 1]
    btnColor = [0.1, 0.1, 0.1, 1]
    btnForeground = [1, 1, 1, 1]
    foregroundColor = [0, 0, 0, 1]
