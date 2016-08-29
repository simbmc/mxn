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
import numpy as np

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
    
    # important values
    h = NumericProperty()
    minStrain, maxStrain = NumericProperty(-0.5), NumericProperty(0.5)
    
    # constructor
    def __init__(self, **kwargs):
        super(Explorer, self).__init__(**kwargs)
        self.cols, self.spacing = 1, Design.spacing
        self.graphContent = GridLayout(cols=2)
        self.h = self.csShape.ch
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
        self.pStrain = LinePlot(color=[255, 0, 0])
        self.pStrainCs = LinePlot(color=[255, 0, 0])
        self.graphStrain.add_plot(self.pStrain)
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
        inputArea = GridLayout(cols=4, row_force_default=True,
                             row_default_height=Design.btnHeight, size_hint_y=None,
                             height=1.1 * Design.btnHeight)
        self.lowerStrainBtn = OwnButton(text=self.defaultMinStrain)
        self.lowerStrainBtn.bind(on_press=self.show_popup)
        self.upperStrainBtn = OwnButton(text=self.defaultMaxStrain)
        self.upperStrainBtn.bind(on_press=self.show_popup)
        inputArea.add_widget(OwnLabel(text=self.lowerStrainStr))
        inputArea.add_widget(self.lowerStrainBtn)
        inputArea.add_widget(OwnLabel(text=self.upperStrainStr))
        inputArea.add_widget(self.upperStrainBtn)
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
                                 points=[(0, layer.y),
                                         (layer.material.materialLaw.f(np.abs(v)), layer.y)])
            self.graphStress.add_plot(pstress)
        # #update all bar-lines
        for bar in self.bars:
            v = self.f(bar.y)
            pStrain = DashedLine(color=[255, 0, 0], points=[(0, bar.y), (v, bar.y)])
            self.graphStrain.add_plot(pStrain)
            pstress = DashedLine(color=[255, 0, 0],
                                 points=[(0, bar.y),
                                         (bar.material.materialLaw.f(np.abs(bar.y)), bar.y)])
            self.graphStress.add_plot(pstress)
    
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
        self.pStrain.points = [(self.minStrain, 0), (self.maxStrain, self.h)]
        self.pStrainCs.points = [(self.minStrain, 0), (0, 0), (0, self.h), (self.maxStrain, self.h)]
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
                if plot != self.pStrain and plot != self.pStrainCs:
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
    
    '''
    open the popup for the value input
    '''
    def show_popup(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = str(btn.text)
        if btn == self.lowerStrainBtn:
            self.popupNumpad.title = self.lowerStrainStr
        else:
            self.popupNumpad.title = self.upperStrainStr
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
            self.update_strain_stress()
        else:
            self.maxStrain = v
            self.update_strain_stress()
        self.popupNumpad.dismiss()
