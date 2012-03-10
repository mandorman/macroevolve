'''
Created on Mar 10, 2012

@author: armand
'''

'''
Is the interface between the GUI and the population. Itself contains the parameters
of the specific algorithm.
'''

class Fitness_algorithm(object):
    
    def __init__(self):
        pass
    
    def new_population(self):
        '''
        It creates a new population
        '''
        
        pass
        
    def update_population(self):
        '''
        Updates the population (next generation of events)
        '''
        
        pass
    
    def get_individuals(self):
        '''
        Return the individuals
        '''
        pass
    
    def get_size_population(self):
        '''
        Returns the size of population
        '''
        return len(self.get_individuals())
    
    def is_population_enough_good(self):
        '''
        Condition to stop the algorithm
        '''
        # The random algorithm never converges :P
        return False