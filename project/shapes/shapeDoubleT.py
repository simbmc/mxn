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
        self.concreteDensity = 2300.
        self.concretePrice = 0.065
        self.concreteStiffness = 30000.
        self.concreteStrength = 3.
        self.view = DoubleTView()
        self.view.setCrossSection(self)

    '''
    return the top-width
    '''

    def getWidthTop(self):
        return self.tw

    '''
    set the top-width
    '''

    def setWidthTop(self, value):
        self.tw = value
        self.view.update()

    '''
    return the top-height
    '''

    def getHeightTop(self):
        return self.th

    '''
    set the top-height
    '''

    def setHeightTop(self, value):
        self.th = value
        self.view.update()

    '''
    set the middle-width
    '''

    def setWidthMiddle(self, value):
        self.mw = value
        self.view.update()
    '''
    return the middle-width
    '''

    def getWidthMiddle(self):
        return self.mw

    '''
    return the middle-height
    '''

    def getHeightMiddle(self):
        return self.mh

    '''
    set the middle-height
    '''

    def setHeightMiddle(self, value):
        self.mh = value
        self.view.update()

    '''
    set the bottom-height
    '''

    def setHeightBottom(self, value):
        self.bh = value
        self.view.update()

    '''
    return the bottom-height
    '''

    def getHeightBottom(self):
        return self.bh

    '''
    set the bottom-width
    '''

    def setWidthBottom(self, value):
        self.bw = value
        self.view.update()

    '''
    return the bottom-width
    '''

    def getWidthBottom(self):
        return self.bw

    '''
    return the cs-height
    '''

    def getHeight(self):
        return self.th + self.bh + self.mh

    '''
    return the max-width
    '''

    def getWidth(self):
        wmax = self.tw
        if wmax < self.mw:
            wmax = self.mw
        if wmax < self.bw:
            wmax = self.bw
        return wmax

    '''
    set the cs-information
    '''

    def setInformation(self, information):
        self.information = information

    '''
    set the ack
    '''

    def setAck(self, ack):
        self.ack=ack

    '''
    the method addLayer add new materials in the view
    '''

    def addLayer(self, percent, material):
        self.view.addLayer(percent, material)

    '''
    delete the selected layer
    '''

    def deleteLayer(self):
        self.view.deleteLayer()

    '''
    update the layerinformation in the cs-information
    '''

    def setLayerInformation(self, name, price, density, stiffness, strength, percent):
        self.information.updateLayerInformation(
            name, price, density, stiffness, strength, percent)

    '''
    update the cross section information in the cs-information
    '''

    def setCrossSectionInformation(self):
        self.information.updateCrossSectionInformation(self.price, self.weight, self.strength)

    '''
    set the percent
    '''

    def setPercent(self, value):
        self.view.setPercent(value)

    '''
    calculate the weight and price
    '''

    def calculateWeightPrice(self):
        weight=0.
        price=0.
        #go trough all layers and get the weight of them
        for l in self.view.layers:
            cur=l.getWeight()
            weight+=cur
            price+=cur*l.material.price
        #if the percentOfLayers is not 1 there is a matrix
        #with concrete as material
        freeplaces=self.view.getFreePlaces()
        for i in freeplaces:
            cur=(i[1]-i[0])*i[2]*self.concreteDensity
            weight+=cur
            price+=cur*self.concretePrice
        self.weight=weight
        self.price=price

    '''
    calculate the strength of the cross section
    '''

    def calculateStrength(self):
        strength=0.
        #cur supremum
        self.minOfMaxstrain=1e10
        #max strain is necessary for other calculations
        self.maxOfMaxstrain=0
        #find the minimum max_strain and the maximum max_strain
        for l in self.view.layers:
            curStrain=l.getStrain()
            #proof whether the curStrain is smaller as the min
            if curStrain<self.minOfMaxstrain:
                self.minOfMaxstrain=curStrain
            #proof whether the curStrain is bigger as the max
            if curStrain>self.maxOfMaxstrain:
                self.maxOfMaxstrain=curStrain
        #if the percentOfLayers is not 1 there is a matrix
        #with concrete as material
        freePlaces=self.view.getFreePlaces()
        if len(freePlaces)>0:
            curValue=self.concreteStrength/self.concreteStiffness
            if self.minOfMaxstrain>curValue:
                self.minOfMaxstrain=curValue
            if self.maxOfMaxstrain<curValue:
                self.maxOfMaxstrain=curValue
        #calculate the strength
        csSize=self.th*self.tw+self.mw*self.mh+self.bh*self.bw
        for l in self.view.layers:
            strength+=self.minOfMaxstrain*l.material.stiffness*l.getSize()/csSize
        freePlacesSize=0.
        for i in freePlaces:
            freePlacesSize+=(i[1]-i[0])*i[2]
        strength+=self.minOfMaxstrain*freePlacesSize/csSize*self.concreteStiffness
        self.strength=strength
