'''
Created on 02.09.2016

@author: mkennert
'''
from decimal import Decimal

from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

import numpy as np
from mxnenvelope.gui import EnvelopeGui


class MXNEnvelop(GridLayout, EnvelopeGui):

    # explorer of the cross section
    explorer = ObjectProperty()

    n_eps = NumericProperty(20)

    # number of plots 4*n_eps
    n_plt = NumericProperty(80)
    
    forceStr = StringProperty('force [kN]')
    
    momentStr = StringProperty('moment [kN.m]')
    
    strainStr = StringProperty('strain')
    
    heightStr = StringProperty('height [m]',)
    
    '''
    constructor
    '''

    def __init__(self, **kwargs):
        super(MXNEnvelop, self).__init__(**kwargs)
        self.cols = 1
        self.create_gui()

    '''
    calculate parameters for the plot
    '''

    def calculation(self):
        eps_u_r, y_r, eps_cu = self.explorer.get_coordinates_upperStrain()
        eps_lo_arr = self.convert_eps_u_2_lo(
            self.explorer.maxStrain, eps_u_r, y_r)
        env_reinf_idx = -1
        if len(eps_lo_arr) > 0:
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
        self.N_arr *= 1000.
        self.M_arr *= 1000.
        self.update_graph(self.eps_arr, self.M_arr, self.N_arr)
        self.slider.max = len(self.eps_arr[0]) - 1
        self.focusLine.points = [
            (-self.eps_arr[0][0], 0), (-self.eps_arr[1][0], self.explorer.h)]
        self.focusPoint.xrange = [-self.M_arr[0] - 
                                  self.eps_x, -self.M_arr[0] + self.eps_x]
        self.focusPoint.yrange = [-self.N_arr[0] - 
                                  self.eps_y, -self.N_arr[0] + self.eps_y]
        self.slider.value = 0
        self.normalForceLbl.text = 'N: '+str('%.2E' % Decimal(str(-self.N_arr[0])))
        self.momentLbl.text = 'M: '+str('%.2E' % Decimal(str(-self.M_arr[0])))

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
