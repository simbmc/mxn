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
    minStrain = NumericProperty(-0.5)
    
    # maximum strain
    maxStrain = NumericProperty(0.5)
    
    # minimum stress of the cross section
    minStress = NumericProperty()
    
    # maximum stress of the cross section
    maxStress = NumericProperty()
    
    # number of integration points
    numberIntegration = NumericProperty(30)
    
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
    update the cs-properties and the strain-stress-diagram
    '''
   
    def update_csShape(self, cs, h, layers, bars):
        self.csShape = cs
        self.layers = layers
        self.bars = bars
        self.h = h
        self.minStress = self.minStrain
        self.maxStress = self.maxStrain
        self.reset_explorer()
        self.update_strain_stress()
        self.plot()
        self.update_graph()
        
    '''
    update the strain-stress-behavior of the cross-section
    '''
        
    def update_strain_stress(self):
        print('update_strain_stress (explorer)')
        self.m = (self.h) / (self.maxStrain - self.minStrain)
        self.b = self.h - self.m * self.maxStrain
        print('update_matrix (explorer)')
        self.mlaw = self.allMaterial.allMaterials[3].materialLaw.f
        self.yCoordinatesMatrix = np.linspace(0, self.h, self.numberIntegration)
        self.strainMatrix = np.interp(self.yCoordinatesMatrix, [0, self.h], [self.minStrain, self.maxStrain])
        self.stressMatrix = np.array([self.mlaw(strain) for strain in self.strainMatrix])
        # update all layer-lines
        index = 0
        for layer in self.layers:
            strain = self.f(layer.y)
            stress = layer.material.materialLaw.f(strain)
            self.yRef[index] = layer.y
            self.csArea[index] = layer.h
            self.strainRef[index] = strain
            self.stressRef[index] = stress
            index += 1
        # #update all bar-lines
        for bar in self.bars:
            strain = self.f(bar.y)
            stress = bar.material.materialLaw.f(strain)
            self.yRef[index] = bar.y
            self.csArea[index] = bar.csArea
            self.strainRef[index] = strain
            self.stressRef[index] = stress
            index += 1
        self.calculate_force_moment()
    
    '''
    calculation the force and the moment of the cross-section
    '''
   
    def calculate_force_moment(self):
        stress_y = np.array([s * self.csShape.get_width(s) for s in self.stressMatrix])
        y_coord = np.array([self.yCoordinatesMatrix])
        # normal force
        N_m = np.trapz(stress_y , y_coord)
        N_r = np.sum(self.stressRef * self.csArea)
        N = N_m + N_r
        # moment - matrix
        gravity_center = self.csShape._get_gravity_centre()
        M_m = np.trapz(stress_y * (y_coord - gravity_center), y_coord)
        # moment - reinforcement
        M_r = np.sum(self.stressRef * self.csArea * (self.yRef - gravity_center))
        M = M_m + M_r
        self.normalForceLbl.text = str('%.2E' % Decimal(str(N[0])))
        self.momentLbl.text = str('%.2E' % Decimal(str(M[0])))
        print('normal force: ' + str(N))
        print('moment: ' + str(M))
    
    '''
    plot the strain- and the stress-line of the matrix and reinforcment
    '''
        
    def plot(self):
        self.clear_graph()
        for y, strain, stress in zip(self.yCoordinatesMatrix, self.strainMatrix, self.stressMatrix):
            if stress > self.maxStress:
                self.maxStress = round(stress, 2)
            elif stress < self.minStress:
                self.minStress = round(stress, 2)
            pstrain = DashedLine(color=[0, 0, 0], points=[(0, y), (strain, y)])
            pstress = DashedLine(color=[0, 0, 0], points=[(0, y), (stress, y)])
            self.graphStrain.add_plot(pstrain)
            self.graphStress.add_plot(pstress)
        for y, strain, stress in zip(self.yRef, self.strainRef, self.stressRef):
            pstrain = DashedLine(color=[255, 0, 0], points=[(0, y), (strain, y)])
            pstress = DashedLine(color=[255, 0, 0], points=[(0, y), (stress, y)])
            if stress > self.maxStress:
                self.maxStress = round(stress, 2)
            elif stress < self.minStress:
                self.minStress = round(stress, 2)
            self.graphStrain.add_plot(pstrain)
            self.graphStress.add_plot(pstress)
    
    '''
    delete the plots which represent a layer or a bar
    '''
        
    def clear_graph(self):
        print('clear_graph (explorer)')
        self.switch = False
        while len(self.graphStrain.plots) > 2 or len(self.graphStress.plots) > 1:
            for plot in self.graphStrain.plots:
                if  plot != self.pStrainCs:
                    self.graphStrain.remove_plot(plot)
                    self.graphStrain._clear_buffer()
            for plot in self.graphStress.plots:
                if plot != self.pStressCs:
                    self.graphStress.remove_plot(plot)
                    self.graphStress._clear_buffer()
        
    '''
    reset the attributes for the calculation
    '''
                    
    def reset_explorer(self):
        # coordinates of the reinforcement
        n = len(self.layers) + len(self.bars)
        m = self.numberIntegration
        self.yRef = np.zeros(n)
        self.yCoordinatesMatrix = np.zeros(m)
        # reinforcement area
        self.csArea = np.zeros(n)
        self.strainMatrix = np.zeros(m)
        self.stressMatrix = np.zeros(m)
        self.strainRef = np.zeros(n)
        self.stressRef = np.zeros(n)
    
    '''
    the function which describes the strain-line
    '''
                    
    def f(self, y):
        # y=mx+b <=> x=(y-b)/m
        return (y - self.b) / self.m
