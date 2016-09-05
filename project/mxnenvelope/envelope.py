'''
Created on 02.09.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider

from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from ownComponents.ownLabel import OwnLabel
import numpy as np
from plot.line import LinePlot

class MXNEnvelop(GridLayout):
    
    # explorer of the cross section
    explorer = ObjectProperty()
    
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
        slider = Slider()
        slider.bind(on_value=self.update_slider)
        slideArea = GridLayout(cols=2, row_force_default=True,
                             row_default_height=Design.btnHeight, size_hint_y=None,
                             height=1.1 * Design.btnHeight)
        slideArea.add_widget(OwnLabel(text='text'))
        slideArea.add_widget(slider)
        self.add_widget(slideArea)
    
    '''
    create the graph
    '''
        
    def create_graphs(self):
        self.graphs = GridLayout(cols=2, spacing=Design.spacing)
        # create the left graph- explorer graph
        self.graphLeft = OwnGraph(
                                  x_ticks_major=0.1, y_ticks_major=0.1,
                                  y_grid_label=True, x_grid_label=True,
                                  xmin=-0.5, xmax=0.5, ymin=0, ymax=self.explorer.h)
        # create the right graph
        self.graphRight = OwnGraph(
                                 x_ticks_major=100, y_ticks_major=50,
                                 y_grid_label=True, x_grid_label=True,
                                 xmin=-0.5, xmax=400, ymin=0, ymax=350)
        self.graphs.add_widget(self.graphLeft)
        self.graphs.add_widget(self.graphRight)
        self.add_widget(self.graphs)
        
    '''
    update the graph
    '''
   
    def update_graph(self, eps_arr, M_arr, N_arr):
        h = self.explorer.h
        self.graphLeft.ymax = h
        self.graphLeft.y_ticks_major = h / 5.
        self.graphLeft.xmin = -1.2
        self.graphLeft.x_ticks_major = 0.3
        # plot left side
        n = len(eps_arr[0])
        for i in range(n):
            # print(arr)
            p = LinePlot(color=[0, 0, 0], points=[(-eps_arr[0][i], 0), (-eps_arr[1][i], h)])
            self.graphLeft.add_plot(p)
        p = LinePlot(color=[0, 0, 0], points=[(m, -n)for n, m in zip(N_arr, M_arr)])
        self.graphRight.add_plot(p)
        print(p.points)
        
    '''
    will called when the slider changes the value
    '''
   
    def update_slider(self, inst, v):
        print('not finished yet')
    
    
    '''
    calculate parameters for the plot
    '''
   
    def calculation(self):
        eps_u_r, y_r, eps_cu = self.explorer.get_coordinates_upperStrain()
        print('eps_u: ' + str(eps_u_r))
        print('y: ' + str(y_r))
        print('eps_cu: ' + str(eps_cu))
        eps_lo_arr = self.convert_eps_u_2_lo(self.explorer.minStrain, eps_u_r, y_r)
        env_reinf_idx = -1
        if eps_lo_arr:
            env_reinf_idx = np.argmin(eps_lo_arr)
        eps_ccu, n_eps = 0.8 * eps_cu, 20
        eps_arr = self.get_strain_arrays(eps_cu, eps_ccu, eps_u_r, y_r, env_reinf_idx, n_eps)
        # get the m-n envelop
        M_arr = np.zeros_like(eps_arr[0])
        N_arr = np.zeros_like(eps_arr[0])
        for i in np.arange(len(eps_arr[0])):
            result = self.explorer.calculation(eps_arr[0][i], eps_arr[1][i], n_eps)
            N_arr[i] = result[0]
            M_arr[i] = result[1]
            print('eps_lower: ' + str(eps_arr[0][i]) + ' eps_upper: ' + str(eps_arr[1][i]) + ' i: ' + str(i))
            print('N: ' + str(N_arr[i]))
            print('M: ' + str(M_arr[i]))
        self.update_graph(eps_arr, M_arr, N_arr)
    
    '''
    return the strain_arrays
    '''
        
    def get_strain_arrays(self, eps_cu, eps_ccu, eps_u_r, reinf_y_coord, env_reinf_idx, n_eps):
        n = len(self.explorer.layers) + len(self.explorer.bars)
        if n > 0:
            eps_t_lo = self.convert_eps_u_2_lo(eps_cu, eps_u_r, reinf_y_coord[env_reinf_idx])
            eps_t_lo_0 = self.convert_eps_u_2_lo(0., eps_u_r, reinf_y_coord[env_reinf_idx])
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
    
