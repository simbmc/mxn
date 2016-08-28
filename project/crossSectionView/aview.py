'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod

from ownComponents.design import Design


class AView(object):
    
    '''
    AView is a interface which the views must implement. it makes sure,
    that the view has the necessary methods, which the other components
    are use
    '''
    
    #############################################################################
    # the following methods must implemented individual in the class,           #
    # which implements the interface                                            #
    #############################################################################
    
    @abstractmethod
    def add_layer(self, x, y, material):
        # should add a layer to the graph and 
        # safe the layer in the list of the csShape
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def add_bar(self, x, y, material):
        # should add a bar to the graph and 
        # safe the bar in the list of the csShape
        raise NotImplemented('not implemented')

    @abstractmethod
    def create_graph(self):
        # create the graph where you can see the shape of
        # the cross-section
        raise NotImplemented('not implemented')
    
    #############################################################################
    # the following methods must not implemented in the class,                  #
    # which implements the interface                                            #
    #############################################################################
    
    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        if len(self.csShape.layers) > 0:
            print(len(self.csShape.layers))
            for layer in self.csShape.layers:
                if layer.focus:
                    self.csShape.layers.remove(layer)
                    self.graph.remove_plot(layer.line)
                    self.graph.remove_plot(self.focusLine)
    
    '''
    the method delete_bar was developed to delete bars from the cross section
    '''
    def delete_bar(self):
        if len(self.csShape.bars) > 0:
            for bar in self.csShape.bars:
                if bar.focus:
                    self.csShape.bars.remove(bar)
                    self.graph.remove_plot(bar.ellipse)
    
    '''
    give the user the possibility to focus a layer or a bar
    '''
    def touch_reaction(self, x, y , cw, ch):
        # change_bar is a switch
        change_bar = False
        for bar in self.csShape.bars:
            if bar.mouse_within(x, y):
                bar.focus = True
                bar.ellipse.color = Design.focusColor
                self.focusBar = bar
                self.csShape.cancel_editing_layer()
                self.csShape.show_edit_bar_area()
                # x, y, material, csArea
                self.csShape.update_bar_information(bar.x, bar.y, bar.csArea, bar.material)
                change_bar = True
            else:
                bar.ellipse.color = [255, 0, 0]
                bar.focus = False
        # make sure that only one reinforcement can be select
        # at the same time
        if change_bar:
            return
        else:
            self.csShape.cancel_editing_bar()
        oneIsFocused = False
        if x < cw:
            for layer in self.csShape.layers:
                if layer.mouse_within(y, ch / 1e2):
                    layer.focus = True
                    oneIsFocused = True
                    self.lineIsFocused = True
                    self.focusLayer = layer
                    self.csShape.cancel_editing_bar()
                    self.csShape.show_edit_area_layer()
                    self.csShape.update_layer_information(layer.y, layer.h, layer.material)
                    self.focusLine.points = layer.line.points
                    self.graph.add_plot(self.focusLine)
                else:
                    layer.focus = False
        if not oneIsFocused and self.lineIsFocused:
            self.graph.remove_plot(self.focusLine)
            self.csShape.cancel_editing_layer()
