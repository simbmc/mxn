'''
Created on 28.06.2016

@author: mkennert
'''

from kivy.graphics import Line, RenderContext
from kivy.garden.graph import Plot, Color, Mesh

class LinePlot(Plot):
    
    '''
    draw a line by the given color
    '''
    
    width = 1.
    
    def __init__(self, **kwargs):
        super(LinePlot, self).__init__(**kwargs)
    
    def create_drawings(self):
        self._mesh = Mesh(mode='lines')
        self._grc = RenderContext(
                use_parent_modelview=True,
                use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(points=[], width=self.width)
        return [self._grc]
    
    def draw(self, *args):
        super(LinePlot, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        with self._grc:
            self._gcolor = Color(*self.color)
        self._gline.points = points