'''
Created on Mar 11, 2012

@author: armand
'''


class Terrain(object):
    
    foo = lambda x,y : x**2+y**2
    def __init__(self, upper_limit=10, lower_limit=-10, landscape_function=foo, minimize=True):
        '''
        It is the territorium, so it contains restrictions propers of it 
        and also a fitness function (it infere to each individual its fitness).
        
        '''
        self.__upper_limit = upper_limit
        self.__lower_limit = lower_limit
        self.__function = landscape_function
        self.__minimize = minimize

    def get_minimize(self):
        return self.__minimize


    def set_minimize(self, value):
        self.__minimize = value


    def calculate_fitness(self, x, y):
        return self.__function(x,y)

    def get_function(self):
        return self.__function

    def set_function(self, value):
        self.__function = value

    def get_upper_limit(self):
        return self.__upper_limit


    def get_lower_limit(self):
        return self.__lower_limit


    def set_upper_limit(self, value):
        self.__upper_limit = value


    def set_lower_limit(self, value):
        self.__lower_limit = value
            

    upper_limit = property(get_upper_limit, set_upper_limit, None, "upper_limit's of map")
    lower_limit = property(get_lower_limit, set_lower_limit, None, "lower_limit's of map")
    function = property(get_function, set_function, None, "function to minimize")
    
    def is_better_fitness(self, fit_ref, fit_new):
        '''
        Depending if we are maximizing(minimize)
        -move to population- 
        '''
        # If there is no ref, yes at all
        if fit_ref == None:
            return True
        
        # Otherwise depends if we are maximizing or minizing
        res = False
        
        if self.__minimize:
            if (fit_ref > fit_new ):
                return True
        else:
            if (fit_ref < fit_new ):
                return True
            
        return res
    is_minimize = property(get_minimize, set_minimize, None, "minimize's docstring")

    