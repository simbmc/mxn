'''
Created on 06.07.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from materialLawEditor.linearEditor import LinearEditor
from materialLawEditor.multilinearEditor import MultilinearEditor
from materialLawEditor.quadraticFunctionEditor import QuadraticFunctionEditor
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownPopup import OwnPopup
from plot.line import LinePlot
from kivy.properties import ObjectProperty, StringProperty

class MaterialLawEditor(GridLayout):
    
    '''
    component to edit the material-law of the 
    materials
    '''
    
    # important components
    linearEditor = ObjectProperty()
    multiLinearEditor = ObjectProperty()
    quadraticEditor = ObjectProperty()
    creater = ObjectProperty()
    f = ObjectProperty()
    
    # strings
    okStr, cancelStr = StringProperty('ok'), StringProperty('cancel')
    linearStr, mulitlinearStr = StringProperty('linear'), StringProperty('multi-linear')
    quadraticStr, expStr = StringProperty('quadratic'), StringProperty('exponentiell')
    functiontypeStr = StringProperty('function-type')
    strainStr, stressStr = StringProperty('strain [MPa]'), StringProperty('stress')
    
    # constructor
    def __init__(self, **kwargs):
        super(MaterialLawEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.linearEditor = LinearEditor(lawEditor=self)
        self.multiLinearEditor = MultilinearEditor(lawEditor=self)
        self.quadraticEditor = QuadraticFunctionEditor(lawEditor=self)
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
        self.create_graph_linear()
        self.create_graph_multilinear()
        self.create_graph_quadratic()
    
    '''
    create the area where you can the function-type
    '''
    def create_selction_area(self):
        self.information = GridLayout(cols=1, spacing=Design.spacing)
        self.create_btns()
        self.information.add_widget(self.btnLinear)
        self.information.add_widget(self.btnMultiLinear)
        self.information.add_widget(self.btnQuadratic)
        self.information.add_widget(self.btnExponentiell)
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
        self.btnExponentiell = OwnButton(text=self.expStr)
        self.btnOk = OwnButton(text=self.okStr)
        self.btnCancel = OwnButton(text=self.cancelStr)
        self.btnOk.bind(on_press=self.confirm)
        self.btnCancel.bind(on_press=self.cancel)
        self.btnLinear.bind(on_press=self.show_linear)
        self.btnMultiLinear.bind(on_press=self.show_multilinear)
        self.btnQuadratic.bind(on_press=self.show_quadratic)
        self.btnExponentiell.bind(on_press=self.show_exponentiell)
        
    '''
    create the linear-function graph
    '''
    def create_graph_linear(self):
        self.graphLinear = OwnGraph(xlabel=self.stressStr, ylabel=self.strainStr,
                                    x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True,
                                    xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[(0, 0), (0.5, 0.5)], color=Design.focusColor)
        self.graphLinear.add_plot(self.p)
        self.focusGraph = self.graphLinear
        self.functionSelection.add_widget(self.graphLinear)

    '''
    create the quadratic-function graph
    '''
    def create_graph_quadratic(self):
        self.graphQuadratic = OwnGraph(xlabel=self.stressStr, ylabel=self.strainStr,
                                       x_ticks_major=0.1, y_ticks_major=0.1,
                                       y_grid_label=True, x_grid_label=True,
                                       xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[(0.005 * x, 0.0001 * x * x)
                                  for x in range(100)], color=Design.focusColor)
        self.graphQuadratic.add_plot(self.p)
    
    '''
    create the mulit-linear-function graph
    '''
    def create_graph_multilinear(self):
        self.graphMulitLinear = OwnGraph(xlabel=self.stressStr, ylabel=self.strainStr,
                                         x_ticks_major=0.1, y_ticks_major=0.1,
                                         y_grid_label=True, x_grid_label=True,
                                         xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[(0, 0), (0.1, 0.3), (0.2, 0.1), (0.3, 0.2), (0.4, 0.1), (0.5, 0.45)],
                          color=Design.focusColor)
        self.graphMulitLinear.add_plot(self.p)
    
    '''
    show the linear-function-view
    '''
    def show_linear(self, btn):
        self.focusBtn = btn
        self.functionSelection.remove_widget(self.focusGraph)
        self.functionSelection.add_widget(self.graphLinear, index=1)
        self.focusGraph = self.graphLinear
    
    '''
    show the quadratic-function-view
    '''
    def show_quadratic(self, btn):
        self.focusBtn = btn
        self.functionSelection.remove_widget(self.focusGraph)
        self.functionSelection.add_widget(self.graphQuadratic, index=1)
        self.focusGraph = self.graphQuadratic
    
    '''
    show the exp-function-view
    '''
    def show_exponentiell(self, btn):
        print('not yet implemented')
    
    '''
    show the multi-linear-function-view
    '''
    def show_multilinear(self, btn):
        self.focusBtn = btn
        self.functionSelection.remove_widget(self.focusGraph)
        self.functionSelection.add_widget(self.graphMulitLinear, index=1)
        self.focusGraph = self.graphMulitLinear
        
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
        print('confirm lawEditor (lawEditor)')
        self.remove_widget(self.focusEditor)
        if self.focusBtn == self.btnLinear:
            self.focusEditor = self.linearEditor
            self.add_widget(self.focusEditor)
            print('linear')
        elif self.focusBtn == self.btnMultiLinear:
            self.focusEditor = self.multiLinearEditor
            self.add_widget(self.focusEditor)
            print('multiLinear')
        elif self.focusBtn == self.btnQuadratic:
            self.focusEditor = self.quadraticEditor
            self.add_widget(self.focusEditor)
        elif self.focusBtn == self.btnExponentiell:
            print('not finished yet')
            return  # not finished yet
        self.editor.dismiss()
    
