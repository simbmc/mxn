'''
Created on 01.09.2016

@author: mkennert
'''
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot


class ExplorerGui:
    '''
    the ExplorerGui contains and manages all gui-components of the explorer.
    '''
    
    strainStr = StringProperty('strain')
    
    stressStr = StringProperty('stress')
    
    lowerStrainStr = StringProperty('lower-strain:')
    
    upperStrainStr = StringProperty('upper-strain:')
    
    defaultMinStrain = StringProperty('-0.5')
    
    defaultMaxStrain = StringProperty('0.5')
    
    defaultNumber = StringProperty('30')
    
    numberStr = StringProperty('integration points')
    
    nfStr = StringProperty('normal force:')
    
    momStr = StringProperty('moment:')
    
    '''
    create the gui of the explorer
    '''
        
    def create_gui(self):
        self.create_graphs()
        self.add_widget(self.graphContent)
        self.create_input_area()
        self.numpad = Numpad(p=self, sign=True)
        self.popupNumpad = OwnPopup(content=self.numpad)
    
    '''
    the method create_graphs create the graphs, where you can observe
    the stress-strain-behavior
    '''
        
    def create_graphs(self):
        # create-strain-graph
        self.graphStrain = OwnGraph(xlabel=self.strainStr,
                                    x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True,
                                    xmin=-0.5, xmax=0.5, ymin=0, ymax=self.h)
        self.graphContent.add_widget(self.graphStrain)
        self.pStrainCs = LinePlot(color=[255, 0, 0])
        self.graphStrain.add_plot(self.pStrainCs)
        # create-stress-graph
        self.graphStress = OwnGraph(xlabel=self.stressStr,
                                    x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True, padding=5,
                                    xmin=-0.5, xmax=0.5, ymin=0, ymax=self.h)
        self.graphContent.add_widget(self.graphStress)
        self.pStressCs = LinePlot(color=[255, 0, 0])
        self.graphStress.add_plot(self.pStressCs)
    
    '''
    create the area where you can input the lower and upper strain
    '''
        
    def create_input_area(self):
        inputArea = GridLayout(cols=6, row_force_default=True,
                             row_default_height=Design.btnHeight, size_hint_y=None,
                             height=2.1 * Design.btnHeight)
        # create and bind btns
        self.lowerStrainBtn = OwnButton(text=self.defaultMinStrain)
        self.lowerStrainBtn.bind(on_press=self.show_popup)
        self.upperStrainBtn = OwnButton(text=self.defaultMaxStrain)
        self.upperStrainBtn.bind(on_press=self.show_popup)
        self.integrationNumberBtn = OwnButton(text=self.defaultNumber)
        self.integrationNumberBtn.bind(on_press=self.show_popup)
        self.normalForceLbl = OwnLabel()
        self.momentLbl = OwnLabel()
        # fill the inputArea
        inputArea.add_widget(OwnLabel(text=self.lowerStrainStr))
        inputArea.add_widget(self.lowerStrainBtn)
        inputArea.add_widget(OwnLabel(text=self.upperStrainStr))
        inputArea.add_widget(self.upperStrainBtn)
        inputArea.add_widget(OwnLabel(text=self.numberStr))
        inputArea.add_widget(self.integrationNumberBtn)
        inputArea.add_widget(OwnLabel(text=self.nfStr))
        inputArea.add_widget(self.normalForceLbl)
        inputArea.add_widget(OwnLabel(text=self.momStr))
        inputArea.add_widget(self.momentLbl)
        self.add_widget(inputArea)
    
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
                self.numberIntegration = 100
                self.integrationNumberBtn.text = str(100)
            else:
                self.integrationNumberBtn.text = s
                self.numberIntegration = int(v)
        self.update_explorer()
        self.popupNumpad.dismiss()
    
    '''
    update the graph-properties
    '''

    def update_graph(self):
        print('update graph')
        # update strain-graph
        self.graphStrain.xmin = self.minStrain * 1.05 
        self.graphStrain.xmax = self.maxStrain * 1.05 
        self.graphStrain.x_ticks_major = (self.graphStrain.xmax  - self.graphStrain.xmin) / 5.
        self.graphStrain.ymax = self.h
        self.graphStrain.y_ticks_major = self.h / 5.
        # updare stress-graph
        self.graphStress.xmin = self.minStress * 1.05
        self.graphStress.xmax = self.maxStress * 1.05
        self.graphStress.x_ticks_major = (self.maxStress - self.minStress) / 5.
        self.graphStress.ymax = self.h
        self.graphStress.y_ticks_major = self.h / 5.
        # update plots
        self.pStrainCs.points = [ (0, 0), (0, self.h)]
        self.pStressCs.points = [(0, 0), (0, self.h)]