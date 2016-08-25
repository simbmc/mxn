'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod

class AView(object):

    @abstractmethod
    def add_layer(self, x, y, material):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def add_bar(self, x, y, material):
        raise NotImplemented('not implemented')

    @abstractmethod
    def create_graph(self):
        raise NotImplemented('not implemented')
    
    '''
    the method update_layer_information update the layer information of 
    the view_information
    '''

    def update_layer_information(self, name, price, density, stiffness, strength):
        self.csShape.set_layer_information(name, price, density, stiffness, strength)
