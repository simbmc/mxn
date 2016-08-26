'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
from kivy.properties import  ObjectProperty, StringProperty

class MultilinearView(GridLayout):
    
    # important components
    editor = ObjectProperty()
    
    # strings
    strainStr, stressStr = StringProperty('strain '), StringProperty('stress [MPa]')
    
    # constructor
    def __init__(self, **kwargs):
        super(MultilinearView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.create_points(self.editor._points)

    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.stressStr, ylabel=self.strainStr,
                           x_ticks_major=self.editor.upperStress / 5.,
                           y_ticks_major=self.editor.upperStrain / 5.,
                           x_grid=True, y_grid=True,
                           y_grid_label=True, x_grid_label=True,
                           xmin=self.editor.lowerStress, xmax=self.editor.upperStress,
                           ymin=self.editor.lowerStrain, ymax=self.editor.upperStrain)
        self.add_widget(self.graph)

    '''
    create the points. draw the points of the diagonal of the graph 
    '''
    def create_points(self, n):
        self._points, self.lines = [], []
        self.epsX = self.graph.xmax / Design.barProcent
        self.epsY = self.graph.ymax / Design.barProcent
        w, h = self.graph.xmin, self.graph.ymin
        wi = (self.graph.xmax - self.graph.xmin) / n
        hi = (self.graph.ymax - self.graph.ymin) / n
        overZero = False
        while n > 0:
            p = FilledEllipse(color=[255, 0, 0], xrange=[w - self.epsX, w + self.epsX],
                              yrange=[h - self.epsY, h + self.epsY])
            self._points.append(p)
            self.graph.add_plot(p)
            w += wi
            h += hi
            n -= 1
            if w > 0 and not overZero:
                p = FilledEllipse(color=[255, 0, 0],
                                                  xrange=[-self.epsX, self.epsX],
                                                  yrange=[-self.epsY, self.epsY])
                self._points.append(p)
                self.graph.add_plot(p)
                overZero = True
        self.draw_lines()

    '''
    draw the lines between the points
    '''
    def draw_lines(self):
        counter = 0
        for i in range(len(self._points)):
            counter += 1
            print(counter)
            if i == 0:
                line = LinePlot(points=[(0, 0), (self._points[i].xrange[0] + self.epsX,
                                                 self._points[i].yrange[0] + self.epsY)],
                                color=[255, 0, 0])
            else:
                line = LinePlot(points=[(self._points[i - 1].xrange[0] + self.epsX,
                                         self._points[i - 1].yrange[0] + self.epsY),
                                        (self._points[i].xrange[0] + self.epsX,
                                         self._points[i].yrange[0] + self.epsY)],
                                color=[255, 0, 0])
            self.lines.append(line)
            self.graph.add_plot(line)
    
    '''
    update the whole graph
    '''
    def update_graph(self):
        self.graph.ymax = self.editor.upperStrain
        self.graph.ymin = self.editor.lowerStrain
        self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 5.
        self.graph.xmax = self.editor.upperStress
        self.graph.xmin = self.editor.lowerStress
        self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 5.
        d = 50.
        curX = self.graph.xmax / d
        curY = self.graph.ymax / d
        for point in self._points:
            y = point.yrange[0] + self.epsY
            point.yrange = [y - curY, y + curY]
            x = point.xrange[0] + self.epsX
            point.xrange = [x - curX, x + curX]
        self.epsY = curY
        self.epsX = curX
        self.update_points()
        
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
        self.create_points(self.editor._points)
    
    '''
    when the user change the x-coordinate of a point
    '''
    def update_point_position(self, x, y):
        l = len(self._points)
        for i in range(l):
            if self._points[i].color == Design.focusColor:
                if i == l - 1 and x > self._points[i - 1].xrange[0] + self.epsX:
                    self._points[i].xrange = [x - self.epsX, x + self.epsX]
                    self._points[i].yrange = [y - self.epsY, y + self.epsY]
                    self.lines[i].points[1] = (x, y)
                elif i == 0 and x < self._points[i + 1].xrange[0] + self.epsX:
                    self.lines[i].points[1] = (x, y)
                    self.lines[i + 1].points[0] = (x, y)
                    self._points[i].xrange = [x - self.epsX, x + self.epsX]
                    self._points[i].yrange = [y - self.epsY, y + self.epsY]
                elif x < self._points[i + 1].xrange[0] + self.epsX and x > self._points[i - 1].xrange[0] + self.epsX:
                    self.lines[i].points[1] = (x, y)
                    self.lines[i + 1].points[0] = (x, y)
                    self._points[i].xrange = [x - self.epsX, x + self.epsX]
                    self._points[i].yrange = [y - self.epsY, y + self.epsY]
                else:
                    print('false input')
    
    '''
    returns the coordinate of the points
    '''
    def get_coordinates(self):
        x = [p.xrange[0] + self.epsX for p in self._points]
        y = [p.yrange[0] + self.epsY for p in self._points]
        return x, y
    
    '''
    reaction when the user move touch on the graph 
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        x0 += self.pos[0]
        y0 += self.pos[1]  
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.graph.xmax - self.graph.xmin) + self.graph.xmin
        y = (touch.y - y0) / gh * (self.graph.ymax - self.graph.ymin) + self.graph.ymin
        for p in self._points:
            if p.xrange[0] <= x and p.xrange[1] >= x \
                    and p.yrange[0] <= y and p.yrange[1] >= y:
                # the point (0,0) can't get the focus
                if p.xrange == [-self.epsX, self.epsX] and p.yrange == [-self.epsY, self.epsY]:
                    return
                p.color = Design.focusColor
                self.editor.information.update_coordinates(x, y)
            else:
                if p.color == Design.focusColor:
                    p.color = [255, 0, 0]

    '''
    reaction when the user move over the graph
    '''

    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        x0 += self.pos[0]
        y0 += self.pos[1]  
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * (self.graph.xmax - self.graph.xmin) + self.graph.xmin
        y = (touch.y - y0) / gh * (self.graph.ymax - self.graph.ymin) + self.graph.ymin
        l = len(self._points)
        for i in range(l):
            p = self._points[i]
            if p.color == Design.focusColor:
                x1 = self._points[i - 1].xrange[0]
                if i < l - 1:
                    x2 = self._points[i + 1].xrange[0]
                if (x > self.graph.xmin and y > self.graph.ymin and \
                    x < self.graph.xmax and y < self.graph.ymax) and \
                   ((x > x1 and i < l - 1 and x2 > x) or (i == 0 and x < x2)\
                     or (i == l - 1 and x > x1)):
                    p.xrange = [x - self.epsX, x + self.epsX]
                    p.yrange = [y - self.epsY, y + self.epsY]
                    self.editor.information.update_coordinates(x, y)
                    if i == l - 1:
                        self.lines[i].points[1] = (x, y)
                    else:
                        self.lines[i].points[1] = (x, y)
                        self.lines[i + 1].points[0] = (x, y)
