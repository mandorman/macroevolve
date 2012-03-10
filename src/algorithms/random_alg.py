'''
Created on Mar 10, 2012

@author: armand

Dummy sample of algoritm (just to test)

'''
from common_entities.population import Population
from common_entities.fitness_algorithm import Fitness_algorithm


class Population_random(Population):
    '''
    Our specific population class of this algorithm
    '''
    def __init__(self, size_populus):
        super(Population_random, self).__init__(size=size_populus)
    
        #self.__size = size
    
    def new_population(self):
        '''
        New population (next event)
        '''
        # Just to put explicit that is called super method  
        super(Population_random, self).new_population()    
    
    def next_generation(self):
        '''
        In this case, the next generation is starting another time the population.
        Just to test.
        '''
        super(Population_random, self).new_population()

class Random_alg_params(object):
    '''
    Class to encapsulate all the params
    '''
    def __init__(self, population):
        self.__population = population

    def get_size_population(self):
        return self.__population


    def set_size_population(self, value):
        self.__population = value

    population = property(get_size_population, set_size_population, None, "population's size")
    

class Random_alg(Fitness_algorithm):
    '''
    Implementation of random algorithm
    '''
    def __init__(self, params):
        '''
        The parameters that the algorithm takes ... (whatever..)
        '''
        super(Random_alg, self).__init__()   
        
        # Specific params for this algorithm
        self.__params = params
        
        # Specific params
        self.__population = Population_random(self.__params.get_size_population())
        #self.new_population()
        
    def new_population(self):
        '''
        It creates a new population
        '''
        self.__population.new_population()    
        
    def update_population(self):
        '''
        Updates the population (next event and updates)
        '''
        self.__population.next_generation()
    
    def is_population_enough_good(self):
        '''
        Condition to stop the algorithm
        '''
        # The random algorithm never converges :P
        return False
    
    def get_individuals(self):
        '''
        Return individuals
        '''
        #print("There are {0} individuals".format(self.__population.get_size()) )
        return self.__population.get_individuals()