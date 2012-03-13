'''
Created on Mar 9, 2012

@author: armand
'''
import random
import math
from matplotlib.mlab import griddata


'''
//////////////////////////////////////////////////////////////////////////////////
  Functions to test

    Now only put all the functions right here.
    The idea should be serialize it to JSON, and let import functions as objects.
//////////////////////////////////////////////////////////////////////////////////
'''

def functionXY(x,y):
    '''
    Some nice base function.
    '''
    #return x**2+y**2
    dist = math.sqrt((x*x)+(y*y))
    return ( dist+math.sin(2*dist)  )/( 100+dist)

def calculate_gaussian(disp, x_center, y_center, x,y):
    '''
    Base function to calculate gaussians 
    '''
    # Centered on (x-xo)**2
    
    f_x = (x - x_center)**2/(2*disp**2 )
    f_y = (y - y_center)**2/(2*disp**2 )
    e_factor = -1* math.exp( f_x + f_y )
    res = 2/e_factor
    #     print "Value e_factor {0} and {1} with a base dist of {2}".format(e_factor, res, disp )

    return res 

def function_G1_XY(x,y):
    '''
    Gaussian 1
    (i try to use several ones ... )
    '''
    res = calculate_gaussian(2, 0, 3,x,y)
    res = res + calculate_gaussian(4, 5, 3,x,y)
    
    return res

def function_G2_XY(x,y):
    '''
    Other combination (sum of gaussians)
    '''
    res = calculate_gaussian(3, -2, -7,x,y)
    res = res + calculate_gaussian(2, -5, -3,x,y)
    res = res + function_G1_difficult_XY(x,y)
    res = res + calculate_gaussian(3, 9, 4,x,y)
    
    return res

def function_G3_XY(x,y):
    '''
    Other combination (sum of gaussians)
    '''
    res = calculate_gaussian(2, -2, 9,x,y)
    res = res + calculate_gaussian(4, -5, -3,x,y)
    res = res + calculate_gaussian(3, 9, 4,x,y)
    return res

def function_G1_difficult_XY(x,y):
    '''
    Gaussian very difficult
    (i try to use several ones ... )
    '''
    dist = math.sqrt((x*x)+(y*y))
    e_factor = -1* math.exp(( dist+math.sin(2*dist)  ))
    
    return 10/e_factor

def function_G1_very_very_difficult_XY(x,y):
    '''
    Gaussian (lots of pics..) --> here the macroevolutionary algorithm could work fine ..
    '''
    dist = math.sqrt((x*x)+(y*y))
    e_factor = -1* math.exp(( dist+math.sin(2*dist)  ))
    
    res = 10*math.exp(dist)/e_factor 
    return res

'''
////////////////////////////////////////
  Object to manage functions
////////////////////////////////////////
'''

class FunctionsXY(object):
    '''
    Set of functions to test
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        # Core function
        self.__function = functionXY
        
        # Set of functions
        self.__functions = []
        self.__functions.append(functionXY)
        self.__functions.append(function_G1_XY)
        self.__functions.append(function_G2_XY)
        self.__functions.append(function_G3_XY)
        self.__functions.append(function_G1_difficult_XY)
    
    def get_function(self):
        '''
        Get the core function
        '''
        return self.__function
     
    def get_random_function(self):
        '''
        Get some random function
        '''
        r = random.randint(0,len(self.__functions)-1)
        self.__function = self.__functions[r]
        return self.__function
        
if __name__ == "__main__":
    '''
    Just to do quick test of the functions
    '''
    import matplotlib.pyplot as p
    from numpy import *
    from numpy.oldnumeric.random_array import uniform
     
    lower_limit = -10
    upper_limit = 10
    npts = 500
    xi = linspace(lower_limit-0.1, upper_limit+0.1, npts)
    yi = linspace(lower_limit-0.1, upper_limit+0.1, npts)

    x = []
    y = []
    z = []
    
    # Fun to test
    functionXY = function_G1_difficult_XY
    
    x = uniform(lower_limit, upper_limit, npts)
    y = uniform(lower_limit, upper_limit, npts)
    for index in range(0,len(x)):
        z.append(functionXY(x[index],y[index]))             

    zgrid = griddata(x,y,z,xi,yi)
    
    
    p.cla()
    p.contour(xi, yi, zgrid,linewidths=0.5,colors='k')
    p.contourf(xi, yi, zgrid)
    p.draw()
    p.show()