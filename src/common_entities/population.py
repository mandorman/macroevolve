'''
Created on Mar 9, 2012

@author: armand

Usally this kind of algorithms use the concept of population and individuals.

If it is necessary, the new algorithms implemented could use it and add to this
objects the proper methods.

'''

import random

class Individual(object):
    '''
    Representation of an individual.
    '''
    def __init__(self):
        '''
        Individual.
        '''
        self.__x = 0
        self.__y = 0
        self.__fitness = 0
                
        pass

    def get_x(self):
        return self.__x


    def get_y(self):
        return self.__y


    def get_fitness(self):
        '''
        Fitness function that gives the territorium
        '''
        return self.__fitness


    def set_x(self, value):
        self.__x = value


    def set_y(self, value):
        self.__y = value


    def set_fitness(self, value):
        self.__fitness = value

    
    x = property(get_x, set_x, None, "x's docstring")
    y = property(get_y, set_y, None, "y's docstring")
    fitness = property(get_fitness, set_fitness, None, "fitness's docstring")
    

class Terrain(object):
    
    foo = lambda x,y : x**2+y**2
    def __init__(self, upper_limit=10, lower_limit=-10, landscape_function=foo):
        '''
        It is the territorium, so it contains restrictions propers of it 
        and also a fitness function (it infere to each individual its fitness).
        
        '''
        self.__upper_limit = upper_limit
        self.__lower_limit = lower_limit
        self.__function = landscape_function

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
    

territorium = Terrain()
class Population(object):
    
    def __init__(self, indyClass=Individual, size=10, terrain=territorium):
        '''
        We could specify the number of individuals that we want.
        Of course, every type of individual could be specified
        '''
        self.__individualClass = indyClass
        self.__size = size
        self.__map = terrain
        self.__people = []

    def new_population(self):
        '''
        By default it sparse the individuals among the map (zone).
        '''
        ulimit = self.__map.get_upper_limit()
        dlimit = self.__map.get_lower_limit()
        
        # Init
        self.__people = []
        
        # Sparse individuals randomly for the terrain
        for i in range(self.__size):
            x = random.uniform(dlimit, ulimit)
            y = random.uniform(dlimit, ulimit)
            z = self.__map.get_function()
            
            individual = self.__individualClass()
            individual.set_x(x)
            individual.set_y(y)
            individual.set_fitness(z)
            
            self.__people.append(individual)

    def next_generation(self):
        '''
        Next step of the population
        
        (override)
        '''
        
        pass
    
    def get_individuals(self):
        '''
        Returns the individuals of the class
        '''    
        return self.__people

    def get_individual_class(self):
        return self.__individualClass


    def get_size(self):
        return self.__size


    def set_individual_class(self, value):
        self.__individualClass = value


    def set_size(self, value):
        self.__size = value


    individualClass = property(get_individual_class, set_individual_class, "individualClass's docstring")
    size = property(get_size, set_size, "size's docstring")
        

