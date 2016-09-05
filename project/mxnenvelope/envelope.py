'''
Created on 02.09.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider

from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
import numpy as np
from plot.line import LinePlot
from plot.thickline import ThickLine
from plot.filled_ellipse import FilledEllipse


class MXNEnvelop(GridLayout):

    # explorer of the cross section
    explorer = ObjectProperty()
    
    n_eps = NumericProperty(20)
    
    # number of plots 4*n_eps
    n_plt = NumericProperty(80)
    
    '''
    constructor
    '''

    def __init__(self, **kwargs):
        super(MXNEnvelop, self).__init__(**kwargs)
        self.cols = 1
        self.create_gui()

    '''
    create the gui of the graph
    '''

    def create_gui(self):
        self.create_graphs()
        self.slider = Slider()
        self.slider.bind(value=self.update_slider)
        slideArea = GridLayout(cols=2, row_force_default=True,
                               row_default_height=Design.btnHeight, size_hint_y=None,
                               height=1.1 * Design.btnHeight)
        self.valueLbl = OwnLabel(text='step: 0')
        slideArea.add_widget(self.valueLbl)
        slideArea.add_widget(self.slider)
        self.add_widget(slideArea)

    '''
    create the graph
    '''

    def create_graphs(self):
        self.graphs = GridLayout(cols=2, spacing=Design.spacing)
        # create the left graph- explorer graph
        self.graphLeft = OwnGraph(x_ticks_major=0.1, y_ticks_major=0.1,
                                  y_grid_label=True, x_grid_label=True,
                                  xmin=-0.5, xmax=0.5, ymin=0, ymax=self.explorer.h)
        # create the right graph
        self.graphRight = OwnGraph(x_ticks_major=100, y_ticks_major=50,
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
        self.forceMomentLine = LinePlot(color=[0, 0, 255])
        self.graphRight.add_plot(self.forceMomentLine)
        self.focusPoint = FilledEllipse(color=[255, 0, 0])
        self.graphRight.add_plot(self.focusPoint)
    
    '''
    will called when the slider changes the value
    '''

    def update_slider(self, inst, v):
        v = int(v)
        self.valueLbl.text = 'step: ' + str(v)
        self.focusLine.points = [(-self.eps_arr[0][v], 0), (-self.eps_arr[1][v], self.explorer.h)]
        self.focusPoint.xrange = [self.M_arr[v] - self.eps_x, self.M_arr[v] + self.eps_x]
        self.focusPoint.yrange = [-self.N_arr[v] - self.eps_y, -self.N_arr[v] + self.eps_y]
    
    '''
    update the graph
    '''

    def update_graph(self, eps_arr, M_arr, N_arr):
        h = self.explorer.h
        # update left graph
        self.graphLeft.ymax = h
        self.graphLeft.y_ticks_major = h / 5.
        min_v, max_v = self.find_min_max()
        print(min_v, max_v)
        self.graphLeft.xmax = float(max_v)* 1.02
        self.graphLeft.xmin = float(min_v)* 1.02
        self.graphLeft.x_ticks_major = np.abs((self.graphLeft.xmax - self.graphLeft.xmin)) / 5.

        # update right graph
        max_index = np.argmax(self.M_arr)
        self.graphRight.xmax = float(self.M_arr[max_index]) * 1.02
        self.graphRight.xmin = 0
        self.graphRight.x_ticks_major = (self.graphRight.xmax - self.graphRight.xmin) / 3.
        max_index = np.argmax(self.N_arr)
        min_index = np.argmin(self.N_arr)
        self.graphRight.ymax = -float(self.N_arr[min_index]) * 1.02
        self.graphRight.ymin = -float(self.N_arr[max_index]) * 1.02
        self.graphRight.y_ticks_major = (self.graphRight.ymax - self.graphRight.ymin) / 5.
        # plot left side
        n = len(eps_arr[0])
        index = 0
        self.eps_x = (self.graphRight.xmax - self.graphRight.xmin) / 8e1
        self.eps_y = (self.graphRight.ymax - self.graphRight.ymin) / 8e1
        for i in range(n):
            self.plots[index].points = [(-eps_arr[0][i], 0), (-eps_arr[1][i], h)]
            index += 1
        while index < self.n_plt:
            self.plots[index].points = [(0, 0), (0, 0)]
            index += 1
        # plot right side
        self.forceMomentLine.points = [(m, -n) for n, m in zip(N_arr, M_arr)]
    
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
        
    '''
    calculate parameters for the plot
    '''

    def calculation(self):
        eps_u_r, y_r, eps_cu = self.explorer.get_coordinates_upperStrain()
        eps_lo_arr = self.convert_eps_u_2_lo(
            self.explorer.minStrain, eps_u_r, y_r)
        env_reinf_idx = -1
        if len(eps_lo_arr) <> 0:
            env_reinf_idx = np.argmin(eps_lo_arr)
        eps_ccu = 0.8 * eps_cu
        self.eps_arr = self.get_strain_arrays(
            eps_cu, eps_ccu, eps_u_r, y_r, env_reinf_idx, self.n_eps)
        # get the m-n envelop
        self.M_arr = np.zeros_like(self.eps_arr[0])
        self.N_arr = np.zeros_like(self.eps_arr[0])
        for i in np.arange(len(self.eps_arr[0])):
            result = self.explorer.calculation(
                self.eps_arr[0][i], self.eps_arr[1][i], self.n_eps)
            self.N_arr[i] = result[0]
            self.M_arr[i] = result[1]
        self.update_graph(self.eps_arr, self.M_arr, self.N_arr)
        self.slider.max = len(self.eps_arr[0]) - 1
        self.focusLine.points = [(-self.eps_arr[0][0], 0), (-self.eps_arr[1][0], self.explorer.h)]
        self.focusPoint.xrange = [self.M_arr[0] - self.eps_x, self.M_arr[0] + self.eps_x]
        self.focusPoint.yrange = [self.N_arr[0] - self.eps_y, self.N_arr[0] + self.eps_y]
        self.slider.value = 0
        self.valueLbl.text = 'step: 0'

    '''
    return the strain_arrays
    '''

    def get_strain_arrays(self, eps_cu, eps_ccu, eps_u_r, reinf_y_coord, env_reinf_idx, n_eps):
        n = len(self.explorer.layers) + len(self.explorer.bars)
        if n > 0:
            eps_t_lo = self.convert_eps_u_2_lo(
                eps_cu, eps_u_r, reinf_y_coord[env_reinf_idx])
            eps_t_lo_0 = self.convert_eps_u_2_lo(
                0., eps_u_r, reinf_y_coord[env_reinf_idx])
            eps_t_u = eps_u_r
            # Strain arrays for the lower rim
            eps_cc_0 = np.linspace(eps_ccu, 0., n_eps)
            eps_0_tlo = np.linspace(0., eps_t_lo, n_eps)
            eps_tlo_tlo0 = np.linspace(eps_t_lo, eps_t_lo_0, n_eps)
            eps_tlo0_tu = np.linspace(eps_t_lo_0, eps_t_u, n_eps)

            # Strain arrays for the upper rim
            eps_cc_c = np.linspace(eps_ccu, eps_cu, n_eps)
            eps_c_const = eps_cu * np.ones_like(eps_cc_0)
            eps_c_0 = np.linspace(eps_cu, 0., n_eps)
            eps_0_tu = np.linspace(0., eps_t_u, n_eps)

            eps1 = np.vstack([eps_cc_0, eps_cc_c])
            eps2 = np.vstack([eps_0_tlo, eps_c_const])
            eps3 = np.vstack([eps_tlo_tlo0, eps_c_0])
            eps4 = np.vstack([eps_tlo0_tu, eps_0_tu])

            return np.hstack([eps1, eps2, eps3, eps4])
        else:
            # Strain arrays for the lower rim
            eps_cc_0 = np.linspace(eps_ccu, 0., n_eps)
            eps_00 = np.zeros_like(eps_cc_0)

            # Strain arrays for the upper rim
            eps_cc_c = np.linspace(eps_ccu, eps_cu, n_eps)
            eps_c_0 = np.linspace(eps_cu, 0., n_eps)

            eps1 = np.vstack([eps_cc_0, eps_cc_c])
            eps2 = np.vstack([eps_00, eps_c_0])

            return np.hstack([eps1, eps2])

    '''
    Convert the strain in the lowest reinforcement layer at failure
    to the strain at the bottom of the cross section
    '''

    def convert_eps_u_2_lo(self, eps_up, eps_u_r, y_coord_r):
        # eps_u_r -- the maximum strain of the corresponding reinforcement
        h = self.explorer.h
        eps_lo = eps_up + (eps_u_r - eps_up) / (h - y_coord_r) * h
        return eps_lo
