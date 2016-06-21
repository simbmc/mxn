from math import log10

from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Line
from kivy.garden.graph import Plot, Color, Mesh

class LinePlot(Plot):
    def __init__(self, **kwargs):
        super(LinePlot, self).__init__(**kwargs)
    
    def create_drawings(self):
        from kivy.graphics import Line, RenderContext
        self._mesh = Mesh(mode='lines')
        self._grc = RenderContext(
                use_parent_modelview=True,
                use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(points=[], width=1,dash_offset=5,dash_length=10)
        return [self._grc]
    
    def draw(self, *args):
        super(LinePlot, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        self._gline.points = points
        


