"""Basic architecture for a simple Genetic Algorithm example."""
import random
import numpy
import time
#from multiprocessing.dummy import Pool as ThreadPool


# 1 - Heredity
# 2 - Variation
# 3 - Selection

# Setup: Make a random a pop of N elements,
    # Calculate fitness.
    # Reproduction/Selection -> Returns a new N-element pop
        # Pick M (1 or 2 or ... or M) parents
            # We can pick based on probability to make use of fitting residue mutations
# Make a new element
    # Crossover
    # Mutation
# Crossover: Take half of the genetic information of each parent (2 parents)
# Mutation: X% of generating a random attribute for an element

#Step 1: Initialize. Create a pop of N elem with random DNA.
#Step 2: Selection. Evaluate the fitness for each elem. and build a mating pool.
#Step 3: Reproduction. Repeat N times:
    #1: Pick 2 parents with prob. according to relative fitness.
    #2: Crossover: create a child by combining its parent's DNA.
    #3: Mutation: Mutate the child's DNA based on a given prob. Add new child to the pop.
#Step 4: Replace the old pop with new pop. Go back to Step 2.

# Notes:
#   Having a large pop. takes too many resources.
#   Too much mutation takes the problem to brute force approach.
#   0 mutation relays on the implicit variation of the initial pop.


class GeneticElement(object):
    """Represents an individual with its own dna and associated score."""

    def __init__(self, dna, score):
        self._dna = dna
        self._score = score
    
    @property
    def dna(self): return self._dna
    @dna.setter
    def dna(self, dna): self._dna = dna
    @property
    def score(self): return self._score
    @score.setter
    def score(self, score): self._score = score

class Population(object):
    """Represents a population with parameters: target, mutation rate, population."""

    _scoring = ()
    _scoring_sum = 0
    _max_score = -1
    _max_score_id = -1    

    def __init__(self, target, population_size, mutation_rate):
        self._target = target
        self._mutation_rate = mutation_rate
        self._population_size = population_size
        self._length = len(target)
        self._target_score = 2 ** self._length
        self._population = self.initpopulation(target, population_size)
        
    @property
    def scoring(self): return self._scoring
    @scoring.setter
    def scoring(self, scoring): self._scoring = scoring
    @property
    def scoring_sum(self): return self._scoring_sum
    @scoring_sum.setter
    def scoring_sum(self, scoring_sum): self._scoring_sum = scoring_sum
    @property
    def max_score(self): return self._max_score
    @max_score.setter
    def max_score(self, max_score): self._max_score = max_score
    @property
    def max_score_id(self): return self._max_score_id
    @max_score_id.setter
    def max_score_id(self, max_score_id): self._max_score_id = max_score_id

    ##GENETIC RULES##

    #Initialization
    def initpopulation(self, target, population_size):
        """Initializes population with random elements"""

        population_tuple = ()

        for i in range(population_size):
            dna = ''
            score = 0

            for c in target:
                #Generates a random new character from space (ASCII 32) to tilde (ASCII 126)
                character = chr(random.randint(32, 126))
                dna += character
                if c == character:
                    score += 1

            score = 2 ** score
            if score > self.max_score:
                self.max_score = score
                self.max_score_id = i
            self.scoring += (score, )
            self.scoring_sum += score
            population_tuple += (GeneticElement(dna, score), )

        return population_tuple
    
    #Selection, Heredity and Variation
    def crossmutation(self, target, parent_a, parent_b, mutation_rate, position):
        """Performs parental gene crosover, mutation and scoring returning a new element."""

        dna = ''
        score = 0

        divisor = parent_a.score + parent_b.score
        if divisor == 0:
            ratio = 0
        else:
            ratio = parent_a.score / divisor

        if ratio == 0:
            for i in range(self._length):
                character = chr(random.randint(32, 126))
                dna += character
                if character == target[i]:
                    score += 1
        else:
            for i in range(self._length):
                #Mutation rate is the chance of a gene to be changed (ranges from 0 to 1)
                if random.random() < mutation_rate:
                    character = chr(random.randint(32, 126))
                else:
                    #The fittest is more likely to pass its genes
                    if random.random() < ratio:
                        character = parent_a.dna[i]
                    else:
                        character = parent_b.dna[i]
                dna += character
                if character == target[i]:
                    score += 1

        score = 2 ** score
        if score > self.max_score:
            self.max_score = score
            self.max_score_id = position
        self.scoring += (score, )
        self.scoring_sum += score

        return GeneticElement(dna, score)

    ##GENETIC ENGINE##

    #New generation engine
    def next_generation(self):
        '''Returns a new tuple of children looping through the population tuple'''

        new_generation = ()

        if self.scoring_sum > self.max_score:
            #This is the regular case where there's 2 or more eligible parents
            self.max_score = -1
            self.max_score_id = -1

            #Scores have to be normalized to be used as a distribution function
            scores = ()
            for score in self.scoring:
                scores += (score / self.scoring_sum, )
            #Resets the scores
            self.scoring = ()
            self.scoring_sum = 0

            for i in range(self._population_size):
                parents = numpy.random.choice(self._population, 2, False, scores)
                new_generation += (self.crossmutation(self._target, parents[0], parents[1], self._mutation_rate, i), )

        else:
            #Resets the scores
            self.max_score = -1
            self.scoring = ()

            if self.scoring_sum == 0:
                #scores_sum == 0 is the starting case with no preferred parent
                self.max_score_id = -1

                for i in range(self._population_size):
                    parents = numpy.random.choice(self._population, 2, False)
                    new_generation += (self.crossmutation(self._target, parents[0], parents[1], self._mutation_rate, i), )

            else:
                #scores_sum == max_score is the (rare) case when there's just 1 parent (an alpha) with score > 0
                parent_alpha = self._population[self.max_score_id]
                #Resets the scores
                self.max_score_id = -1
                self.scoring_sum = 0

                reduced_range = self._population_size - 1

                for i in range(reduced_range):
                    #To skip the alpha parent we choose from all but 1 parent
                    #This way the alpha parent can't mate itself
                    parent_id = numpy.random.randint(length)
                    if parent_id >= self.max_score_id:
                        parent_id += 1
                    new_generation += (self.crossmutation(self._target, parent_alpha, self._population[parent_id], self._mutation_rate, i), )

        return new_generation

    ##THE MAIN SCRIPT##
    def run(self):
        """Runs the simulation"""

        count = 1
        print('')
        print('\t{}\t{}\t\t {}'.format('Generation', 'Best', 'Score'))
        print('\t---------------------------------------------------')
        print('\t{}\t\t{}\t\t {}/{}'.format(count, self._population[self.max_score_id].dna, self.max_score, self.scoring_sum))
        while self.max_score < self._target_score:
            count += 1
            self._population = self.next_generation()
            print('\t{}\t\t{}\t\t {}/{}'.format(count, self._population[self.max_score_id].dna, self.max_score, self.scoring_sum))
        print('')
        print('\tFound \'' + self._target + '\' after ' + str(count) + ' generations.')
        print(
            '\tMutation Rate: ' + str(self._mutation_rate) + '% chance.\n' +
            '\tPopulation: ' + str(self._population_size) + ' elements.'
            )
        return count

    def run_silent(self, max_generation = None):
        """Runs the simulation with no messages and the opportunity of early interruption"""

        count = 1        
        while self.max_score < self._target_score:
            count += 1
            self._population = self.next_generation()
            if max_generation:
                if max_generation <= count:
                    break
        return count

class PopulationMap(object):
    """Runs all simulations within given ranges of population and mutation rates"""

    #Constructor
    def __init__(self, target,
                 minpopulation, maxpopulation, population_step,
                 minmutationrate, maxmutationrate, mutation_rate_step):
        self._target = target
        self._min_population = minpopulation
        self._max_population = maxpopulation
        self._population_step = population_step
        self._min_mutationrate = minmutationrate
        self._max_mutationrate = maxmutationrate
        self._mutation_rate_step = mutation_rate_step

    #TODO: Matrix operations and exception handling

    #Matrix simulator
    def simulator(self, iterations, max_generation = None):
        """Fills the matrix with the values of the simulation map"""

        fileobj = None
        try:
            fileobj = open('data.csv', 'w')
            #Top row: all studied mutation rates
            fileobj.write('{};'.format(''))
            tmp_mmr = int(self._min_mutationrate * 100)
            tmp_mrs = int(self._mutation_rate_step * 100)
            tmp_Mmr = int(self._max_mutationrate * 100) + tmp_mrs
            for current_mutation_rate in range(tmp_mmr, tmp_Mmr, tmp_mrs):
                fileobj.write('{}%;'.format(current_mutation_rate))
            fileobj.write('\n')

            tmp_mp = self._max_population + self._population_step
            for current_population in range(self._min_population, tmp_mp, self._population_step):
                #Left column: each studied population
                fileobj.write('{};'.format(current_population))

                for current_mutation_rate in range(tmp_mmr, tmp_Mmr, tmp_mrs):
                    cumulative_generations = 0
                    #CORREGIR LA CHAPUZA#
                    chapuza = current_mutation_rate / 100
                    #Sum the values of the final generation value for every simulation
                    for current_iteration in range(iterations):
                        cumulative_generations += Population(self._target, current_population, chapuza).run_silent(max_generation)
                    #Middle rows: all average generations
                    average = cumulative_generations / iterations
                    fileobj.write('{};'.format(average))

                fileobj.write('\n')
        except Exception as e:
            print(e)
        finally:
            if fileobj is not None:
                fileobj.close()

    #Runs the script
    def run(self, iterations, max_generation):
        """Runs the matrix simulator"""

        start_time = time.time()
        self.simulator(iterations, max_generation)
        print('')
        print('\t---------------------------------------------------')
        print('\tMapped {} from {} to {} elements with'.format(self._target, self._min_population, self._max_population))
        print('\t{}% to {}% mutation chance on {} iterations.'.format(self._min_mutationrate, self._max_mutationrate, iterations))
        print('\tIt took {} seconds.'.format(time.time() - start_time))
        print('\t---------------------------------------------------')
        print('')



#Launch the program
#Population('to be or not to be', 100, 0.1).run()
#   target,
#   minpopulation, maxpopulation, population_step, 
#   minmutationrate, maxmutationrate, mutation_rate_step
#PopulationMap('abcdefghij', 200, 30, 100, 1, 10).run(5, 200)
#PopulationMap('unicorn', 30, 100, 5, 0.01, 0.1, 0.01).run(5, None)
PopulationMap('unicorn', 30, 100, 5, 0.01, 0.10, 0.01).run(4, 200)

#TODO:
    #<THREADING>
    #for...
    #   population_map += (Population(target, current_mutation_rate, current_population).run(), )
    #
    #pool = ThreadPool(4) sets the pool size to 4
    #pool = ThreadPool() defaults for the number of cores in the machine
    #pool = ThreadPool()
    #Each Thread performs an interation
    #results = pool.map(run, population_map)
    #sumgen = sum
    #pool.close()
    #pool.join()(results)
    #</THREADING>