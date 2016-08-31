'''
Created on 18.04.2016
@author: Yingxiong
'''
from math import log10

from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Line
from kivy.garden.graph import Plot


class Circle(Plot):

    '''
    draw a circle for given color and geometric parameters,
    the radius is automatically scaled to guarantee that the
    circle is still a perfect when the ratio of the graph is not 1:1
    '''
    
    _image = ObjectProperty()
    pos = ListProperty([0, 0])  # center
    d = NumericProperty(0.)  # radius
    color = ListProperty([255, 255, 255])

    def __init__(self, **kwargs):
        super(Circle, self).__init__(**kwargs)
        self.bind(
            color=self.ask_draw, pos=self.ask_draw, d=self.ask_draw)

    def create_drawings(self):
        self._image = Line(circle=[0., 0., 0.])
        return [self._image]

    def draw(self, *args):
        super(Circle, self).draw(*args)

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

        bl = (funcx(self.pos[0]) - xmin) * ratiox + \
            size[0], (funcy(self.pos[1]) - ymin) * ratioy + size[1]
        radius = min(self.d * ratiox, self.d * ratioy)
        image.circle = [bl[0], bl[1], radius]
