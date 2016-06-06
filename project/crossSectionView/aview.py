'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod


class AView(object):
    @abstractmethod
    def setPercent(self, value):
        raise NotImplemented('not implemented')

    @abstractmethod
    def addLayer(self, percent, material):
        raise NotImplemented('not implemented')

    @abstractmethod
    def deleteLayer(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def updateLayerInformation(self, name, price, density, stiffness, strength, percent):
        raise NotImplemented('not implemented')

    @abstractmethod
    def createGraph(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def on_touch_move(self, touch):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def on_touch_down(self, touch):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def setCrossSection(self, cs):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def updateAllGraph(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def updateCrossSectionInformation(self):
        raise NotImplemented('not implemented')