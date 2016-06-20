'''
Created on 12.05.2016

@author: mkennert
'''
from abc import abstractmethod


class AShape:

    def setInformation(self, information):
        self.information = information
        self.calculateWeightPrice()
        self.calculateStrength()
        self.setCrossSectionInformation()

    @abstractmethod
    def setAck(self, ack):
        raise NotImplemented('not implemented')

    @abstractmethod
    def addLayer(self, percent, material):
        raise NotImplemented('not implemented')

    @abstractmethod
    def deleteLayer(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def setLayerInformation(self, name, price, density, stiffness, strength, percent):
        raise NotImplemented('not implemented')

    @abstractmethod
    def setCrossSectionInformation(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def calculateWeightPrice(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def calculateStrength(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def getFreePlaces(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def getHeight(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def getWidth(self):
        raise NotImplemented('not implemented')
    '''
    calculate the strain of concrete
    '''

    def calculateStrainOfConcrete(self):
        return self.concreteStrength / self.concreteStiffness

    '''
    get all the layers
    '''

    def getLayers(self):
        return self.view.getLayers()

    '''
    the method setPercent change the percentage share of the selected materials
    '''

    def setPercent(self, value):
        self.view.setPercent(value)
    
    '''
    show the error message
    '''
    def showErrorMessage(self):
        self.information.showErrorMessage()
    
    '''
    hide the errorMessage
    '''
    def hideErrorMessage(self):
        self.information.hideErrorMessage()