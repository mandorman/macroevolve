'''
Created on Mar 9, 2012

@author: armand
'''
from common_entities.fitness_algorithm import Fitness_algorithm
from algorithms.random_alg import Population_random


class GA_alg(Fitness_algorithm):
    '''
    Implementation of Macroevolutionary Algorithm
    '''
    def __init__(self, params):
        '''
        The parameters that the algorithm takes ... (whatever..)
        '''
        super(GA_alg, self).__init__()   
        
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