'''
Created on 25.08.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownButton import OwnButton
from ownComponents.numpad import Numpad
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot
from plot.dashedLine import DashedLine
from materialEditor.materiallist import MaterialList

class Explorer(GridLayout):
    
    '''
    the Explorer is the component which shows the stress-strain.behaviour
    of the selected cross-section-shape
    '''
    
    # important components
    csShape = ObjectProperty()
    layers, bars = ListProperty([]), ListProperty([])
    
    # important strings
    strainStr = StringProperty('strain')
    stressStr = StringProperty('stress')
    lowerStrainStr = StringProperty('lower-strain:')
    upperStrainStr = StringProperty('upper-strain:')
    defaultMinStrain = StringProperty('-0.5')
    defaultMaxStrain = StringProperty('0.5')
    defaultNumber = StringProperty('30')
    numberStr = StringProperty('integration points')
    
    # important values
    h = NumericProperty()
    minStrain, maxStrain = NumericProperty(-0.5), NumericProperty(0.5)
    numberIntegration = NumericProperty(30)
    
    # constructor
    def __init__(self, **kwargs):
        super(Explorer, self).__init__(**kwargs)
        self.cols, self.spacing = 1, Design.spacing
        self.graphContent = GridLayout(cols=2)
        self.h = self.csShape.ch
        self.allMaterial = MaterialList.Instance()
        self.create_gui()
    
    '''
    create the gui of the explorer
    '''
    def create_gui(self):
        self.create_strain_graph()
        self.create_stress_graph()
        self.add_widget(self.graphContent)
        self.create_input_area()
        self.numpad = Numpad(p=self, sign=True)
        self.popupNumpad = OwnPopup(content=self.numpad)
        
    '''
    the method create_graph create the graph, where you can observe
    the strain-behavior
    '''

    def create_strain_graph(self):
        self.graphStrain = OwnGraph(xlabel=self.strainStr,
                                    x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True,
                                    xmin=-0.5, xmax=0.5, ymin=0, ymax=self.h)
        self.graphContent.add_widget(self.graphStrain)
        self.pStrainCs = LinePlot(color=[255, 0, 0])
        self.graphStrain.add_plot(self.pStrainCs)
    
    '''
    the method create_graph create the graph, where you can observe
    the strain-behavior
    '''
    def create_stress_graph(self):
        self.graphStress = OwnGraph(xlabel=self.stressStr,
                                    x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True, padding=5,
                                    xmin=-0.5, xmax=0.5, ymin=0, ymax=self.h)
        self.graphContent.add_widget(self.graphStress)
        self.pStressCs = LinePlot(color=[255, 0, 0], points=[(0, 0), (0, self.h)])
        self.graphStress.add_plot(self.pStressCs)
    
    '''
    create the area where you can input the lower and upper strain
    '''
    def create_input_area(self):
        inputArea = GridLayout(cols=6, row_force_default=True,
                             row_default_height=Design.btnHeight, size_hint_y=None,
                             height=1.1 * Design.btnHeight)
        # create and bind btns
        self.lowerStrainBtn = OwnButton(text=self.defaultMinStrain)
        self.lowerStrainBtn.bind(on_press=self.show_popup)
        self.upperStrainBtn = OwnButton(text=self.defaultMaxStrain)
        self.upperStrainBtn.bind(on_press=self.show_popup)
        self.integrationNumberBtn = OwnButton(text=self.defaultNumber)
        self.integrationNumberBtn.bind(on_press=self.show_popup)
        # fill the inputArea
        inputArea.add_widget(OwnLabel(text=self.lowerStrainStr))
        inputArea.add_widget(self.lowerStrainBtn)
        inputArea.add_widget(OwnLabel(text=self.upperStrainStr))
        inputArea.add_widget(self.upperStrainBtn)
        inputArea.add_widget(OwnLabel(text=self.numberStr))
        inputArea.add_widget(self.integrationNumberBtn)
        self.add_widget(inputArea)
    
    '''
    update the strain-stress-behavior of the cross-section
    '''
    def update_strain_stress(self):
        # y=mx+b <=>y-mx=b
        self.layers = self.csShape.layers
        self.bars = self.csShape.bars
        self.update_graph()
        self.m = (self.h) / (self.maxStrain - self.minStrain)
        self.b = self.h - self.m * self.maxStrain
        # update all layer-lines
        for layer in self.layers:
            v = self.f(layer.y)
            pstrain = DashedLine(color=[255, 0, 0], points=[(0, layer.y), (v, layer.y)])
            self.graphStrain.add_plot(pstrain)
            pstress = DashedLine(color=[255, 0, 0],
                                 points=[(0, layer.y), (layer.material.materialLaw.f(v), layer.y)])
            self.graphStress.add_plot(pstress)
        # #update all bar-lines
        for bar in self.bars:
            v = self.f(bar.y)
            pStrain = DashedLine(color=[255, 0, 0], points=[(0, bar.y), (v, bar.y)])
            self.graphStrain.add_plot(pStrain)
            pstress = DashedLine(color=[255, 0, 0],
                                 points=[(0, bar.y), (bar.material.materialLaw.f(v), bar.y)])
            self.graphStress.add_plot(pstress)
        self.update_matrix()
    
    def update_matrix(self):
        concrete = self.allMaterial.allMaterials[3]
        # save the y-coordinates of the layers and bars
        yCoordinates = []
        for layer in self.layers:
            yCoordinates.append(layer.y)
        for bar in self.bars:
            yCoordinates.append(bar.y)
        #
        tick = self.h / (self.numberIntegration + len(yCoordinates))
        counter = 0.
        while counter < self.h:
            reinforcentmentExist = False
            for y in yCoordinates:
                if counter == y:
                    reinforcentmentExist = True
            if not reinforcentmentExist:
                v = self.f(counter)
                p = DashedLine(color=[0, 0, 0], points=[(0, counter), (v, counter)])
                self.graphStrain.add_plot(p)
                p = DashedLine(color=[0, 0, 0], points=[(0, counter), (concrete.materialLaw.f(v), counter)])
                self.graphStress.add_plot(p)
            counter += tick
            
    '''
    update the graph-properties
    '''
    def update_graph(self):
        # update strain-graph
        self.graphStrain.xmin = self.minStrain
        self.graphStrain.xmax = self.maxStrain
        self.graphStrain.x_ticks_major = (self.maxStrain - self.minStrain) / 5.
        self.graphStrain.ymax = self.h
        self.graphStrain.y_ticks_major = self.h / 5.
        # updare stress-graph
        self.graphStress.xmin = self.minStrain
        self.graphStress.xmax = self.maxStrain
        self.graphStress.x_ticks_major = (self.maxStrain - self.minStrain) / 5.
        self.graphStress.ymax = self.h
        self.graphStress.y_ticks_major = self.h / 5.
        # update plots
        self.pStrainCs.points = [ (0, 0), (0, self.h)]
        self.pStressCs.points = [(0, 0), (0, self.h)]
        # clear the graph and delete the plots which represent 
        # the layers and the bars
        self.clear_graph()
    
    
    '''
    delete the plots which represent a layer or a bar
    '''
    def clear_graph(self):
        while len(self.graphStrain.plots) > 2 or len(self.graphStress.plots) > 1:
            for plot in self.graphStrain.plots:
                if  plot != self.pStrainCs:
                    self.graphStrain.remove_plot(plot)
                    self.graphStrain._clear_buffer()
            for plot in self.graphStress.plots:
                if plot != self.pStressCs:
                    self.graphStress.remove_plot(plot)
                    self.graphStress._clear_buffer()
            
    '''
    the function which describes the strain-line
    '''
    def f(self, y):
        # y=mx+b <=> x=(y-b)/m
        return (y - self.b) / self.m
    
    '''
    update the cs-properties
    '''
    def update_csShape(self, cs, h, layers, bars):
        self.csShape = cs
        self.layers = layers
        self.bars = bars
        self.h = h
        print(self.h)
    
    '''
    open the popup for the value input
    '''
    def show_popup(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = str(btn.text)
        if btn == self.lowerStrainBtn:
            self.popupNumpad.title = self.lowerStrainStr
        elif btn == self.upperStrainBtn:
            self.popupNumpad.title = self.upperStrainStr
        elif btn == self.integrationNumberBtn:
            self.popupNumpad.title = self.numberStr
        self.popupNumpad.open()
    
    '''
    cancel the numpad-input. the numpad call this method
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()
    
    '''
    when the numpad input will be confirmed. the numpad call this method
    '''
    def finished_numpad(self):
        s = self.numpad.lblTextinput.text
        v = float(s)
        self.focusBtn.text = s
        if self.focusBtn == self.lowerStrainBtn:
            self.minStrain = v
        elif self.focusBtn == self.upperStrainBtn:
            self.maxStrain = v
        elif self.focusBtn == self.integrationNumberBtn:
            # 100 is the limit
            if v > 100:
                v = 100
            else:
                self.integrationNumberBtn.text = s
                self.numberIntegration = int(v)
        self.update_strain_stress()
        self.popupNumpad.dismiss()
