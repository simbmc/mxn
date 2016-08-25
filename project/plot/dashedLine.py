'''
Created on 27.06.2016

@author: mkennert
'''
from math import log10

from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Line,RenderContext
from kivy.garden.graph import Plot, Color, Mesh

class DashedLine(Plot):
    
    '''
    draw a dashed-line by the given color
    '''
    
    def __init__(self, **kwargs):
        super(DashedLine, self).__init__(**kwargs)
    
    def create_drawings(self):
        self._mesh = Mesh(mode='lines')
        self._grc = RenderContext(
                use_parent_modelview=True,
                use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(points=[], width=1,dash_offset=5,dash_length=10)
        return [self._grc]
    
    def draw(self, *args):
        super(DashedLine, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        with self._grc:
            self._gcolor = Color(*self.color)
        self._gline.points = points