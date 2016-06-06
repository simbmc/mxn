'''
Created on 03.05.2016

@author: mkennert
'''
from math import log10

from kivy.graphics import Line
from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty

from kivy.garden.graph import Plot


class LinePlot(Plot):
    '''
    draw a filled rectangular for given color and geometric parameters
    '''
    _image = ObjectProperty()
    xrange = ListProperty([0, 100])
    yrange = ListProperty([0, 100])
    color = ListProperty([255, 255, 255])
    
    def __init__(self, **kwargs):
        super(LinePlot, self).__init__(**kwargs)
        self.bind(
            color=self.ask_draw, xrange=self.ask_draw, yrange=self.ask_draw)
    
    def create_drawings(self):
        self._image = Line(points=(0.,0.,1,1),width=2)
        return [self._image]

    def draw(self, *args):
        super(LinePlot, self).draw(*args)
        self._texture = Texture.create(size=(1, 1), colorfmt='rgb')
        self._texture.blit_buffer(
            b''.join(map(chr, self.color)), colorfmt='rgb', bufferfmt='ubyte')
        image = self._image
        image.texture = self._texture
        print('point1: '+str((self.xrange[0],self.yrange[0])))
        print('point2: '+str((self.xrange[1],self.yrange[1])))
        image.points=(self.xrange[0],self.yrange[0],self.xrange[1],self.yrange[1])
        print(image.points)
        image.width=1
        