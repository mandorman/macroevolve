'''
Created on Mar 9, 2012

@author: armand
'''

'''
//////////////////////////////////////////////////////////////////////////////////
  Functions to test

    Now only put all the functions right here.
    The idea should be serialize it to JSON, and let import functions as objects.
//////////////////////////////////////////////////////////////////////////////////
'''
import math

def functionXY(x,y):
    '''
    Some nice base function.
    '''
    #return x**2+y**2
    dist = math.sqrt((x*x)+(y*y))
    return ( dist+math.sin(2*dist)  )/( 100+dist)



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
        #self.functions = []
        self.functions = []
        self.functions.append(functionXY)
        
    def get_random_function(self):
        r = 0
        return self.functions[r]
        
