'''
Created on Mar 7, 2012

@author: Armand Gutierrez Arumi


        Macroevolve is an application to try different algorithms to maximize(minimize) 
        a given function.
        
        Maximize(Minimize) a given function using genetic o macroevolutionary algorithms.

'''
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
from algorithms.random_alg import Population_random, Random_alg,\
    Random_alg_params

import wx
from wxPython.wx import *


def functionXY(x,y):
    '''
    Some nice base function.
    '''
    #return x**2+y**2
    dist = math.sqrt((x*x)+(y*y))
    return ( dist+math.sin(2*dist)  )/( 100+dist)

class Point(object):
    '''
    Base point
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def __repr__(self):
        return("({0},{1})".format(self.x,self.y))

# Quit this
glb_alg_choice = 0;

glb_algorithms = {}
glb_algorithms[0] = "Pseudo ME"
glb_algorithms[1] = "Genetic Algorithm"
glb_algorithms[2] = "Random"


import wx
class GraphicPlot(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent,-1)
        
        '''
        Base map contains the region to plot.
        By default an XY plane between (-10,-10) and (10,10)
        '''
        self.upper_limit=10
        self.lower_limit=-10
        self.npts = 500
        self.function = functionXY
        self.points = []
        # Add Countor graph
        self.new_countour()
        
        '''
        Base parameters (from GUI).
        '''  
        # N of people      
        self.__number_population = 3
        
        # The algorithm is the kind of population
        params = Random_alg_params(self.__number_population)
        self.__fitness_alg = Random_alg(params)
      
        # Distributes the population among the map 
        self.init_population()
        
    
    def init_population(self):
        '''
        Initializes a certain population (with his kind)
        '''
        self.__fitness_alg.new_population()
        
        
    def new_countour(self):
        '''
        It draws a new map and also inits new population
        '''
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
        
        # Distributes the population among the map 
        #self.init_population()
        
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
        
        '''One step more, apply the algorithm'''
        self.draw_base_plot()
        
        self.__fitness_alg.update_population()
        
        # Plot each individual
        for indy in self.__fitness_alg.get_individuals():
            self.axes.plot(indy.x,indy.y,'wo',ms=5)
            
        
        self.figure.canvas.draw()

       
# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    '''Define Result Event.'''
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    '''Simple event to carry arbitrary result data.'''
    def __init__(self, data):
        '''Init Result Event.'''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        
class CronoThread(Thread):
    '''Crono engine that calculates the ticks in simulation.'''
    def __init__(self, notify_window, foo_gen_ticks):
        '''Init Worker Thread Class.'''
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        
        # Function
        self.gen_ticks = foo_gen_ticks
        
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        '''Run Crono Thread.'''
        self._want_abort = False
        for one_step_more in self.gen_ticks():
            print "step!"
            # Need to update the ResultEvent ! (we cannot pass directly the function )
            wx.PostEvent(self._notify_window, ResultEvent(True))
            if self._want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
       
    def abort(self):
        '''abort crono thread.'''
        # Method for use by main thread to signal an abort
        self._want_abort = 1
    
    
class MainFrame(wx.Frame):
    '''
    MainFrame of the application (the controls and the window).
    '''
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))

        # Add the main widget
        self.add_widgetPanel()
        
        # In construction ...
        #self.add_widgetMenu()
        
        # Status bar
        self.statusbar = self.CreateStatusBar()
        
        # Event status
        self.pause = False
        self.tic_time = 1.5 # Seconds
        
        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.on_result_event)
        self.crono_worker = None
        
        # Add the control
        self.add_control_panel()
        
    def add_widgetPanel(self):
        '''
        It adds the main control and graph zone
        '''
        self.sp = wx.SplitterWindow(self)
        self.p1 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        self.gp = GraphicPlot(self.sp)
        self.sp.SplitVertically(self.p1, self.gp, 170)

    def add_control_panel(self):

        # Buttons
        self.runButton = wx.Button(self.p1, -1, "run", size=(55,30), pos=(10,10))
        self.runButton.Bind(wx.EVT_BUTTON, self.run_event)
        
        self.stepButton = wx.Button(self.p1, -1, "step", size=(55,30), pos=(10,40))
        self.stepButton.Bind(wx.EVT_BUTTON, self.step_event)
        
        self.pauseButton = wx.Button(self.p1, -1, "pause", size=(55,30), pos=(10,70))
        self.pauseButton.Bind(wx.EVT_BUTTON, self.pause_event)

        # List of algorithms
        list_algorithms = glb_algorithms.values()
        self.comboAlg = wx.ComboBox(self.p1, -1, value=(list_algorithms[0]), size=(120,30), pos=(10,130), choices=list_algorithms, style=wx.TE_PROCESS_ENTER)
        self.comboAlg.SetToolTip(wx.ToolTip("select algorithm to test"))


        self.comboAlg.Bind(wx.EVT_COMBOBOX, self.update_choice_alg)


        # Population selector (by now fixed... then i change this
        #self.size_populus

        # Create the static text widget and set the text
        self.add_population_widget( 10,170 )
        

    def add_population_widget(self, pos_x, pos_y):
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wxStaticText(self, label="Enter some text:")
        sizer.Add(self.text, proportion=0,  border=5)
        sizer.AddSpacer(2) 
        # or sizer.Add((0,0))
        self.edit = wxTextCtrl(self, size=wx.Size(70, -1))
        sizer.Add(self.edit, proportion=0,  border=5)

        """
        # Horizontal sizer
        self.h_sizer = wxBoxSizer(wx.HORIZONTAL)
        #, pos=(pos_x, pos_y)
        # Create the static text widget and set the text
        self.text = wxStaticText(self, label="Enter some text:")
        #Create the Edit Field (or TextCtrl)
        self.edit = wxTextCtrl(self, size=wx.Size(70, -1))
        #self.size_populus_wdg = wxTextCtrl(self, -1,"10",size=(120, 30), pos=position)
        
        #Add to horizontal sizer
        #add the static text to the sizer, tell it not to resize
        self.h_sizer.Add(self.text, 0,)
        #Add 5 pixels between the static text and the edit
        self.h_sizer.AddSpacer((5,0))
        #Add Edit
        self.h_sizer.Add(self.edit, 1)
        
        #Set the sizer
        self.SetSizer(self.h_sizer)
        """

    def update_choice_alg(self, event):
        # By now global variable, fix this
        alg = event.GetSelection()
        #

    def add_widgetMenu(self):
        # Creating the menubar.
        
        # Id does not work.. 
        """
        menuBar = wxMenuBar()
        menuBar.Append(self.get_menu_file(),"&File") # Adding the "filemenu" to the MenuBar
        #menuBar.Append(self.get_menu_config(),"&Settings")
        #menuBar.Append(self.get_menu_run(),"&Run") 
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        """
        
        """
        menu = wxMenu()
        menu.Append(wx.ID_ABOUT, "&About", "More information about this program")
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        menuBar = wxMenuBar()
        menuBar.Append(menu, "&File");
        self.SetMenuBar(menuBar)
        """
        
        
    def get_menu_file(self):
        # Setting up the menu.
        filemenu= wxMenu()
        
        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
    
        """
        menu = wxMenu()
        menu.Append(ID_ABOUT, "&About", "More information about this program")
        menu.AppendSeparator()
        menu.Append(ID_EXIT, "E&xit", "Terminate the program")
        menuBar = wxMenuBar()
        menuBar.Append(menu, "&File");
        """

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        return filemenu


    def get_menu_config(self):
        # Setting up the menu.
        filemenu= wx.Menu()
         
        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&Config","Configurating the program")
    
        # Set events.
        #self.Bind(wx.EVT_MENU, self.OnChangeDepth, menuAbout)
        
        return filemenu

    def get_menu_run(self):
        # Setting up the menu.
        filemenu= wx.Menu()
        return filemenu


    def OnAbout(self,e):
        """
        Macroevolutionary algorithm
        """
        msg = """
Simple plataform to simulate methods to minimize algorithms.\n
Some of implemented algorithms:\n    macroevolutionary algorithm."
        """
        dlg = wx.MessageDialog( self, msg,"About", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
     
    def OnExit(self,e):
        self.Close(True)  # Close the frame.

        
    def run_event(self,event):
        #self.statusbar.setStatusText("Running")
        print("Running...")
        if not self.crono_worker:
            self.crono_worker = CronoThread(self, self.ticks)
            #thread.start_new_thread(self.go_ticks,())
    
    def step_event(self,sevent):
        self.gp.do_step()
        if self.crono_worker != None:
            self.crono_worker.abort()
        self.crono_worker = None
        
    def pause_event(self,event):
        #self.pause = True
        print "pause! Is crono : {0}".format(self.crono_worker != None)
        if self.crono_worker != None:
            self.crono_worker.abort()
            self.crono_worker = None
            
    def on_result_event(self, event):
        '''Trick to show result status, otherwise it crashes.'''
        if event.data is True:
            self.gp.do_step()
        else:
            if self.crono_worker != None:
                self.crono_worker.abort()
                self.crono_worker = None


    def ticks(self):
        '''
        Hommade function to control the maximum number of ticks
        '''
        t = 0
        while t < 100000:
            if (self.pause):
                raise StopIteration

            time.sleep(self.tic_time)
            t=t+1
            yield t

'''
(The MIT License)

Copyright (c) 2012 Armand Gutierrez Arumi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
if __name__ == "__main__":
    	
    app = wx.App(redirect=False)
   
    frame = MainFrame(None, "Main Frame")
    frame.Show()
 
    app.MainLoop()
