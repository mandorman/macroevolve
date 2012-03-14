'''
Created on Mar 9, 2012

@author: armand
'''
from common_entities.population import Population
from common_entities.fitness_algorithm import Fitness_algorithm
import math as m
import random
from algorithms.random_alg import Population_random

class Population_mixed(Population):
    def __init__(self, param):
        super(Population_mixed, self).__init__(size=param.get_size_population())

        
class Mixed_alg(Fitness_algorithm):
    '''
    Implementation of pseudoMacroevolutionary Algorithm
    (not, the concept is the same but without the distance matrix ... )
    '''
    def __init__(self, params):
        '''
        The parameters that the algorithm takes ... (whatever..)
        '''
        super(Mixed_alg, self).__init__()   
        
        # Specific params for this algorithm
        self.__params = params
        
        # Specific params
        self.__population = Population_mixed(self.__params)
        
        # Hard coded params (then put in GUI and play!)
        self.__radius_param = 4 # -10 a 10
        self.__random_prop = 0.3 # 30 % of eliminated, search randomly


    def new_population(self):
        '''
        It creates a new population
        '''
        print "ma_alg : new_population"
        self.__population.new_population()    
    
    def update_population(self):
        '''
        Updates the population (next event and updates).
        
        This strategy is like hook (just to show explicitally the main idea)
        '''
        # Pseudo Macro Evolutionary algorithm
        #avg_fitness = sum([ ind.get_fitness() for ind in self.get_individuals() ])/self.get_size_population()
        #ind.set_fitness( self.get_population().calculate_fitness(ind.x, ind.y) )
        
        # This depends of it maximize or minimize the function!
        avg_fitness = 0
        #best_fitness = None # Not that this value should be opposite if minimize!!!
        best_ind = None
        best_fitness = None
        
        for ind in self.get_individuals():
            if self.__is_better_fitness(best_fitness, ind.get_fitness()):
                best_ind = ind
                best_fitness = ind.get_fitness()
            avg_fitness = avg_fitness + ind.get_fitness()
        
        x_best = best_ind.get_x()
        y_best = best_ind.get_y()
        
        avg_fitness = avg_fitness/self.get_size_population()
        
        new_individuals = []
        
        # And what if we pivote among the best? (instead average?)
        avg_fitness = (best_ind.get_fitness() + avg_fitness)/2
        # For all individuals that are less than the average
        for ind in self.get_individuals():
            # Minimize the fitness ...  encapsulate this!
            #if (ind.get_fitness() > avg_fitness):
            if (not self.__is_better_fitness(avg_fitness, ind.get_fitness() ) ) :
                # Calculates new position near best 
                x,y = self.__calculate_pos_in_radius(self.__radius_param, x_best, y_best)
                ind.set_x(x)
                ind.set_y(y)
                ind.set_fitness(self.get_population().calculate_fitness(x, y))
   
            else:
                '''
                We could try to improve a little for the rest of individuals (chance to improve..)
                ''' 
                # Also we could try to mutate more than one..
                indyTmp = ind
                indyTmp = (self.mutate_individual(indyTmp))
                if (  self.__is_better_fitness(indyTmp.get_fitness(), ind.get_fitness()) ):
                    ind.set_x(indyTmp.get_x())
                    ind.set_y(indyTmp.get_y())
            
            # New individuals (try to improve)         
            new_individuals.append(ind)
            self.get_population().set_individuals(new_individuals)
            
    def mutate_individual(self, indy):
        '''
        Mutates the individual object and returns it.
        It must calculate the fitness for the new mutated individual.
        '''
        variation=random.uniform(0,0.05)
         
        indy.x+=variation
        
        lower_lim = self.get_population().get_terrain().get_lower_limit()
        upper_lim = self.get_population().get_terrain().get_upper_limit()
        
        if indy.x > lower_lim: indy.x = lower_lim + (indy.x - upper_lim)
        if indy.x < lower_lim: indy.x = upper_lim + (indy.x - lower_lim)
        indy.y += variation
        if indy.y > upper_lim : indy.y = lower_lim + indy.y- upper_lim
        if indy.y < lower_lim: indy.y = upper_lim + (indy.y - lower_lim)
        
        indy.set_fitness(self.get_population().calculate_fitness(indy.x, indy.y)) 
        return(indy)



    def is_population_enough_good(self):
        '''
        Condition to stop the algorithm
        '''
        # The random algorithm never converges :P
        return False
    
    def get_population(self):
        return self.__population


    def set_population(self, value):
        self.__population = value
        

    def get_individuals(self):
        '''
        Return individuals
        '''
        #print("There are {0} individuals".format(self.__population.get_size()) )
        return self.__population.get_individuals()

    def __calculate_pos_in_radius(self, max_r, center_x, center_y):
        '''
        Calculates a position inside a certain radius ...
        
        I calculate new position as :
            a = random.uniform(0,2*pi)
            x = d*cos(a)
            y = d*sin(a)
        '''
        a = random.uniform(0, 2*m.pi)
        d = random.uniform(0,max_r) 
        x = center_x + d*m.cos(a)
        y = center_y + d*m.sin(a)
         
        # The restriction but, is that not pass the limits... so..
        lower_lim = self.__get_terrain().get_lower_limit()
        upper_lim = self.__get_terrain().get_upper_limit()
        x = self.__into_range(x, lower_lim, upper_lim)
        y = self.__into_range(y, lower_lim, upper_lim)
        
        return (x, y )


    def __into_range(self, c, lower_limit, upper_limit):
        '''
        Just avoid get out of the map...
        '''
        if (c  < lower_limit):
            c = lower_limit
        elif (c > upper_limit):
            c = upper_limit
        return c
    
    
    def __get_terrain(self):
        return self.get_population().get_terrain()
    
    def __is_better_fitness(self, fit_ref, fit_new):
        return self.__get_terrain().is_better_fitness(fit_ref, fit_new)
    
    population = property(get_population, set_population, None, "population's docstring")
    
    