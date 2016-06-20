'''
Created on 15.03.2016

@author: mkennert
'''


from kivy.uix.gridlayout import GridLayout
from crossSectionView.rectangleView import CSRectangleView
from shapes.ashape import AShape

'''
the cross_Section was developed to undock the cs_information from the view
'''

class ShapeRectangle(GridLayout, AShape):
    # Constructor

    def __init__(self, **kwargs):
        super(ShapeRectangle, self).__init__(**kwargs)
        self.ch = 0.5
        self.cw = 0.25
        self.concreteDensity = 2300.
        self.concretePrice = 0.065
        self.concreteStiffness = 30000.
        self.concreteStrength = 3.
        self.view = CSRectangleView()
        self.view.set_crossSection(self)

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
    the method setHeight changes the height of the view
    '''

    def setHeight(self, value):
        self.view.setHeight(value)
        self.ch = value

    '''
    the method setWidth change the width of the view
    '''

    def setWidth(self, value):
        self.view.setWidth(value)
        self.cw = value
    '''
    return the heigth of the shape
    '''
    def getHeight(self):
        return self.ch
    '''
    return the width of the shape
    '''
    def getWidth(self):
        return self.cw
    '''
    the method setPercent change the percentage share of the selected materials
    '''

    def setPercent(self, value):
        self.view.setPercent(value)

    '''
    calculate the weight and the price of the cross section
    '''

    def calculateWeightPrice(self):
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
        self.weight = weight
        self.price = price

    '''
    the method calculateStrength calculate the strength of 
    the crossSection
    '''

    def calculateStrength(self):
        strength = 0.
        # cur supremum
        self.minOfMaxstrain = 1e10
        # max strain is necessary for other calculations
        self.maxOfMaxstrain = 0
        percentOfLayers = 0.
        # find the minimum max_strain and the maximum max_strain
        for l in self.view.layers:
            percentOfLayers += l.h / self.ch
            curStrain = l.getStrain()
            # proof whether the curStrain is smaller as the min
            if curStrain < self.minOfMaxstrain:
                self.minOfMaxstrain = curStrain
            # proof whether the curStrain is bigger as the max
            if curStrain > self.maxOfMaxstrain:
                self.maxOfMaxstrain = curStrain
        # if the percentOfLayers is not 1 there is a matrix
        # with concrete as material
        if 1. - percentOfLayers > 0:
            cur_value = self.concreteStrength / self.concreteStiffness
            if self.minOfMaxstrain > cur_value:
                self.minOfMaxstrain = cur_value
            if self.maxOfMaxstrain < cur_value:
                self.maxOfMaxstrain = cur_value
        # calculate the strength
        for l in self.view.layers:
            strength += self.minOfMaxstrain * \
                l.material.stiffness * l.h / self.ch
        if 1. - percentOfLayers > 0:
            strength += self.minOfMaxstrain * \
                (1. - percentOfLayers) * self.concreteStiffness
        self.strength = strength

    
    '''
    sign in by the cross section
    '''
    def signParent(self, crossSection):
        self.allCrossSection = crossSection
        self.information = crossSection.getInformation()
