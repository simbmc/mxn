'''
Created on 12.05.2016

@author: mkennert
'''
from abc import abstractmethod

class AShape:
    
    '''
    AShape is the interface which the shapes must implement. it makes sure,
    that the shapes has the necessary methods, which the other components
    are uses
    '''

    '''
    add a bar
    '''

    def add_bar(self, x, y, material):
        self.view.add_bar(x, y, material)

    '''
    the method add_layer add new materials in the view
    '''

    def add_layer(self, x, y, material):
        self.view.add_layer(x, y, material)
    
    
    def delete_bar(self):
        self.view.delete_bar()
        
    def update_layer_information(self, y, material, csArea):
        self.information.update_layer_information(y, material, csArea)
    
    def update_bar_information(self, x, y, material, csArea):
        self.information.update_bar_information(x, y, material, csArea)
        
    @abstractmethod
    def set_cross_section_information(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def get_total_height(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def get_max_width(self):
        raise NotImplemented('not implemented')
    '''
    calculate the strain of concrete
    '''

    def calculate_strain_of_concrete(self):
        return self.concreteStrength / self.concreteStiffness

    '''
    get all the layers
    '''

    def get_layers(self):
        return self.view.get_layers()

    '''
    show the error message
    '''

    def show_error_message(self):
        self.information.show_error_message()

    '''
    hide the errorMessage
    '''

    def hide_error_message(self):
        self.information.hide_error_message()

    # not finished yet
    def show_edit_area_layer(self):
        self.information.show_edit_layer_area()
    # not finished yet

    def show_edit_bar_area(self):
        self.information.show_edit_bar_area()

    # not finished yet
    def cancel_editing_bar(self):
        self.information.cancel_editing_bar(None)
    # not finished yet

    def cancel_editing_layer(self):
        self.information.cancel_editing_layer(None)

    # not finished yet

    def edit_layer(self, y, material, csArea):
        self.view.edit_layer(y, material, csArea)
    # not finished yet

    def edit_bar(self, x, y, material, csArea):
        self.view.edit_bar(x, y, material, csArea)
