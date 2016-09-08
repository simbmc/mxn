'''
Created on 25.08.2016
@author: mkennert
'''
from decimal import Decimal

from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.gridlayout import GridLayout

from explorer.gui import ExplorerGui
from materialEditor.materiallist import MaterialList
import numpy as np
from ownComponents.design import Design
from plot.dashedLine import DashedLine


class Explorer(GridLayout, ExplorerGui):

    '''
    the Explorer is the component which shows the stress-strain.behaviour
    of the selected cross-section-shape
    '''

    # cross-section-shape
    csShape = ObjectProperty()

    # layers of the cross-section
    layers = ListProperty([])

    # bars of the cross-section
    bars = ListProperty([])

    # height of the cross-section-shape
    h = NumericProperty()

    # minimum strain
    minStrain = NumericProperty(0.5)

    # maximum strain
    maxStrain = NumericProperty(-0.5)

    # minimum stress of the cross section
    minStress = NumericProperty()

    # maximum stress of the cross section
    maxStress = NumericProperty()

    # number of integration points
    numberIntegration = NumericProperty(100)

    # limit of the integrationpoints
    limitIntegration = NumericProperty(1e3)

    '''
    constructor
    '''

    def __init__(self, **kwargs):
        super(Explorer, self).__init__(**kwargs)
        print('create explorer')
        self.cols, self.spacing = 1, Design.spacing
        self.graphContent = GridLayout(cols=2)
        self.h = self.csShape.ch
        self.allMaterial = MaterialList.Instance()
        self.create_gui()

    '''
    update just the cs-properties and the strain-stress-diagram
    '''

    def update_csShape(self, cs, h, layers, bars):
        self.csShape = cs
        self.layers = layers
        self.bars = bars
        self.h = h

    '''
    update the whole explorer
    '''

    def update_explorer(self):
        self.minStress = self.minStrain
        self.maxStress = self.maxStrain
        self.calculation(
            self.minStrain, self.maxStrain, self.numberIntegration)
        self.plot()
        self.update_graph()

    '''
    calculate the normal force and the moment
    '''

    def calculation(self, minStrain, maxStrain, numInt):
        # number of reinforcement components
        n = len(self.layers) + len(self.bars)
        self.y_r = np.zeros(n)
        self.y_m = np.zeros(numInt)
        # reinforcement area
        self.csArea = np.zeros(n)
        self.strain_m, self.stress_m = np.zeros(numInt), np.zeros(numInt)
        self.strain_r, self.stress_r = np.zeros(n), np.zeros(n)
        # update matrix
        self.mlaw = self.allMaterial.allMaterials[3].materialLaw.f
        self.y_m = np.linspace(0, self.h, numInt)

        self.strain_m = np.interp(
            self.y_m, [0, self.h], [minStrain, maxStrain])
        self.stress_m = np.array([self.mlaw(strain)
                                  for strain in self.strain_m])
        # update all layer-lines
        index = 0
        for layer in self.layers:
            strain = np.interp(layer.y, [0, self.h], [minStrain, maxStrain])
            stress = layer.material.materialLaw.f(strain)
            self.y_r[index], self.csArea[index] = layer.y, layer.h
            self.strain_r[index], self.stress_r[index] = strain, stress
            index += 1
        # update all bar-lines
        for bar in self.bars:
            strain = np.interp(bar.y, [0, self.h], [minStrain, maxStrain])
            stress = bar.material.materialLaw.f(strain)
            self.y_r[index], self.csArea[index] = bar.y, bar.csArea
            self.strain_r[index], self.stress_r[index] = strain, stress
            index += 1
        # calculate the normal force and the moment
        stress_y = np.array([s * self.csShape.get_width(s)
                             for s in self.stress_m])
        # normal force
        N_m = np.trapz(stress_y, self.y_m)
        N_r = np.sum(self.stress_r * self.csArea)
        print('normal force: nm=' + str(N_m) + ' nr=' + str(N_r))
        N = N_m + N_r
        # moment - matrix
        gravity_center = self.csShape._get_gravity_centre()
        M_m = np.trapz(stress_y * (self.y_m - gravity_center), self.y_m)
        # moment - reinforcement
        M_r = np.sum(self.stress_r * self.csArea * (self.y_r - gravity_center))
        M = (M_m + M_r)
        self.normalForceLbl.text = str('%.2E' % Decimal(str(N)))
        self.momentLbl.text = str('%.2E' % Decimal(str(M)))
        return N, M, self.strain_m, self.stress_m, self.strain_r, self.stress_r

    '''
    plot the strain- and the stress-line of the matrix and reinforcement
    '''

    def plot(self):
        self.pMatrixStrain.points = []
        self.pMatrixStress.points = []
        for y, strain, stress in zip(self.y_m, self.strain_m, self.stress_m):
            if stress > self.maxStress:
                self.maxStress = round(stress, 2)
            elif stress < self.minStress:
                self.minStress = round(stress, 2)

            self.pMatrixStrain.points.append((strain, y))
            self.pMatrixStress.points.append((stress, y))
            # index += 1
        n = len(self.plotsStrain)
        index = 0
        for y, strain, stress in zip(self.y_r, self.strain_r, self.stress_r):
            if stress > self.maxStress:
                self.maxStress = round(stress, 2)
            elif stress < self.minStress:
                self.minStress = round(stress, 2)
            if index < n:
                self.plotsStrain[index].points = [(0, y), (strain, y)]
                self.plotsStress[index].points = [(0, y), (stress, y)]
            else:
                pStrain = DashedLine(
                    color=[255, 0, 0], points=[(0, y), (strain, y)])
                pStress = DashedLine(
                    color=[255, 0, 0], points=[(0, y), (stress, y)])
                self.plotsStrain.append(pStrain)
                self.plotsStress.append(pStress)
                self.graphStrain.add_plot(pStrain)
                self.graphStress.add_plot(pStress)
            index += 1
        while index < n:
            self.plotsStrain[index].points = [(0, 0), (0, 0)]
            self.plotsStress[index].points = [(0, 0), (0, 0)]
            index += 1

    def get_coordinates_upperStrain(self):
        n = len(self.layers) + len(self.bars)
        y_r = np.zeros(n)
        eps_cu = self.allMaterial.allMaterials[3].materialLaw.minStrain
        eps_u_r = -1e6
        index = 0.
        for layer in self.layers:
            maxStrain = layer.material.materialLaw.maxStrain
            if maxStrain > eps_u_r:
                eps_u_r = maxStrain
            y_r[index] = layer.y
            index += 1
        for bar in self.bars:
            maxStrain = layer.material.materialLaw.maxStrain
            if maxStrain > eps_u_r:
                eps_u_r = maxStrain
            y_r[index] = bar.y
            index += 1
        return eps_u_r, y_r, eps_cu
