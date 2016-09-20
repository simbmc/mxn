'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

from ownComponents.design import Design
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
from reinforcement.bar import Bar
from reinforcement.layer import Layer


class AView(object):
    
    '''
    AView is a interface which the views must implement. it makes sure,
    that the view has the necessary methods, which the other components
    are use
    '''
    
    # cross-section-shape
    csShape = ObjectProperty()
    
    # line to show that the layer has the focus
    focusLine = LinePlot(width=1.5, color=Design.focusColor)
    
    # boolean whether a line has the focus
    lineIsFocused = BooleanProperty(False)
    
    ylabelStr = StringProperty('cross-section-height [m]')
    
    xlabelStr = StringProperty('cross-section-width [m]')
    
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
    create a layer and add it to the graph and the csShape
    '''
   
    def create_layer(self, y, csArea, w, material, line):
        # hide the error-message in the reinforcement editor
        self.csShape.hide_error_message()
        # create layer
        l = Layer(y, csArea, w)
        l.material, l.line = material, line
        # add the layer to the graph
        self.graph.add_plot(line)
        # add the layer in the layer-list of the cs-shape
        self.csShape.layers.append(l)
    
    '''
    update layer properties
    '''
   
    def update_layer_properties(self, y, material, csArea):
        # hide the error-message in the reinforcement editor
        self.csShape.hide_error_message()
        # edit the layer
        self.focusLayer.y = y
        self.focusLayer.material = material
        self.focusLayer.h = csArea
        # set the points of the focus-line and remove 
        # the line from the graph 
        if self.lineIsFocused:
            self.focusLine.points = self.focusLayer.line.points
            self.graph.remove_plot(self.focusLine)
    
    '''
    delete all reinforcement of the cross-section
    '''
            
    def delete_reinforcement(self):
        #reset the layers and bars of the cross-section
        self.csShape.layers=[]
        self.csShape.bars=[]
        #delete all plots apart from self.p
        while len(self.graph.plots)>1:
            for plot in self.graph.plots:
                if plot!=self.p:
                    self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        
    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        # if the cross-section contains layers
        if len(self.csShape.layers) > 0:
            for layer in self.csShape.layers:
                print(layer)
                if layer.focus:
                    # remove the layer and the line
                    self.csShape.layers.remove(layer)
                    self.graph.remove_plot(layer.line)
                    self.graph.remove_plot(self.focusLine)
    
    '''
    the method delete_bar was developed to delete bars from the cross section
    '''
                    
    def delete_bar(self):
        # if the cross-section contains bars
        if len(self.csShape.bars) > 0:
            for bar in self.csShape.bars:
                if bar.focus:
                    # remove the bar
                    self.csShape.bars.remove(bar)
                    self.graph.remove_plot(bar.ellipse)
                
    '''
    create a bar and add it to the graph and the csShape
    '''
                    
    def create_bar(self, x, y, csArea, material, epsX, epsY):
        # hide the error-message in the reinforcement editor
        self.csShape.hide_error_message()
        # create the bar
        b = Bar(x, y, csArea)
        b.material = material
        plot = FilledEllipse(xrange=[x - epsX, x + epsX], yrange=[y - epsY, y + epsY],
                             color=[255, 0, 0, 1])
        b.ellipse = plot
        # add the plot to the graph and the bar to the 
        # bars in the cross-section-shape
        self.graph.add_plot(plot)
        self.csShape.bars.append(b)
    
    '''
    update the bar-properties
    '''
                    
    def update_bar_properties(self, x, y, csArea, material, epsX, epsY):
        # hide the error-message in the reinforcement editor
        self.csShape.hide_error_message()
        # edit the new position of the bar
        self.focusBar.ellipse.xrange = [x - epsX, x + epsX]
        self.focusBar.ellipse.yrange = [y - epsY, y + epsY]
        # edit the bar-properties
        self.focusBar.x = x
        self.focusBar.y = y
        self.focusBar.material = material
        self.focusBar.csArea = csArea
    
    '''
    give the user the possibility to focus a layer or a bar
    '''
                    
    def touch_reaction(self, x, y , cw, ch):
        #if one bar is focused, it's not necessary
        #to go through the layers
        if self.touch_bar(x, y, cw, ch):
            return
        else:
            self.touch_layer(x, y, cw, ch)
    
    '''
    proofs whether one bar is focused. if one is focused the properties
    will showed in the reinforcement-editor.
    the method returns true, when a bar is focused, else
    return false 
    '''
            
    def touch_bar(self, x, y , cw, ch):
        # change_bar is a switch to recognize that
        # one bar has changed and the layer-loop 
        # doesn't should go through
        change_bar = False
        for bar in self.csShape.bars:
            # proofs whether the coordinates are in the bar
            if bar.mouse_within(x, y):
                bar.focus = True
                bar.ellipse.color = Design.focusColor
                self.focusBar = bar
                self.csShape.cancel_editing_layer()
                self.csShape.show_edit_bar_area()
                # update bar information in the reinforcement-editor
                self.csShape.update_bar_information(bar.x, bar.y, bar.csArea, bar.material)
                change_bar = True
            else:
                bar.ellipse.color = [255, 0, 0]
                bar.focus = False
        # make sure that only one reinforcement can be select
        # at the same time. 
        if change_bar:
            return True
        else:
            return False
    
    '''
    proofs whether one layer is focused. if one is focused the properties
    will showed in the reinforcement-editor.
    '''
       
    def touch_layer(self, x, y , cw, ch):
        # oneIsFocused is a switch to proof whether 
        # one layer has a focus
        oneIsFocused = False
        if x < cw:
            for layer in self.csShape.layers:
                # proofs whether the y-coordinate are in the near enough
                # by the layer
                if layer.mouse_within(y, ch / 2e1):
                    layer.focus = True
                    oneIsFocused = True
                    self.lineIsFocused = True
                    self.focusLayer = layer
                    self.csShape.cancel_editing_bar()
                    self.csShape.show_edit_area_layer()
                    # update layer information in the reinforcement editor
                    self.csShape.update_layer_information(layer.y, layer.h, layer.material)
                    self.focusLine.points = layer.line.points
                    self.graph.add_plot(self.focusLine)
                else:
                    layer.focus = False
        if not oneIsFocused and self.lineIsFocused:
            # when no layer has the focus the focus line
            # and the editing layer must disappear 
            self.graph.remove_plot(self.focusLine)
            self.csShape.cancel_editing_layer()
