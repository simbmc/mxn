'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from crossSectionView.aview import AView
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from layers.layerDoubleT import LayerDoubleT
from plot.filled_rect import FilledRect
from layers.layerRectangle import LayerRectangle


class DoubleTView(AView, GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(DoubleTView, self).__init__(**kwargs)
        AView.__init__(self)
        self.cols = 1
        self.layers = []
    '''
    the method createGraph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def createGraph(self):
        self.deltaX = self.wmax / 10.
        self.deltaY = self.hmax / 50.
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.wmax + self.deltaX,
            ymin=0, ymax=self.hmax + self.deltaY)
        self.add_widget(self.graph)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.drawDoubleT()
        self.graph.add_plot(self.p)

    '''
    draw the double_T
    '''

    def drawDoubleT(self):
        x0 = self.graph.xmax / 2.
        y1 = self.graph.ymax / 1e3
        x1 = x0 - self.bw / 2.
        y2 = y3 = self.bh
        x3 = x1 + self.bw / 2. - self.mw / 2.
        y4 = y3 + self.mh
        x5 = x3 + self.mw / 2. - self.tw / 2.
        y6 = y4 + self.th
        x7 = x5 + self.tw
        x9 = x7 - self.tw / 2. + self.mw / 2.
        x11 = x9 + self.bw / 2. - self.mw / 2.
        return [(x1, y1), (x1, y2), (x3, y2), (x3, y4), (x5, y4), (x5, y6),
                (x7, y6), (x7, y4), (x9, y4), (x9, y3), (x11, y3), (x11, y1), (x1, y1)]

    '''
    update the view when the model has changed
    '''

    def update(self):
        # save old values for the update
        self.obw = self.bw
        self.obh = self.bh
        self.omw = self.mw
        self.omh = self.mh
        self.otw = self.tw
        self.oth = self.th
        self.ohmax = self.hmax
        # get the new values
        self.bh = self.csShape.getHeightBottom()
        self.bw = self.csShape.getWidthBottom()
        self.mh = self.csShape.getHeightMiddle()
        self.mw = self.csShape.getWidthMiddle()
        self.th = self.csShape.getHeightTop()
        self.tw = self.csShape.getWidthTop()
        self.hmax = self.csShape.getHeight()
        self.wmax = self.csShape.getWidth()
        # update graph
        self.updateAllGraph()

    '''
    the method addLayer was developed to add new layer at the cross section
    '''

    def addLayer(self, x, y, h, w, material):
        mid=self.graph.xmax/2.
        #half of the width
        bwh=self.bh/2.
        mwh=self.mh/2.
        twh=self.tw/2.
        if y+h>self.hmax or x<self.deltaX:
            print('case 1')
            self.csShape.showErrorMessage()
        elif (y<self.bh and y+h>self.bh) or (y<self.bh+self.mw and y+h>self.bh+self.mw):
            print('case 2')
            self.csShape.showErrorMessage()
        elif y+h<self.bh and x+w>mid+bwh and x<mid-bwh:
            print('case 3')
            self.csShape.showErrorMessage()
        elif y+h<self.mw+self.bh and x+w>mid+mwh and x<mid-mwh:
            print('case 4')
            self.csShape.showErrorMessage()
        elif y+h<self.hmax and x+w>mid+twh and x<mid-twh:
            print('case 5')
            self.csShape.showErrorMessage()
        else:
            print('case 6')
            self.csShape.hideErrorMessage()
            l = LayerRectangle(x, y, h, w,
                               next(Design.colorcycler))
            l.setMaterial(material)
            filledRectCs = FilledRect(xrange=[x, x + w],
                                      yrange=[y, y + h],
                                      color=l.colors)
            filledRectAck = FilledRect(xrange=[x, x + w],
                                       yrange=[y, y + h],
                                       color=l.colors)
            l.setFilledRectCs(filledRectCs)
            l.setFilledRectAck(filledRectAck)
            self.graph.add_plot(filledRectCs)
            self.layers.append(l)
            self.csShape.calculateStrength()
            self.updateCrossSectionInformation()

    '''
    update the graph and the layers
    '''
    def updateAllGraph(self):
        # update graph
        self.deltaX = self.wmax / 10.
        self.deltaY = self.hmax / 50.
        self.graph.xmax = self.wmax + self.deltaX
        self.graph.ymax = self.hmax + self.deltaY
        self.graph.x_ticks_major = self.graph.xmax / 5.
        self.graph.y_ticks_major = self.graph.ymax / 5.
        self.graph.remove_plot(self.p)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.drawDoubleT()
        self.graph.add_plot(self.p)
        self.updateCrossSectionInformation()

    
    '''
    return the freePlaces, where is no layer of the cross section
    '''

    def getFreePlaces(self):
        return []
        '''
        self.freePlaces = []
        # running index
        y = 0
        h = self.hmax
        # if the cross section contains layers
        if not len(self.layers) == 0:
            # minLayer is the layer nearest at the bottom
            minLayer = self.findLayer()
            if minLayer.r3.yrange == [0, 0]:
                minValue = minLayer.r2.yrange[0]
            else:
                minValue = minLayer.r3.yrange[0]
            nextMinValue = minLayer.getHeight() + minValue
            self.appendLayer(y, minValue)
            y = minLayer.getHeight() + minValue
            while y < h:
                # layerExist is a switch to proofs whether
                # a layer exist over the runnning index or not
                layerExist = False
                minValue = h
                for layer in self.layers:
                    if not layer is minLayer:
                        # the r3 of the layer is not in use
                        if layer.r3.yrange == [0, 0] and layer.r2.yrange[0] >= y and layer.r2.yrange[0] < minValue:
                            layerExist = True
                            minValue = layer.r2.yrange[0]
                            nextMinValue = layer.getHeight() + minValue
                        # the r3 of the layer is in use
                        elif layer.r3.yrange[0] >= y and layer.r3.yrange[0] < minValue:
                            print('case 2')
                            layerExist = True
                            minValue = layer.r3.yrange[0]
                            nextMinValue = layer.getHeight() + minValue
                        # if the running index is equals the min, means that there's no
                        # area
                        if y < minValue:
                            print('y: ' + str(y))
                            print('minValue: ' + str(minValue))
                            if minValue < h:
                                self.appendLayer(y, minValue)
                        y = nextMinValue
                        print('nextvalue: ' + str(y))
                # if no layer exist over the running index then that's the last
                # area which is free.
                if not layerExist:
                    self.appendLayer(y, h)
                    return self.freePlaces
        # if no layer exist,all area of the cross section is free
        else:
            self.appendLayer(0, h)
        return self.freePlaces
        '''

    '''
    append the free layer in the freeplaces
    '''

    def appendLayer(self, y1, y2):
        pass
        '''
        # case 1
        if y1 < self.bh and y2 > self.bh and y2 < self.mh + self.bh:
            self.freePlaces.append([y1, self.bh, self.bw])
            self.freePlaces.append([self.bh, y2, self.mw])
        # case 2
        elif y1 < self.bh and y2 > self.bh:
            self.freePlaces.append([y1, self.bh, self.bw])
            self.freePlaces.append([self.bh, self.mh + self.bh, self.mw])
            self.freePlaces.append([self.bh + self.mh, y2, self.tw])
        # case 3
        elif y1 < self.mh + self.bh and y2 > self.mh + self.bh:
            self.freePlaces.append([y1, self.mh + self.bh, self.mw])
            self.freePlaces.append([self.mh + self.bh, y2, self.tw])
        # case 4
        else:
            if y2 < self.bh:
                self.freePlaces.append([y1, y2, self.bw])
            elif y2 < self.bh + self.mh:
                self.freePlaces.append([y1, y2, self.mw])
            else:
                self.freePlaces.append([y1, y2, self.tw])
        '''
    '''
    return the layer which is nearest at the bottom
    '''

    def findLayer(self):
        pass
        '''
        minY = self.th + self.mh + self.bh
        for layer in self.layers:
            if not layer.r3.yrange == [0, 0]:
                if minY > layer.r3.yrange[0]:
                    minY = layer.r3.yrange[0]
                    ret = layer
                    print('minY: ' + str(minY))
            else:
                if minY > layer.r2.yrange[0]:
                    minY = layer.r2.yrange[0]
                    print('minY: ' + str(minY))
                    ret = layer
        return ret
        '''

    '''
    update the cross section information
    '''

    def updateCrossSectionInformation(self):
        self.csShape.calculateWeightPrice()
        self.csShape.calculateStrength()
        self.csShape.setCrossSectionInformation()

    '''
    delete the selected layer
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
    update the layer information in the information-area
    '''

    def updateLayerInformation(self, name, price, density, stiffness, strength):
        self.csShape.setLayerInformation(name, price, density,
                                         stiffness, strength)

    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        y = (touch.y - y0) / gh * self.hmax
        x = (touch.x - x0) / gw * self.wmax
        for l in self.layers:
            if l.mouseWithin(x, y):
                if l.focus:
                    self.percent_change = False
                    self.updateAllGraph()
                    return
                else:
                    l.focus = True
                    l.filledRectCs.color = Design.focusColor
                    info = l.getMaterialInformations()
                    self.csShape.setLayerInformation(info[0], info[1],
                                                     info[2], info[3], info[4])
            else:
                if l.focus == True:
                    l.focus = False
                    l.filledRectCs.color = l.colors

    '''
    set the cross section
    '''

    def set_crossSection(self, cs):
        self.csShape = cs
        self.bh = self.csShape.getHeightBottom()
        self.bw = self.csShape.getWidthBottom()
        self.mh = self.csShape.getHeightMiddle()
        self.mw = self.csShape.getWidthMiddle()
        self.th = self.csShape.getHeightTop()
        self.tw = self.csShape.getWidthTop()
        self.hmax = self.csShape.getHeight()
        self.wmax = self.csShape.getWidth()
        self.createGraph()
