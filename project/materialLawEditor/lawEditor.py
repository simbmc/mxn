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


class MaterialLawEditor(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(MaterialLawEditor, self).__init__(**kwargs)
        self.cols = 2
        self.spacing=Design.spacing
        self.btnSize = Design.btnHeight
        self.linearEditor = LinearEditor()
        self.linearEditor.sign_in(self)
        self.multiLinearEditor = MultilinearEditor()
        self.multiLinearEditor.sign_in(self)
        self.quadraticEditor = QuadraticFunctionEditor()
        self.quadraticEditor.sign_in(self)
        self.create_gui()
    
    '''
    create the gui of the lawEditor
    '''
    def create_gui(self):
        self.create_graphs()
        self.create_selction_area()
        self.editor = OwnPopup(title='function-type',content=self.linearEditor)
        
    '''
    create the area where you can the function-type
    '''
    def create_selction_area(self):
        self.information = GridLayout(cols=1,spacing=Design.spacing)
        self.create_btns()
        self.information.add_widget(self.btnLinear)
        self.information.add_widget(self.btnMultiLinear)
        self.information.add_widget(self.btnQuadratic)
        self.information.add_widget(self.btnExponentiell)
        confirmArea = GridLayout(cols=2, spacing=10)
        btnOk = OwnButton(text='ok')
        btnOk.bind(on_press=self.confirm)
        btnCancel = OwnButton(text='cancel')
        btnCancel.bind(on_press=self.cancel)
        confirmArea.add_widget(btnOk)
        confirmArea.add_widget(btnCancel)
        self.information.add_widget(confirmArea)
        self.add_widget(self.information)
    
    '''
    create all graphs to show the function
    '''
    def create_graphs(self):
        self.create_graph_linear()
        self.create_graph_multilinear()
        self.create_graph_quadratic()
    
    '''
    create the btns
    '''
    def create_btns(self):
        self.btnLinear = OwnButton(text='linear')
        self.focusBtn = self.btnLinear
        self.btnMultiLinear = OwnButton(text='multilinear')
        self.btnQuadratic = OwnButton(text='quadratic')
        self.btnExponentiell = OwnButton(text='exponentiell')
        self.btnLinear.bind(on_press=self.show_linear)
        self.btnMultiLinear.bind(on_press=self.show_multilinear)
        self.btnQuadratic.bind(on_press=self.show_quadratic)
        self.btnExponentiell.bind(on_press=self.show_exponentiell)
        
    '''
    create the linear-function graph
    '''
    def create_graph_linear(self):
        self.graphLinear = OwnGraph(x_ticks_major=0.1, y_ticks_major=0.1,
                                 y_grid_label=True, x_grid_label=True,
                                 xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[(0, 0), (0.5, 0.5)], color=Design.focusColor)
        self.graphLinear.add_plot(self.p)
        self.focusGraph = self.graphLinear
        self.add_widget(self.graphLinear)

    '''
    create the quadratic-function graph
    '''
    def create_graph_quadratic(self):
        self.graphQuadratic = OwnGraph(x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True,
                                    xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[(0.005 * x, 0.0001 * x * x)
                                  for x in range(100)], color=Design.focusColor)
        self.graphQuadratic.add_plot(self.p)
    
    '''
    create the mulit-linear-function graph
    '''
    def create_graph_multilinear(self):
        self.graphMulitLinear = OwnGraph(x_ticks_major=0.1, y_ticks_major=0.1,
                                      y_grid_label=True, x_grid_label=True,
                                      xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[
                          (0, 0), (0.1, 0.3), (0.2, 0.1), (0.3, 0.2), (0.4, 0.1), (0.5, 0.45)], color=Design.focusColor)
        self.graphMulitLinear.add_plot(self.p)
    
    '''
    show the linear-function-view
    '''
    def show_linear(self, btn):
        self.focusBtn = btn
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphLinear, index=1)
        self.focusGraph = self.graphLinear
    
    '''
    show the quadratic-function-view
    '''
    def show_quadratic(self, btn):
        self.focusBtn = btn
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphQuadratic, index=1)
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
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphMulitLinear, index=1)
        self.focusGraph = self.graphMulitLinear
        
    '''
    cancel the create-process
    '''
    def cancel(self,btn):
        self.creater.cancel(btn)
    
    '''
    create the process, where you select the function-type
    '''
    def cancel_graphicShow(self):
        self.editor.dismiss()
    
    '''
    confirm the selection of the function-type
    '''
    def confirm(self,btn):
        if self.focusBtn == self.btnLinear:
            self.editor.content = self.linearEditor
        elif self.focusBtn == self.btnMultiLinear:
            self.editor.content = self.multiLinearEditor
        elif self.focusBtn == self.btnQuadratic:
            self.editor.content = self.quadraticEditor
        elif self.focusBtn == self.btnExponentiell:
            return # not finished yet
        self.editor.open()
    
    '''
    set the created function
    '''
    def set_f(self,f):
        self.f = f
        self.creater.materialLaw.text=f.f_toString()
    
    '''
    sign in by the creater
    '''
    def sign_in(self,creater):
        self.creater=creater