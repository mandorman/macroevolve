'''
Created on Mar 9, 2012

@author: armand
'''
import math
import random
from common_entities.fitness_algorithm import Fitness_algorithm,\
    Common_alg_params
from algorithms.random_alg import Population_random
from common_entities.population import Population, Individual


class Individual_GA(Individual):

    def __init__(self, f_fitness):
        '''
        Genetic Algorithm individual
        '''
        self.f_fitness = f_fitness
                   
    def calculate_fitness(self,x,y):
        '''
        Function that calculates the fitness and stores it it 'fitness' attribute.
        It returns the fitness value.
        '''
        return self.f_fitness(x,y)

    """
    def crossover(self,individual):
        ''' 
        Function that do the crossover of 2 (self and sp) individuals and returns a single one.
        To have the 2 possible crossovers must be called i1.crossover(i2) and i2.crossover(i1).
        It must calculate the fitness for the new crossover.
        '''
        #offspring1=FunctionXYC()
        fit_value = self.calculate_fitness(self.x, individual.y)     
        offspring2.x=individual.x
        offspring2.y=self.y
        offspring2.calculate_fitness()
        return ([offspring1,offspring2])
    """

    def __lt__(self,individual):
        '''
        Defines the lt comparison (to be used by standard library) by:
            i1.__lt__(i2) == 
        '''
        return self.get_fitness()<individual.get_fitness()

class Population_GA(Population):
    
    def __init__(self, param):
        '''
        Population genetic algorithm requires new attributes
        '''
        super(Population_GA, self).__init__(size=param)


    def new_population(self):
        '''
        It creates a new population
        '''
        print "ma_alg : new_population"
        self.__population.new_population() 
        
    def update_population(self):
        """
        Creates new population
        """
        
        # Functions that population must do 
        self.get_new_generation() # Do new resampling with best probabilities
        self.mutate_population() # Mutate some individuals

        #self.crossover_population()
        
        """
        if self.elitism==True:
            self.population.extend(elite)
            self.generation+=1
        """

    def get_new_generation(self):
        '''
        Gets new generation
        '''
        samplesize = self.get_size()
        scaled_fitness_list=self.scaled_fitness()
        
        if (sum(scaled_fitness_list))<0.00001: #to protect zero division
            probability_to_reproduce=[fit/(0.00001) for fit in scaled_fitness_list]
        else:
            probability_to_reproduce=[fit/sum(scaled_fitness_list) for fit in scaled_fitness_list]

        acum_sum=[sum(probability_to_reproduce[0:i+1]) for i in range(0,len(probability_to_reproduce))]
        sample=[]

        individuals_list = self.get_individuals()
        for i in range(0,samplesize):
            random_number= random.uniform(0,1)
            for j in range(0,len(acum_sum)):
                if acum_sum[j]> random_number:
                    break
            sample.append(individuals_list[j])
            
        self.set_individuals(sample)

    def mutate_population(self):
        '''
        Randomly chooses the individuals to be mutated according to the corresponding
        argument
        '''
        people_list = self.get_individuals()
        number_of_individuals_to_mutate=int(self.probability_of_mutation*len(people_list))
        for i in range(0,number_of_individuals_to_mutate):
            r_num = random.randint(0,len(self)-1)
            print "Mutate ind before : {0}".format(people_list[r_num])
            self.mutate_individual(people_list[r_num])
            
    def mutate_individual(self, indy):
        '''
        Mutates the individual object and returns it.
        It must calculate the fitness for the new mutated individual.
        '''
        variation=random.uniform(0,0.05)
         
        indy.x+=variation
        if indy.x > indy.upper_limit: indy.x = indy.lower_limit + (indy.x-indy.upper_limit)
        if indy.x < indy.lower_limit: indy.x = indy.upper_limit + (indy.x -indy.lower_limit)
        indy.y += variation
        if indy.y > indy.upper_limit: indy.y = indy.lower_limit + indy.y-indy.upper_limit
        if indy.y < indy.lower_limit: indy.y = indy.upper_limit + (indy.y -indy.lower_limit)
        
        indy.set_fitness(self.calculate_fitness(indy.x, indy.y)) 
        return(indy)

    
    def scaled_fitness(self):
        '''
        Scales the fitness of each individual according to the population fitness
        to calculate its probability to reproduce
        '''
        
        maxfitness=max([individual.fitness for individual in self.get_individuals()])
        minfitness=min([individual.fitness for individual in self.get_individuals()])
        avgfitness=sum([individual.fitness for individual in self.get_individuals()])/len(self.get_individuals())
       
        if (abs(minfitness-maxfitness)<0.00001): #to protect zero division
            #print "i"
            scaled_fitness_values=[(individual.fitness-maxfitness)/(0.00001) for individual in self]
        elif (self.minimization):
                scaled_fitness_values=[math.fabs((individual.fitness-maxfitness)/(minfitness-maxfitness)) for individual in self]        
        else:
                scaled_fitness_values=[(maxfitness-individual.fitness)/(maxfitness-minfitness) for individual in self]
        
        return scaled_fitness_values
           
           
       


    def max_fitness(self):
        '''
        Return the maximum fitness value.
        '''
        return max([ind.fitness for ind in self.get_individuals()])
    
    def min_fitness(self):
        '''
        Return the minimum fitness value.
        '''
        return min([ind.fitness for ind in self.get_individuals()])
    
    def average_fitness(self):
        '''
        Computes the average fitness of the population.
        It computes the aritmetic mean of the fitness of the individuals in the population
        It may be overriden by descendants.
        '''
        return sum([individual.fitness for individual in self.get_individuals()])/(self.get_size())
    
    def fitness_dispersion(self):
        '''
        calculate the dispersion of the fitness from all the generation individuals
        it is used for stopping the genetic algortihm due to convergence criteria
        '''
    
    def sort(self,reverse=True):
        '''
        Sorts the population by descending fitness.
        It may be overriden by descendants.
        '''
        list.sort(self,reverse)
        

class Params_GA(Common_alg_params):
    def __init__(self):
        '''
        The base parameters for genetic algorithms
        '''
        # Specific parameters
        self.maxgenerations=100
        self.minimization=True
        self.probability_of_mutation=0.05
        self.probability_of_crossover=0.85
        self.elitism=False
        self.convergence_coefficient=0.1    

class GA_alg(Fitness_algorithm):
    '''
    Implementation of Genetic Algorithm
    '''
    def __init__(self, params):
        '''
        The parameters that the algorithm takes ... (whatever..)
        '''
        super(GA_alg, self).__init__()   
        
        # Specific params for this algorithm
        self.__params = Params_GA(params)

        self.__population = Population_GA(self.__params)
 
                
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