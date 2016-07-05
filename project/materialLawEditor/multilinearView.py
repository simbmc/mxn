'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot


class MultilinearView(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(MultilinearView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.create_points(5)

    '''
    create the graph of the view
    '''

    def create_graph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=10, y_ticks_major=10,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=50, ymin=0, ymax=50)
        self.add_widget(self.graph)

    '''
    create the points 
    '''

    def create_points(self, n):
        self._points = []
        self.lines = []
        d = 100.
        self.epsX = self.graph.xmax / d
        self.epsY = self.graph.ymax / d
        c = (self.graph.xmax - 2) / n
        i = self.graph.xmax / n
        while n > 0:
            p = FilledEllipse(color=[255, 0, 0])
            p.xrange = [c - self.epsX, c + self.epsX]
            p.yrange = [c - self.epsY, c + self.epsY]
            self._points.append(p)
            self.graph.add_plot(p)
            c += i
            n -= 1
        self.draw_lines()

    '''
    reaction when the user move touch on the graph 
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.editor.w
        y = (touch.y - y0) / gh * self.editor.h
        for p in self._points:
            if p.xrange[0] <= x and p.xrange[1] >= x \
                    and p.yrange[0] <= y and p.yrange[1] >= y:
                p.color = Design.focusColor
            else:
                if p.color == Design.focusColor:
                    p.color = [255, 0, 0]

    '''
    reaction when the user move over the graph
    '''

    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.editor.w
        y = (touch.y - y0) / gh * self.editor.h
        for i in range(len(self._points)):
            p = self._points[i]
            if p.color == Design.focusColor:
                l=len(self._points)
                x1=self._points[i-1].xrange[0]
                if i<l-1:
                    x2=self._points[i+1].xrange[0]
                print('x: '+str(x))
                print('y: '+str(y))
                if (x>0 and y>0 and x<self.editor.w and y<self.editor.h) and \
                   ((x>x1 and i<l-1 and x2>x) or (i==0 and x<x2) or (i==l-1 and x>x1)):
                    p.xrange = [x - self.epsX, x + self.epsX]
                    p.yrange = [y - self.epsY, y + self.epsY]
                    if i==l-1:
                        self.lines[i].points[1]=(x,y)
                    else:
                        self.lines[i].points[1]=(x,y)
                        self.lines[i+1].points[0]=(x,y)
                

    # not finished yet
    def draw_lines(self):
        counter=0
        for i in range(len(self._points)):
            counter+=1
            print(counter)
            if i == 0:
                line = LinePlot(points=[(0, 0), (self._points[i].xrange[0] + self.epsX, self._points[i].yrange[0] + self.epsY)],
                                color=[255, 255, 255])
            else:
                line = LinePlot(points=[(self._points[i - 1].xrange[0] + self.epsX, self._points[i - 1].yrange[0] + self.epsY),
                                        (self._points[i].xrange[0] + self.epsX, self._points[i].yrange[0] + self.epsY)],
                                color=[255, 255, 255])
            self.lines.append(line)
            self.graph.add_plot(line)

    '''
    update the width of the graph
    '''

    def update_width(self):
        self.graph.xmax = self.editor.w
        self.graph.x_ticks_major=self.graph.xmax/5.
        d = 100.
        curX = self.graph.xmax / d
        for point in self._points:
            x = point.xrange[0] + self.epsX
            point.xrange = [x - curX, x + curX]
        self.epsX = curX
    '''
    update the height of the graph
    '''

    def update_height(self):
        self.graph.ymax = self.editor.h
        self.graph.y_ticks_major=self.graph.ymax/5.
        d = 100.
        curY = self.graph.ymax / d
        for point in self._points:
            y = point.yrange[0] + self.epsY
            point.yrange = [y - curY, y + curY]
        self.epsY = curY
    '''
    update the number of points
    '''

    def update_points(self):
        # clear all points and lines
        while len(self.graph.plots) > 0:
            for plot in self.graph.plots:
                self.graph.remove_plot(plot)
                self.graph._clear_buffer()
        # draw the new points and lines
        self.create_points(self.editor.get_points())

    '''
    sign in by the parent
    '''

    def sign_in(self, parent):
        self.editor = parent
