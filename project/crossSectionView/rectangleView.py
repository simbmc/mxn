'''
Created on 14.03.2016

@author: mkennert
'''


from kivy.garden.graph import Graph, MeshLinePlot
from crossSectionView.aview import AView
from layers.layerRectangle import LayerRectangle
from plot.filled_rect import FilledRect
from designClass.design import Design
from kivy.uix.gridlayout import GridLayout


'''
the class CSRectangleView was developed to show the the cross section,
which has a rectangle shape
'''


class CSRectangleView(GridLayout, AView):
    # Constructor

    def __init__(self, **kwargs):
        super(CSRectangleView, self).__init__(**kwargs)
        self.cols=1
        self.ch = 0.5
        self.cw = 0.25
        self.csShape = None
        self.percent_change = False
        self.layers = []
        self.createGraph()

    '''
    the method createGraph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def createGraph(self):
        self.graph = Graph(
            #background_color = [1, 1, 1, 1],
            border_color = [0,0,0,1],
            #tick_color = [0.25,0.25,0.25,0],
            #_trigger_color = [0,0,0,1],
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.cw, ymin=0, ymax=self.ch)
        self.add_widget(self.graph)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.drawRectangle()
        self.graph.add_plot(self.p)
    '''
    update the graph
    '''
    def updateGraph(self):
        self.graph.remove_plot(self.p)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.drawRectangle()
        self.graph.add_plot(self.p)
    '''
    draw the rectangle
    '''
    def drawRectangle(self):
        h=self.ch/1e3
        w=self.cw/1e3
        return [(w,h),(w,self.ch),(self.cw,self.ch),(self.cw,h),(w,h)]
    

    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.cw
        y = (touch.y - y0) / gh * self.ch
        focus = False  # one is alreay focus
        for l in self.layers:
            if l.mouseWithin(x, y):
                if l.focus == True and self.percent_change:
                    self.percent_change = False
                    self.updateAllGraph()
                    return
                if l.focus == False and focus == False:
                    l.focus = True
                    l.filledRectCs.color = Design.focusColor
                    focus = True
                    info = l.getMaterialInformations()
                    self.csShape.setLayerInformation(info[0], info[1], info[
                        2], info[3], info[4])
            else:
                if l.focus == True:
                    l.focus = False
                    l.filledRectCs.color=l.colors
                    

    '''
    the method addLayer was developed to add new layer at the cross section
    '''

    def addLayer(self, x, y, h, w, material):
        if x+w>self.cw or y+h>self.ch:
            print('case 1:')
            self.csShape.showErrorMessage()
            return
        else:
            print('case 2:')
            self.csShape.hideErrorMessage()
            l = LayerRectangle(x, y, h, w,
                               next(Design.colorcycler))
            l.setMaterial(material)
            l.setMaterial(material)
            filledRectCs = FilledRect(xrange=[x, x+w],
                                      yrange=[y, y + h],
                                      color=l.colors)
            filledRectAck = FilledRect(xrange=[x, x+w],
                                      yrange=[y, y + h],
                                      color=l.colors)
            self.graph.add_plot(filledRectCs)
            l.setFilledRectCs(filledRectCs)
            l.setFilledRectAck(filledRectAck)
            self.layers.append(l)
            self.csShape.calculateStrength()
            self.updateCrossSectionInformation()

    '''
    the method deleteLayer was developed to delete layer from the cross section
    '''

    def deleteLayer(self):
        if len(self.layers)>0:
            for layer in self.layers:
                if layer.focus:
                    layer.filledRectCs.yrange = [0, 0]
                    layer.filledRectAck.yrange = [0, 0]
                    self.layers.remove(layer)
            self.csShape.calculateStrength()
            self.updateCrossSectionInformation()

    '''
    the method updateLayerInformation update the layer information of 
    the view_information
    '''

    def updateLayerInformation(self, name, price, density, stiffness, strength):
        self.csShape.setLayerInformation(
            name, price, density, stiffness, strength)

    '''
    the method updateCrossSectionInformation update the cross section information of 
    the view_information
    '''

    def updateCrossSectionInformation(self):
        self.csShape.calculateWeightPrice()
        self.csShape.setCrossSectionInformation()

    '''
    the method getFreePlaces return the free-places, 
    where is no layer
    '''

    def getFreePlaces(self):
        self.freePlaces = []
        # running index
        y = 0
        # if the cross section contains layers
        if not len(self.layers) == 0:
            while y < self.ch:
                # layerExist is a switch to proofs whether
                # a l exist over the runnning index or not
                layerExist = False
                minValue = self.ch
                for l in self.layers:
                    if l.y >= y and l.y < minValue:
                        layerExist = True
                        minValue = l.y - l.h / 2.
                        nextMinValue = l.y + l.h / 2.
                        # if the running index is equals the min, means that there's no
                        # area
                        if not y == minValue:
                            self.freePlaces.append((y, minValue))
                        y = nextMinValue
                # if no l exist over the running index then that's the last
                # area which is free.
                if not layerExist:
                    self.freePlaces.append((y, self.ch))
                    return self.freePlaces
        # if no l exist,all area of the cross section is free
        else:
            self.freePlaces.append((0, self.ch))
        return self.freePlaces

    ##########################################################################
    #                                Setter && Getter                        #
    ##########################################################################
    '''
    the method setPercent change the percent shape of the selected rectangle
    '''

    def setPercent(self, value):
        self.percent_change = True
        for rectangle in self.layers:
            if rectangle.focus:
                rectangle.setHeight(self.ch * value)
                rectangle.setPercentage(value)
                self.updateAllGraph()
                self.csShape.calculateStrength()
                self.updateCrossSectionInformation()
                return

    '''
    the method setHeight change the height of the cross section shape
    and update the layers
    '''

    def setHeight(self, value):
        for l in self.layers:
            l.setYCoordinate(l.y / self.ch * value)
            l.setHeight(l.h / self.ch * value)
            self.updateAllGraph()
        self.ch = value
        self.graph.ymax = self.ch
        self.updateCrossSectionInformation()
        self.updateGraph()

    '''
    the method setWidth change the width of the cross section shape
    and update the layers
    '''

    def setWidth(self, value):
        self.cw = value
        self.graph.xmax = self.cw
        for rectangle in self.layers:
            rectangle.setWidth(value)
        self.updateCrossSectionInformation()
        self.updateGraph()

    '''
    the method set_crossSection was developed to say the view, 
    which cross section should it use
    '''

    def set_crossSection(self, cs):
        self.csShape = cs

    '''
    return all layers 
    '''

    def getLayers(self):
        return self.layers
