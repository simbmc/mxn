'''
Created on 12.05.2016

@author: mkennert
'''
from abc import abstractmethod

from kivy.properties import ListProperty


class AShape(object):
    
    '''
    AShape is the interface which the shapes must implement. it makes sure,
    that the shapes has the necessary methods, which the other components
    are uses
    '''
    
    # all layers of the cross-section
    layers = ListProperty([])
    
    # all bars of the cross-section
    bars = ListProperty([])
    
    #############################################################################
    # the following methods must implemented individual in the class,           #
    # which implements the interface                                            #
    #############################################################################
    
    @abstractmethod
    def _get_gravity_centre(self):
        # should return the gravity centre of
        # the cross-section-shape
        raise NotImplemented('not implemented')
    
    def get_width(self, y):
        # should return the width by the
        # given y-coordinate
        raise NotImplemented('not implemented')
    
    #############################################################################
    # the following methods must not implemented in the class,                  #
    # which implements the interface                                            #
    #############################################################################
    
    '''
    the method add_layer add new materials in the view
    '''
    def add_layer(self, y, csArea, material):
        self.view.add_layer(y, csArea, material)
    
    '''
    edit the layer with the new values
    '''
    def edit_layer(self, y, csArea, material):
        self.view.edit_layer(y, material, csArea)
     
    '''
    add a bar
    '''
    def add_bar(self, x, y, csArea, material):
        self.view.add_bar(x, y, csArea, material)

    '''
    edit the bar with the new values
    '''
    def edit_bar(self, x, y, csArea, material):
        self.view.edit_bar(x, y, csArea, material)
    
    '''
    update the layer-information when you edit existing layers
    '''
    def update_layer_information(self, y, csArea, material):
        self.information.editLayer.update_layer_information(y, csArea, material)
    
    '''
    update the bar-information when you edit existing bars
    '''
    def update_bar_information(self, x, y, csArea, material):
        self.information.editBar.update_bar_information(x, y, csArea, material)

    '''
    show the error message. this method must be called when the user input wrong
    parameters for the layer or the bar
    '''
    def show_error_message(self):
        self.information.show_error_message()

    '''
    hide the errorMessage
    '''
    def hide_error_message(self):
        self.information.hide_error_message()

    '''
    show the area where you can edit the selected layer
    '''
    def show_edit_area_layer(self):
        self.information.show_add_layer_area(None)
        self.information.editLayer.add = False
    
    '''
    hide the area where you can edit the selected layer
    '''
    def cancel_editing_layer(self):
        self.information.cancel_editing_layer(None)
        
    '''
    show the area where you can edit the selected bar
    '''
    def show_edit_bar_area(self):
        self.information.show_add_bar_area(None)
        self.information.editBar.add = False

    '''
    hide the area where you can edit the selected layer
    '''
    def cancel_editing_bar(self):
        self.information.cancel_editing_bar(None)
