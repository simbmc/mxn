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
        self.view.set_cross_section(self)

    '''
    set the information of the cross section
    '''

    def set_information(self, information):
        self.information = information
        self.calculate_weight_price()
        self.calculate_strength()
        self.set_cross_section_information()

    '''
    the method set_layer_information update the cross section information
    '''

    def set_cross_section_information(self):
        self.information.update_cross_section_information(
            0, 0, 0)

    '''
    get all the layers
    '''

    def get_layers(self):
        return self.view.get_layers()

    '''
    the method set_height changes the height of the view
    '''

    def set_height(self, value):
        self.view.set_height(value)
        self.ch = value

    '''
    the method set_width change the width of the view
    '''

    def set_width(self, value):
        self.view.set_width(value)
        self.cw = value
    '''
    return the heigth of the shape
    '''

    def get_height(self):
        return self.ch
    '''
    return the width of the shape
    '''

    def get_width(self):
        return self.cw

    '''
    calculate the weight and the price of the cross section
    '''

    def calculate_weight_price(self):
        weight = price = percentOfLayers = 0.
        # go trough all layers and
        # get the weight of them
        for l in self.view.layers:
            cur = l.get_weight()
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
    the method calculate_strength calculate the strength of 
    the crossSection
    '''

    def calculate_strength(self):
        pass
        '''
        strength = 0.
        # cur supremum
        self.minOfMaxstrain = 1e10
        # max strain is necessary for other calculations
        self.maxOfMaxstrain = 0
        percentOfLayers = 0.
        # find the minimum max_strain and the maximum max_strain
        for l in self.view.layers:
            percentOfLayers += l.h / self.ch
            curStrain = l.get_strain()
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

    '''
    sign in by the cross section
    '''

    def sign_parent(self, crossSection):
        self.allCrossSection = crossSection
        self.information = crossSection.get_information()
