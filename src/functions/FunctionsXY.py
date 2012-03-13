'''
Created on Mar 9, 2012

@author: armand
'''
import random
import math

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
        
