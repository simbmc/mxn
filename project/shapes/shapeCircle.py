'''
Created on 13.06.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from shapes.ashape import AShape
from crossSectionView.circleView import CSCircleView


class ShapeCircle(GridLayout, AShape):
    # Constructor

    def __init__(self, **kwargs):
        super(ShapeCircle, self).__init__(**kwargs)
        self.r = 0.25
        self.concreteDensity = 2300.
        self.concretePrice = 0.065
        self.concreteStiffness = 30000.
        self.concreteStrength = 3.
        self.view = CSCircleView()
        self.view.set_crossSection(self)
    
    '''
    return the radius
    '''
    def getRadius(self):
        return self.r
    '''
    set the information 
    '''

    def setInformation(self, information):
        self.information = information
        self.calculateWeightPrice()
        self.calculateStrength()
        self.setCrossSectionInformation()

    '''
    the method set_crossSection was developed to say the view, 
    which cross section should it use
    '''

    def setAck(self, ack):
        self.ack = ack

    '''
    the method addLayer add new materials in the view
    '''

    def addLayer(self, x, y, h, w, material):
        self.view.addLayer(x, y, h, w, material)

    '''
    the method deleteLayer delete the selected materials
    '''

    def deleteLayer(self):
        self.view.deleteLayer()

    '''
    calculate the strength
    '''

    def calculateStrength(self):
        self.strength = 0.

    '''
    the method setLayerInformation update the layer
    after a layer get the focus
    '''

    def setLayerInformation(self, name, price, density, stiffness, strength):
        self.information.updateLayerInformation(
            name, price, density, stiffness, strength)

    '''
    the method setLayerInformation update the cross section information
    '''

    def setCrossSectionInformation(self):
        self.information.updateCrossSectionInformation(
            self.price, self.weight, self.strength)

    '''
    get all the layers
    '''

    def getLayers(self):
        return self.view.getLayers()

    '''
    calculate the weight and the price of the cross section
    '''

    def calculateWeightPrice(self):
        '''
        weight = price = percentOfLayers = 0.
        # go trough all layers and
        # get the weight of them
        for l in self.view.layers:
            cur = l.getWeight()
            weight += cur
            price += cur * l.material.price
            percentOfLayers += l.h / self.ch
        # if the percentOfLayers is not 1 there is a matrix
        # with concrete as material
        weight += (1 - percentOfLayers) * self.cw * self.concreteDensity
        price += (1 - percentOfLayers) * self.ch * \
            self.cw * self.concretePrice
        '''
        self.weight = 0.
        self.price = 0
