'''
Created on 06.07.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.linearEditor import LinearEditor
from materialLawEditor.multilinearEditor import MultilinearEditor
from materialLawEditor.quadraticEditor import QuadraticEditor
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot
import numpy as np
from materialLawEditor.exponentialEditor import ExponentialEditor

class MaterialLawEditor(GridLayout):
    
    '''
    component to edit the material-law of the 
    materials
    '''
    
    # editor for the linear-function
    linearEditor = ObjectProperty()
    
    # editor for the multi-linear-function 
    multiLinearEditor = ObjectProperty()
    
    # editor for the quadratic-function
    quadraticEditor = ObjectProperty()
    
    # editor for the exponential-function
    exponentialEditor = ObjectProperty()
    
    # parent of the law-editor
    creater = ObjectProperty()
    
    # function f
    f = ObjectProperty()
    
    # switch to proof whether the multi-linear-editor was created
    boolMultLinearEditor = BooleanProperty(True)
    
    # switch to proof whether the exponential-editor was created
    boolExponentialEditor = BooleanProperty(True)
    
    # switch to proof whether the quadratic-editor was created
    boolQuadraticEditor = BooleanProperty(True)
    
    okStr = StringProperty('ok')
    
    cancelStr = StringProperty('cancel')
    
    linearStr = StringProperty('linear')
    
    mulitlinearStr = StringProperty('multi-linear')
    
    quadraticStr = StringProperty('quadratic')
    
    expStr = StringProperty('exponential')
    
    functiontypeStr = StringProperty('function-type')
    
    strainStr = StringProperty('strain [MPa]')
    
    stressStr = StringProperty('stress')
    
    
    '''
    constructor
    '''
    def __init__(self, **kwargs):
        super(MaterialLawEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.linearEditor = LinearEditor(lawEditor=self)
        self.create_gui()
    
    '''
    create the gui of the lawEditor
    '''
    def create_gui(self):
        self.functionSelection = GridLayout(cols=2)
        self.create_graphs()
        self.create_selction_area()
        self.editor = OwnPopup(title=self.functiontypeStr, content=self.functionSelection)
        self.add_widget(self.linearEditor)
        self.focusEditor = self.linearEditor
        
    '''
    create all graphs to show the function
    '''
    def create_graphs(self):
        self.graph = OwnGraph(xlabel=self.stressStr, ylabel=self.strainStr,
                                    x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True,
                                    xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        # all plots to represent the function
        self.pLinear = LinePlot(points=[(0, 0), (0.5, 0.5)], color=Design.focusColor)
        self.pQuadratic = LinePlot(points=[(0.005 * x, 0.0001 * x * x)
                                  for x in range(100)], color=Design.focusColor)
        self.pMultilinear = LinePlot(points=[(0, 0), (0.1, 0.3), (0.2, 0.1), (0.3, 0.2),
                                             (0.4, 0.1), (0.5, 0.45)],
                                     color=Design.focusColor)
        self.pExponential = LinePlot(points=[(0.005 * x, 0.0001 * np.exp(0.1 * x) - 0.0001)
                                  for x in range(100)], color=Design.focusColor)
        # default focus-plot is linear
        self.focusPlot = self.pLinear
        self.graph.add_plot(self.focusPlot)
        self.functionSelection.add_widget(self.graph)
        
    
    '''
    create the area where you can the function-type
    '''
    def create_selction_area(self):
        self.information = GridLayout(cols=1, spacing=Design.spacing)
        self.create_btns()
        self.information.add_widget(self.btnLinear)
        self.information.add_widget(self.btnMultiLinear)
        self.information.add_widget(self.btnQuadratic)
        self.information.add_widget(self.btnExponential)
        confirmArea = GridLayout(cols=2, spacing=Design.spacing)
        confirmArea.add_widget(self.btnOk)
        confirmArea.add_widget(self.btnCancel)
        self.information.add_widget(confirmArea)
        self.functionSelection.add_widget(self.information)
    
    '''
    create the all btns of the material-law-component where you 
    can select the function-type
    '''
    def create_btns(self):
        self.btnLinear = OwnButton(text=self.linearStr)
        self.focusBtn = self.btnLinear
        self.btnMultiLinear = OwnButton(text=self.mulitlinearStr)
        self.btnQuadratic = OwnButton(text=self.quadraticStr)
        self.btnExponential = OwnButton(text=self.expStr)
        self.btnOk = OwnButton(text=self.okStr)
        self.btnCancel = OwnButton(text=self.cancelStr)
        self.btnOk.bind(on_press=self.confirm)
        self.btnCancel.bind(on_press=self.cancel)
        self.btnLinear.bind(on_press=self.show_linear)
        self.btnMultiLinear.bind(on_press=self.show_multilinear)
        self.btnQuadratic.bind(on_press=self.show_quadratic)
        self.btnExponential.bind(on_press=self.show_exponentiell)    
    
    '''
    show the linear-function-view
    '''
    def show_linear(self, btn):
        self.focusBtn = btn
        self.graph.remove_plot(self.focusPlot)
        self.focusPlot = self.pLinear
        self.graph.add_plot(self.focusPlot)
    
    '''
    show the quadratic-function-view
    '''
    def show_quadratic(self, btn):
        if self.boolQuadraticEditor:
            self.quadraticEditor = QuadraticEditor(lawEditor=self)
            self.boolQuadraticEditor = False
        self.focusBtn = btn
        self.graph.remove_plot(self.focusPlot)
        self.focusPlot = self.pQuadratic
        self.graph.add_plot(self.focusPlot)
    
    '''
    show the exp-function-view
    '''
    def show_exponentiell(self, btn):
        if self.boolExponentialEditor:
            self.exponentialEditor = ExponentialEditor(lawEditor=self)
            self.boolExponentialEditor = False
        self.focusBtn = btn
        self.graph.remove_plot(self.focusPlot)
        self.focusPlot = self.pExponential
        self.graph.add_plot(self.focusPlot)
    
    '''
    show the multi-linear-function-view
    '''
    def show_multilinear(self, btn):
        if self.boolMultLinearEditor:
            self.multiLinearEditor = MultilinearEditor(lawEditor=self)
            self.boolMultLinearEditor = False
        self.focusBtn = btn
        self.graph.remove_plot(self.focusPlot)
        self.focusPlot = self.pMultilinear
        self.graph.add_plot(self.focusPlot)
        
    '''
    cancel the create-process
    '''
    def cancel(self, btn):
        self.editor.dismiss()
    
    '''
    create the process, where you select the function-type
    '''
    def cancel_graphicShow(self):
        self.creater.popupLawEditor.dismiss()
    
    '''
    confirm the selection of the function-type
    '''
    def confirm(self, btn):
        self.remove_widget(self.focusEditor)
        if self.focusBtn == self.btnLinear:
            self.focusEditor = self.linearEditor
            self.add_widget(self.focusEditor)
        elif self.focusBtn == self.btnMultiLinear:
            if self.boolMultLinearEditor:
                self.multiLinearEditor = MultilinearEditor(lawEditor=self)
                self.boolMultLinearEditor = False
            self.focusEditor = self.multiLinearEditor
            self.add_widget(self.focusEditor)
        elif self.focusBtn == self.btnQuadratic:
            if self.boolQuadraticEditor:
                self.quadraticEditor = QuadraticEditor(lawEditor=self)
                self.boolQuadraticEditor = False
            self.focusEditor = self.quadraticEditor
            self.add_widget(self.focusEditor)
        elif self.focusBtn == self.btnExponential:
            if self.boolExponentialEditor:
                self.exponentialEditor = ExponentialEditor(lawEditor=self)
                self.boolExponentialEditor = False
            self.focusEditor = self.exponentialEditor
            self.add_widget(self.exponentialEditor)
        self.editor.dismiss()
