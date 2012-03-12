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
        print "Population GA poop {0}".format(param.get_size_population())
        super(Population_GA, self).__init__(size=param.get_size_population())
        
        self.__param = param 

    def next_generation(self):
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
        
        scaled_fitness_list=self.scaled_fitness(self.get_terrain().is_minimize)
        
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
        mut_prob = self.__param.get_probability_of_mutation()
        number_of_individuals_to_mutate=int(mut_prob*len(people_list))
        print "Mutate some individuals! proB: {0}".format(number_of_individuals_to_mutate)
        for i in range(0,number_of_individuals_to_mutate):
            r_num = random.randint(0,len(people_list)-1)
            self.mutate_individual(people_list[r_num])
            
    def mutate_individual(self, indy):
        '''
        Mutates the individual object and returns it.
        It must calculate the fitness for the new mutated individual.
        '''
        variation=random.uniform(0,0.05)
         
        indy.x+=variation
        
        lower_lim = self.get_terrain().get_lower_limit()
        upper_lim = self.get_terrain().get_upper_limit()
        
        if indy.x > lower_lim: indy.x = lower_lim + (indy.x - upper_lim)
        if indy.x < lower_lim: indy.x = upper_lim + (indy.x - lower_lim)
        indy.y += variation
        if indy.y > upper_lim : indy.y = lower_lim + indy.y-indy.upper_limit
        if indy.y < lower_lim: indy.y = indy.upper_limit + (indy.y - lower_lim)
        
        indy.set_fitness(self.calculate_fitness(indy.x, indy.y)) 
        return(indy)

    
    
    def crossover_population(self):
        '''
        Randomly choose 'X' individuals from the population (according to the corresponding argument).
        Selection allows repetition of individuals. Selection is performed according to probability
        to reproduce from each individual according to its fitness.
        '''
        number_of_pairs_to_crossover=int(self.__params.probability_of_crossover*len(self)/2)
        for i in range(0,number_of_pairs_to_crossover):
            ix_crossover1=random.randint(0,len(self)-1)
            ix_crossover2=random.randint(0,len(self)-1)
            ind_crossover1=self[ix_crossover1]
            ind_crossover2=self[ix_crossover2]
            crossovered_individuals=ind_crossover1.crossover(ind_crossover2)
            self[ix_crossover1]=crossovered_individuals[0]
            self[ix_crossover2]=crossovered_individuals[1]
    
    def scaled_fitness(self, isMinimization):
        '''
        Scales the fitness of each individual according to the population fitness
        to calculate its probability to reproduce
        '''
        
        maxfitness=max([individual.fitness for individual in self.get_individuals()])
        minfitness=min([individual.fitness for individual in self.get_individuals()])
        avgfitness=sum([individual.fitness for individual in self.get_individuals()])/len(self.get_individuals())
       
        if (abs(minfitness-maxfitness)<0.00001): #to protect zero division
            #print "i"
            scaled_fitness_values=[(individual.fitness-maxfitness)/(0.00001) for individual in self.get_individuals()]
            
        elif (isMinimization):
                scaled_fitness_values=[math.fabs((individual.fitness-maxfitness)/(minfitness-maxfitness)) for individual in self.get_individuals()]        
        else:
                scaled_fitness_values=[(maxfitness-individual.fitness)/(maxfitness-minfitness) for individual in self.get_individuals()]
        
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
    def __init__(self, population_size):
        '''
        The base parameters for genetic algorithms
        '''
        super(Params_GA, self).__init__(population_size)
        
        # Specific parameters
        self.maxgenerations=100
        self.minimization=True
        self.probability_of_mutation=0.05
        self.probability_of_crossover=0.85
        self.elitism=False
        self.convergence_coefficient=0.1    

    def get_maxgenerations(self):
        return self.__maxgenerations


    def get_minimization(self):
        return self.__minimization


    def get_probability_of_mutation(self):
        return self.__probability_of_mutation


    def get_probability_of_crossover(self):
        return self.__probability_of_crossover


    def get_elitism(self):
        return self.__elitism


    def get_convergence_coefficient(self):
        return self.__convergence_coefficient


    def set_maxgenerations(self, value):
        self.__maxgenerations = value


    def set_minimization(self, value):
        self.__minimization = value


    def set_probability_of_mutation(self, value):
        self.__probability_of_mutation = value


    def set_probability_of_crossover(self, value):
        self.__probability_of_crossover = value


    def set_elitism(self, value):
        self.__elitism = value


    def set_convergence_coefficient(self, value):
        self.__convergence_coefficient = value

    maxgenerations = property(get_maxgenerations, set_maxgenerations, None, "maxgenerations's docstring")
    minimization = property(get_minimization, set_minimization, None, "minimization's docstring")
    probability_of_mutation = property(get_probability_of_mutation, set_probability_of_mutation, None, "probability_of_mutation's docstring")
    probability_of_crossover = property(get_probability_of_crossover, set_probability_of_crossover, None, "probability_of_crossover's docstring")
    elitism = property(get_elitism, set_elitism, None, "elitism's docstring")
    convergence_coefficient = property(get_convergence_coefficient, set_convergence_coefficient, None, "convergence_coefficient's docstring")



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
        self.__params = params

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