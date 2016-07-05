from math import log10

from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Line,RenderContext
from kivy.garden.graph import Plot, Color, Mesh

class LinePlot(Plot):
    width=1.
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
    
if __name__ == '__main__':
    from kivy.uix.boxlayout import BoxLayout
    from kivy.app import App
    from kivy.garden.graph import Graph
    import random
    from kivy.clock import Clock

    class TestApp(App):

        def build(self):
            b = BoxLayout(orientation='vertical')

            graph2 = Graph(
                xlabel='x',
                ylabel='y',
                x_ticks_major=10,
                y_ticks_major=10,
                y_grid_label=True,
                x_grid_label=True,
                padding=5,
                xlog=False,
                ylog=False,
                xmin=0,
                ymin=0)

            plot = LinePlot(color=[255, 0, 0,1])
            plot.points = [(0,0),(100, 100)]
            plot.width=1.5
            graph2.add_plot(plot)

            b.add_widget(graph2)
            self.plot = plot

            Clock.schedule_interval(self.update_color, 1)
            Clock.schedule_interval(self.update_pos, 1)

            return b

        def update_color(self, *args):
            self.plot.color = [random.randint(0, 255) for r in xrange(3)]

        def update_pos(self, *args):
            self.plot.points = [(0,0),(random.randint(0, 100),random.randint(0, 100))]

    TestApp().run()