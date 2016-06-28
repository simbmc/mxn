'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod

from designClass.design import Design


class AView(object):

    @abstractmethod
    def add_layer(self,x,y, material):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def add_bar(self,x,y, material):
        raise NotImplemented('not implemented')

    @abstractmethod
    def delete_layer(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def update_layer_information(self, name, price, density, stiffness, strength, percent):
        raise NotImplemented('not implemented')

    @abstractmethod
    def create_graph(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def set_cross_section(self, cs):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def update_cross_section_information(self):
        raise NotImplemented('not implemented')
    
    