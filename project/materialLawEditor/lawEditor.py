'''
Created on 06.07.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from materialLawEditor.linearEditor import LinearEditor
from plot.line import LinePlot
from materialLawEditor.multilinearEditor import MultilinearEditor
from materialLawEditor.quadraticFunctionEditor import QuadraticFunctionEditor
from kivy.uix.popup import Popup


class MaterialLawEditor(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(MaterialLawEditor, self).__init__(**kwargs)
        self.cols = 2
        self.btnSize = Design.btnSize
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
        self.editor = Popup(content=self.linearEditor)
        
    
    '''
    create all graphs to show the function
    '''
    def create_graphs(self):
        self.create_graph_linear()
        self.create_graph_multilinear()
        self.create_graph_quadratic()

    def create_selction_area(self):
        self.information = GridLayout(cols=1)
        self.btnLinear = Button(
            text='linear', size_hint_y=None, height=self.btnSize)
        self.focusBtn = self.btnLinear
        self.btnLinear.bind(on_press=self.show_linear)
        self.btnMultiLinear = Button(
            text='multilinear', size_hint_y=None, height=self.btnSize)
        self.btnMultiLinear.bind(on_press=self.show_multilinear)
        self.btnQuadratic = Button(
            text='quadratic', size_hint_y=None, height=self.btnSize)
        self.btnQuadratic.bind(on_press=self.show_quadratic)
        self.btnExponentiell = Button(
            text='exponentiell', size_hint_y=None, height=self.btnSize)
        self.btnExponentiell.bind(on_press=self.show_exponentiell)
        self.information.add_widget(self.btnLinear)
        self.information.add_widget(self.btnMultiLinear)
        self.information.add_widget(self.btnQuadratic)
        self.information.add_widget(self.btnExponentiell)
        confirmArea = GridLayout(cols=2, spacing=10)
        btnOk = Button(text='ok', size_hint_y=None, height=self.btnSize)
        btnOk.bind(on_press=self.confirm)
        btnCancel = Button(
            text='cancel', size_hint_y=None, height=self.btnSize)
        btnCancel.bind(on_press=self.cancel)
        confirmArea.add_widget(btnOk)
        confirmArea.add_widget(btnCancel)
        self.information.add_widget(confirmArea)
        self.add_widget(self.information)

    def create_graph_linear(self):
        self.graphLinear = Graph(x_ticks_major=0.1, y_ticks_major=0.1,
                                 y_grid_label=True, x_grid_label=True,
                                 xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[(0, 0), (0.5, 0.5)], color=Design.focusColor)
        self.graphLinear.add_plot(self.p)
        self.focusGraph = self.graphLinear
        self.add_widget(self.graphLinear)

    def create_graph_quadratic(self):
        self.graphQuadratic = Graph(x_ticks_major=0.1, y_ticks_major=0.1,
                                    y_grid_label=True, x_grid_label=True,
                                    xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[(0.005 * x, 0.0001 * x * x)
                                  for x in range(100)], color=Design.focusColor)
        self.graphQuadratic.add_plot(self.p)

    def create_graph_multilinear(self):
        self.graphMulitLinear = Graph(x_ticks_major=0.1, y_ticks_major=0.1,
                                      y_grid_label=True, x_grid_label=True,
                                      xmin=0.0, xmax=0.5, ymin=0, ymax=0.5)
        self.p = LinePlot(points=[
                          (0, 0), (0.1, 0.3), (0.2, 0.1), (0.3, 0.2), (0.4, 0.1), (0.5, 0.45)], color=Design.focusColor)
        self.graphMulitLinear.add_plot(self.p)

    def show_linear(self, btn):
        self.focusBtn = btn
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphLinear, index=1)
        self.focusGraph = self.graphLinear

    def show_quadratic(self, btn):
        self.focusBtn = btn
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphQuadratic, index=1)
        self.focusGraph = self.graphQuadratic

    def show_exponentiell(self, btn):
        print('not yet implemented')

    def show_multilinear(self, btn):
        self.focusBtn = btn
        self.remove_widget(self.focusGraph)
        self.add_widget(self.graphMulitLinear, index=1)
        self.focusGraph = self.graphMulitLinear
    
    def cancel(self,btn):
        print('cancel lawEditor-class')
        self.creater.cancel(btn)
    
    def cancel_graphicShow(self):
        self.editor.dismiss()
        
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
    
    def set_f(self,f):
        self.f = f
        self.creater.materialLaw.text=f.f_toString()
    
    def sign_in(self,creater):
        self.creater=creater