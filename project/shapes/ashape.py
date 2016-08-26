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
    
    '''
    update the layer-information when you edit existing layers
    '''
    def update_layer_information(self, y, material, csArea):
        self.information.update_layer_information(y, material, csArea)
    
    '''
    update the bar-information when you edit existing bars
    '''
    def update_bar_information(self, x, y, material, csArea):
        self.information.update_bar_information(x, y, material, csArea)

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
        self.information.show_edit_layer_area()
    
    '''
    hide the area where you can edit the selected layer
    '''
    def cancel_editing_layer(self):
        self.information.cancel_editing_layer(None)
        
    '''
    show the area where you can edit the selected bar
    '''
    def show_edit_bar_area(self):
        self.information.show_edit_bar_area()

    '''
    hide the area where you can edit the selected layer
    '''
    def cancel_editing_bar(self):
        self.information.cancel_editing_bar(None)

    '''
    edit the layer with the new values
    '''
    def edit_layer(self, y, material, csArea):
        self.view.edit_layer(y, material, csArea)
    
    '''
    edit the bar with the new values
    '''
    def edit_bar(self, x, y, material, csArea):
        self.view.edit_bar(x, y, material, csArea)
