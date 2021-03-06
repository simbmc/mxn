'''
Created on 09.09.2016

@author: mkennert
'''
from decimal import Decimal

from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider

from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
from plot.thickline import ThickLine
from ownComponents.ownButton import OwnButton

class EnvelopeGui:
    
    '''
    create the gui of the envelope
    '''

    def create_gui(self):
        self.create_graphs()
        self.slider = Slider()
        self.slider.bind(value=self.update_slider)
        slideArea = GridLayout(cols=2, row_force_default=True,
                               row_default_height=Design.btnHeight, size_hint_y=None,
                               height=1.1 * Design.btnHeight)
        lblArea = GridLayout(cols=3, row_force_default=True,
                             row_default_height=Design.btnHeight, size_hint_y=None,
                             height=1.1 * Design.btnHeight)
        self.normalForceLbl = OwnLabel()
        self.momentLbl = OwnLabel()
        lblArea.add_widget(self.normalForceLbl)
        lblArea.add_widget(self.momentLbl)
        btnClear = OwnButton(text='clear')
        btnClear.bind(on_press=self.clear_graph)
        lblArea.add_widget(btnClear)
        slideArea.add_widget(self.slider)
        slideArea.add_widget(lblArea)
        self.add_widget(slideArea)

    '''
    create the graph
    '''

    def create_graphs(self):
        self.graphs = GridLayout(cols=2, spacing=Design.spacing)
        # create the left graph- explorer graph
        self.graphLeft = OwnGraph(xlabel=self.strainStr, ylabel=self.heightStr,
                                  x_ticks_major=0.1, y_ticks_major=0.1,
                                  y_grid_label=True, x_grid_label=True,
                                  xmin=-0.5, xmax=0.5, ymin=0, ymax=self.explorer.h)
        # create the right graph
        self.graphRight = OwnGraph(xlabel=self.momentStr, ylabel=self.forceStr,
                                   x_ticks_major=100, y_ticks_major=50,
                                   y_grid_label=True, x_grid_label=True,
                                   xmin=-0.5, xmax=400, ymin=0, ymax=350)
        self.graphs.add_widget(self.graphLeft)
        self.graphs.add_widget(self.graphRight)
        self.add_widget(self.graphs)
        self.plots = [LinePlot(color=[0, 0, 0]) for i in range(self.n_plt)]
        for plot in self.plots:
            self.graphLeft.add_plot(plot)
        self.focusLine = ThickLine(color=[255, 0, 0])
        self.graphLeft.add_plot(self.focusLine)
        self.forceMomentLine = LinePlot(color=[255, 0, 0])
        self.graphRight.add_plot(self.forceMomentLine)
        self.focusPoint = FilledEllipse(color=[255, 0, 0])
        self.graphRight.add_plot(self.focusPoint)
        self.px = LinePlot(color=[0, 0, 0])
        self.py = LinePlot(color=[0, 0, 0])
        self.graphRight.add_plot(self.px)
        self.graphRight.add_plot(self.py)

    '''
    will called when the slider changes the value
    '''

    def update_slider(self, inst, v):
        v = int(v)
        self.focusLine.points = [(-self.eps_arr[0][v], 0),
                                 (-self.eps_arr[1][v], self.explorer.h)]
        self.focusPoint.xrange = [-self.M_arr[v] - 
                                  self.eps_x, -self.M_arr[v] + self.eps_x]
        self.focusPoint.yrange = [-self.N_arr[v] - 
                                  self.eps_y, -self.N_arr[v] + self.eps_y]
        self.normalForceLbl.text = 'N: ' + str('%.2E' % Decimal(str(-self.N_arr[v])))
        self.momentLbl.text = 'M: ' + str('%.2E' % Decimal(str(-self.M_arr[v])))
        
    '''
    update the graph
    '''

    def update_graph(self, eps_arr, M_arr, N_arr):
        h = self.explorer.h
        # update left graph
        self.graphLeft.ymax = h
        self.graphLeft.y_ticks_major = h / 5.
        min_v, max_v = self.find_min_max()
        self.graphLeft.xmax = float(max_v) * 1.02
        self.graphLeft.xmin = float(min_v) * 1.02
        self.graphLeft.x_ticks_major = float(
                format((self.graphLeft.xmax - self.graphLeft.xmin) / 4., '.1g'))
        # plot left side
        n = len(eps_arr[0])
        index = 0
        for i in range(n):
            self.plots[index].points = [
                (-eps_arr[0][i], 0), (-eps_arr[1][i], h)]
            index += 1
        while index < self.n_plt:
            self.plots[index].points = [(0, 0), (0, 0)]
            index += 1
        # plot right side
        points = [(-m, -n) for n, m in zip(N_arr, M_arr)]
        if points != self.forceMomentLine.points:
            p = LinePlot(color=[0, 0, 255], points=self.forceMomentLine.points)
            self.graphRight.add_plot(p)
            self.forceMomentLine.points = [(-m, -n) for n, m in zip(N_arr, M_arr)]
            self.update_graph_borders()
    
    def update_graph_borders(self):
        minM, maxM = 1e10, -1e10
        minN, maxN = 1e10, -1e10
        for plt in self.graphRight.plots:
            if plt != self.px and plt != self.py:
                for p in plt.points:
                    x, y = -p[0], -p[1]
                    if x > maxM:
                        maxM = x
                    if x < minM:
                        minM = x
                    if y > maxN:
                        maxN = y
                    if y < minN:
                        minN = y
        eps = 1.05
        self.graphRight.xmin = float(-maxM) * eps
        self.graphRight.xmax = float(-minM) * eps
        self.graphRight.ymin = float(-maxN) * eps
        self.graphRight.ymax = float(-minN) * eps
        self.graphRight.y_ticks_major = float(
            format((self.graphRight.ymax - self.graphRight.ymin) / 5., '.1g'))
        self.graphRight.x_ticks_major = float(
            format((self.graphRight.xmax - self.graphRight.xmin) / 5., '.1g'))
        self.eps_x = (self.graphRight.xmax - self.graphRight.xmin) / 8e1
        self.eps_y = (self.graphRight.ymax - self.graphRight.ymin) / 8e1
        self.focusPoint.xrange = [-self.M_arr[0] - 
                                  self.eps_x, -self.M_arr[0] + self.eps_x]
        self.focusPoint.yrange = [-self.N_arr[0] - 
                                  self.eps_y, -self.N_arr[0] + self.eps_y]
        self.slider.value=0
        self.py.points = [(0, self.graphRight.ymin), (0, self.graphRight.ymax)]
        self.px.points = [(self.graphRight.xmin, 0), (self.graphRight.xmax, 0)]
            
    '''
    clear the graph
    '''
        
    def clear_graph(self, btn):
        if len(self.graphRight.plots) < 4:
            return
        while len(self.graphRight.plots) > 4:
            for plot in self.graphRight.plots:
                if plot != self.forceMomentLine and plot != self.px\
                    and plot != self.py and plot != self.focusPoint:
                    self.graphRight.remove_plot(plot)
                    self.graphRight._clear_buffer()
        self.update_graph_borders()
    
    '''
    find the minimum and maximum value of the eps_arr
    '''

    def find_min_max(self):
        max_v = -1 * 1e8
        min_v = 1e8
        for i in range(len(self.eps_arr[0])):
            v1, v2 = -self.eps_arr[0][i], -self.eps_arr[1][i]
            if v1 < min_v:
                min_v = v1
            if v1 > max_v:
                max_v = v1
            if v2 < min_v:
                min_v = v2
            if v2 > max_v:
                max_v = v2
        return min_v, max_v
