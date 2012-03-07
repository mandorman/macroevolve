"""
Author : Armand Gutierrez Arumi

         Maximize/Minimize a given function using genetic o macroevolutionary algorithms.
"""
from numpy import *
from numpy.random import uniform, seed

#matplotlib.use('GTKAgg') # This must be done before importing pylab
import matplotlib

from matplotlib.mlab import griddata
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

import pylab as p
import time as t
import math as m
import time
from threading import *
import thread

def functionXY(x,y):
    """
    Some nice base function.
    """
    #return x**2+y**2
    dist = math.sqrt((x*x)+(y*y))
    return ( dist+math.sin(2*dist)  )/( 100+dist)

class Point(object):
    """
    Base point
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def __repr__(self):
        return("({0},{1})".format(self.x,self.y))
    

import wx
class GraphicPlot(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent,-1)
        
        """
        Base map contains the region to plot.
        By default an XY plane between (-10,-10) and (10,10)
        """
        self.upper_limit=10
        self.lower_limit=-10
        self.npts = 500
        self.function = functionXY
        self.points = []
        # Add Countor graph
        self.new_countour()
        
    def new_countour(self):
        
        # Once every time..
        self.xi = linspace(self.lower_limit-0.1, self.upper_limit+0.1, self.npts)
        self.yi = linspace(self.lower_limit-0.1, self.upper_limit+0.1, self.npts)

        self.x = []
        self.y = []
        self.z = []
        
        #seed(0)
        self.x = uniform(self.lower_limit, self.upper_limit, self.npts)
        self.y = uniform(self.lower_limit, self.upper_limit, self.npts)
        for index in range(0,len(self.x)):
            self.z.append(functionXY(self.x[index],self.y[index]))             
    
        self.zgrid = griddata(self.x,self.y,self.z,self.xi,self.yi)
        
        self.draw_base_plot()
        
    def draw_base_plot(self):
        # Configure graph
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.cla()
        self.axes.contour(self.xi, self.yi, self.zgrid,linewidths=0.5,colors='k')
        self.axes.contourf(self.xi, self.yi, self.zgrid)
        self.canvas = FigureCanvas(self, -1, self.figure)


    def add(self, point):
        self.points.append(point)
        
    def clear(self):
        self.points = []

    def do_step(self):
        """One step more"""
        
        self.draw_base_plot()
        
        for p in range(10):
            print("{} ".format(p))
            x = int(random.rand()*4)
            y = int(random.rand()*7)
            self.axes.plot(x,y,'wo',ms=5)
    
        self.figure.canvas.draw()

         
    def draw(self):
        
        for i in range(10):
            t.sleep(3)
            self.clear()
            # Add some individuals
        
            numberInd = 10
            for i in range(numberInd):
                #x =(self.lower_limit,self.upper_limit,1)
                #y = uniform(self.lower_limit,self.upper_limit,1)
                point = Point(4,2)
                #print(point)
                print("{0},{1}".format(point.x, point.y))
                self.axes.plot(point.x,point.y,'wo',ms=5)
            #self.axes.draw()
            #self.axes.show()

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        
class CronoThread(Thread):
    """Crono engine that calculates the ticks in simulation."""
    def __init__(self, notify_window, foo_gen_ticks):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        
        # Function
        self.gen_ticks = foo_gen_ticks
        
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run Crono Thread."""
        self._want_abort = False
        for one_step_more in self.gen_ticks():
            print "step!"
            # Need to update the ResultEvent ! (we cannot pass directly the function )
            wx.PostEvent(self._notify_window, ResultEvent(True))
            if self._want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
       
    def abort(self):
        """abort crono thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
    
class MainFrame(wx.Frame):
    """
    MainFrame of the application (the controls and the window).
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))

        self.sp = wx.SplitterWindow(self)
        self.p1 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        self.gp = GraphicPlot(self.sp)
        self.sp.SplitVertically(self.p1, self.gp, 100)
        
        # Status bar
        self.statusbar = self.CreateStatusBar()
        
        # Event status
        self.pause = False
        self.tic_time = 1.5 # Seconds
        
        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.on_result_event)
        self.crono_worker = None
        
        # Button
        self.runButton = wx.Button(self.p1, -1, "run", size=(50,30), pos=(10,10))
        self.runButton.Bind(wx.EVT_BUTTON, self.run_event)
        
        self.stepButton = wx.Button(self.p1, -1, "step", size=(50,30), pos=(10,40))
        self.stepButton.Bind(wx.EVT_BUTTON, self.step_event)
        
        self.pauseButton = wx.Button(self.p1, -1, "pause", size=(50,30), pos=(10,70))
        self.pauseButton.Bind(wx.EVT_BUTTON, self.pause_event)
        
    def run_event(self,event):
        #self.statusbar.setStatusText("Running")
        print("Running...")
        if not self.crono_worker:
            self.crono_worker = CronoThread(self, self.ticks)
            #thread.start_new_thread(self.go_ticks,())
    
    def go_ticks(self):
        """
        for one_step_more in self.ticks():
            print "step!"
            self.gp.do_step()
        """
    
    def step_event(self,sevent):
        self.gp.do_step()
        self.crono_worker = None
        
    def pause_event(self,event):
        #self.pause = True
        print "pause! Is crono : {0}".format(self.crono_worker != None)
        if self.crono_worker != None:
            self.crono_worker.abort()
            self.crono_worker = None
            
    def on_result_event(self, event):
        """Trick to show result status, otherwise it crashes."""
        if event.data is True:
            self.gp.do_step()
        else:
            if self.crono_worker != None:
                self.crono_worker.abort()
                self.crono_worker = None


    def ticks(self):
        """
        Hommade function to control the maximum number of ticks
        """
        t = 0
        while t < 100000:
            if (self.pause):
                raise StopIteration

            time.sleep(self.tic_time)
            t=t+1
            yield t

if __name__ == "__main__":
    	
    app = wx.App(redirect=False)
   
    frame = MainFrame(None, "Main Frame")
    frame.Show()
 
    app.MainLoop()

