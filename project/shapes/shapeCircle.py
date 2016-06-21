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
        self.view.set_cross_section(self)
    
    '''
    return the radius
    '''
    def get_radius(self):
        return self.r
    '''
    set the information 
    '''

    def set_information(self, information):
        self.information = information
        self.calculate_weight_price()
        self.calculate_strength()
        self.set_cross_section_information()


    '''
    the method add_layer add new materials in the view
    '''

    def add_layer(self, x, y, material):
        self.view.add_layer(x, y, material)

    '''
    the method delete_layer delete the selected materials
    '''

    def delete_layer(self):
        self.view.delete_layer()

    '''
    calculate the strength
    '''

    def calculate_strength(self):
        self.strength = 0.

    '''
    the method set_layer_information update the layer
    after a layer get the focus
    '''

    def set_layer_information(self, name, price, density, stiffness, strength):
        self.information.update_layer_information(
            name, price, density, stiffness, strength)

    '''
    the method set_layer_information update the cross section information
    '''

    def set_cross_section_information(self):
        self.information.update_cross_section_information(
            self.price, self.weight, self.strength)

    '''
    get all the layers
    '''

    def get_layers(self):
        return self.view.get_layers()

    '''
    calculate the weight and the price of the cross section
    '''

    def calculate_weight_price(self):
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
