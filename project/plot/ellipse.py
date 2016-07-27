'''
Created on 28.06.2016

@author: mkennert
'''
from math import log10

from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Line
from kivy.garden.graph import Plot


class Ellipse(Plot):
    _image = ObjectProperty()
    xrange = ListProperty([0, 100])
    yrange = ListProperty([0, 100])

    def __init__(self, **kwargs):
        super(Ellipse, self).__init__(**kwargs)
        self.bind(
            xrange=self.ask_draw, yrange=self.ask_draw)

    def create_drawings(self):
        self._image = Line(ellipse=(0,0, 0., 0.))
        return [self._image]

    def draw(self, *args):
        super(Ellipse, self).draw(*args)

        self._texture = Texture.create(size=(1, 1), colorfmt='rgb')
        self._texture.blit_buffer(
            b''.join(map(chr, self.color)), colorfmt='rgb', bufferfmt='ubyte')

        image = self._image
        image.texture = self._texture

        params = self._params
        funcx = log10 if params['xlog'] else lambda x: x
        funcy = log10 if params['ylog'] else lambda x: x
        xmin = funcx(params['xmin'])
        ymin = funcy(params['ymin'])
        size = params['size']
        ratiox = (size[2] - size[0]) / float(funcx(params['xmax']) - xmin)
        ratioy = (size[3] - size[1]) / float(funcy(params['ymax']) - ymin)

        bl = (funcx(self.xrange[0]) - xmin) * ratiox + \
            size[0], (funcy(self.yrange[0]) - ymin) * ratioy + size[1]
        tr = (funcx(self.xrange[1]) - xmin) * ratiox + \
            size[0], (funcy(self.yrange[1]) - ymin) * ratioy + size[1]
        w = tr[0] - bl[0]
        h = tr[1] - bl[1]
        image.ellipse = [bl[0], bl[1], w,h]

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

            plot = Ellipse(color=[0, 0, 0])
            graph2.add_plot(plot)

            b.add_widget(graph2)
            self.plot = plot

            Clock.schedule_interval(self.update_color, 0.1)
            Clock.schedule_interval(self.update_pos, 0.1)

            return b

        def update_color(self, *args):
            self.plot.color = [random.randint(0, 255) for r in xrange(100)]

        def update_pos(self, *args):
            self.plot.xrange = [100. * random.random() for r in xrange(2)]
            self.plot.yrange = [100. * random.random() for r in xrange(2)]

    TestApp().run()