'''
Created on 29.04.2016

@author: mkennert
'''
'''
the class design contains just attributes for the design
'''

from itertools import cycle


class Design:
    btnSize=50
    focusColor=[255,255,255]
    colors = [[255, 102, 102], [255, 255, 102], [140, 255, 102], [102, 255, 217],
              [102, 102, 255], [255, 102, 102], [179, 179, 179], [102, 71, 133]]
    colorcycler = cycle(colors)