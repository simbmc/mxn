'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from crossSectionView.doubleTView import DoubleTView
from shapes.ashape import AShape


class ShapeDoubleT(GridLayout, AShape):
    # Constructor

    def __init__(self, **kwargs):
        super(ShapeDoubleT, self).__init__(**kwargs)
        self.cols = 2
        # toparea
        self.tw = 0.3
        self.th = 0.2
        # middlearea
        self.mw = 0.1
        self.mh = 0.25
        # bottomarea
        self.bw = 0.3
        self.bh = 0.2
        self.view = DoubleTView()
        self.view.csShape=self
        self.view.create_graph()

    '''
    return the top-width
    '''

    def get_width_top(self):
        return self.tw

    '''
    set the top-width
    '''

    def set_width_top(self, value):
        self.tw = value
        self.view.update()

    '''
    return the top-height
    '''

    def get_height_top(self):
        return self.th

    '''
    set the top-height
    '''

    def set_height_top(self, value):
        self.th = value
        self.view.update()

    '''
    set the middle-width
    '''

    def set_width_middle(self, value):
        self.mw = value
        self.view.update()
    '''
    return the middle-width
    '''

    def get_width_middle(self):
        return self.mw

    '''
    return the middle-height
    '''

    def get_height_middle(self):
        return self.mh

    '''
    set the middle-height
    '''

    def set_height_middle(self, value):
        self.mh = value
        self.view.update()

    '''
    set the bottom-height
    '''

    def set_height_bottom(self, value):
        self.bh = value
        self.view.update()

    '''
    return the bottom-height
    '''

    def get_height_bottom(self):
        return self.bh

    '''
    set the bottom-width
    '''

    def set_width_bottom(self, value):
        self.bw = value
        self.view.update()

    '''
    return the bottom-width
    '''

    def get_width_bottom(self):
        return self.bw

    '''
    return the cs-height
    '''

    def get_height(self):
        return self.th + self.bh + self.mh

    '''
    return the max-width
    '''

    def get_width(self):
        wmax = self.tw
        if wmax < self.mw:
            wmax = self.mw
        if wmax < self.bw:
            wmax = self.bw
        return wmax

    '''
    set the cs-information
    '''

    def set_information(self, information):
        self.information = information

