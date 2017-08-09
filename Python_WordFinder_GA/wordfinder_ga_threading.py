"""Basic architecture for a simple Genetic Algorithm example."""
import random
import numpy
import time
from multiprocessing.dummy import Pool as ThreadPool


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
    
    def __init__(self, dna = None):
        if dna != None:
            self._dna = dna
    
    @property
    def dna(self):
        return self._dna

    @dna.setter
    def dna(self, dna):
        self._dna = dna

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    #Operator overloading for list/tuple management
    def __lt__(self, other):
        return self._score < other._score

    def ___le__(self, other):
        return self._score <= other._score

    def __eq__(self, other):
        return self._score == other._score

    def __ne__(self, other):
        return self._score != other._score

    def __gt__(self, other):
        return self._score > other._score

    def __ge__(self, other):
        return self._score >= other._score


class Population(object):
    """Represents a population with parameters: target, mutation rate, population."""

    def __init__(self, target, mutationrate, population_size):
        self._target = target
        self._mutationrate = mutationrate
        self._population = population
        self._targetscore = 2**len(target)
        self._population = initpopulation(target, population_size)

    ##GENETIC RULES##

    #Initialization
    @staticmethod
    def initpopulation(target, population_size):
        """Initializes population with a random set of individuals"""
        population_tuple = ()
        for i in range(population_size):
            newchild = GeneticElement()
            newchild.dna = ''.join(newchar() for c in target)
            newchild.score = fitnessfunction(target, newchild.dna)
            population_tuple += newchild
        return population_tuple

    #Selection
    @staticmethod
    def fitnessfunction(target, dna):
        """Evaluates a given individual's score"""
        return 2**sum(1 for i in range(len(target)) if target[i] == dna[i])

    #Heredity
    @staticmethod
    def crossover(parent_a, parent_b):
        """Performs parental gene crosover."""
        #The fittest is more likely to pass its genes
        return ''.join(character if (random.random() < parent_a.score / (parent_a.score + parent_b.score)) else parent_b.dna[i] for i, character in enumerate(parent_a.dna))

    #Variation
    @staticmethod
    def newchar():
        """Generates a random new character from space (ASCII 32) to tilde (ASCII 126)."""
        return chr(random.randint(32, 126))

    @staticmethod
    def mutation(dna, mutationrate):
        """Performs mutation on a given Dna with current mutation rate."""
        #Mutation rate is the chance of a gene to be changed (ranges from 0 to 1)
        return ''.join(newchar() if (random.random() < mutationrate) else character for character in dna)

    @staticmethod
    def crossmutation(target, parent_a, parent_b, mutationrate):
        """Crossover + Mutation. Returns a brand new individual."""
        newchild = GeneticElement()
        newchild.dna = mutation(crossover(parent_a, parent_b), mutationrate)
        newchild.score = fitnessfunction(target, newchild.dna)
        return newchild

    ##GENETIC ENGINE##
    #These methods manage the population list
            
    @staticmethod
    def next_generation(target, length, mutationrate, population, population_size):
        """Returns next generation elements as list."""
        scores = tuple(element.score for element in population)
        population_score = sum(score for score in scores)
        next_generation = ()
        
        #population_score = 0 implies there's no preferred parent
        if population_score == 0:
            for i in range(population_size):
                #Randomly picks 2 parents
                parentcouple = random.sample(population, 2)
                #Adds a new child
                next_generation_list.append(crossmutation(target, parentcouple[0], parentcouple[1], mutationrate))
        else:
            maxscoreid = population.index(max(population))
            parent_alpha = population[maxscoreid]
            #If population_score equals current max score it implies there's just 1 preferred parent since population_score > 0
            if population_score == parent_alpha.score:
                for i in range(population_size):
                    parent_id_b = random.choices(population, scores, 1)
                    #Forces both parents to be different
                    while parent_id_b == maxscoreid:
                        parent_id_b = random.choices(population, scores, 1)
                    #Adds a new child
                    next_generation += crossmutation(target, parent_alpha, population[parent_id_b], mutationrate)
            #population_score != myMaxScore is the regular case where there's 2 or more eligible parents
            else:
                for i in range(population):
                    parent_a = random.choices(population, scores, 1)
                    parent_b = random.choices(population, scores, 1)
                    #Forces all parents to be different
                    while parent_a.id == parent_b.id:
                        parent_b = random.choices(population, scores, 1)
                    #Adds a new child                    
                    next_generation += crossmutation(target, parent_a, parent_b, mutationrate)
        return next_generation

    ##THE MAIN SCRIPT##
    def run(self):
        """Runs the simulation"""
        currentbestscore = 0
        count = 0
        print('')
        print('\t{}\t{}\t\t {}'.format('Generation', 'Best', 'Score'))
        print('\t---------------------------------------------------')
        length = len(self.target)
        maxscore = self.targetscore
        while currentbestscore < self.targetscore:
            count += 1
            bestdna = ''
            generationbestscore = 0
            for element in self.populationlist:
                if element.score > generationbestscore:
                    generationbestscore = element.score
                    bestdna = element.dna
                    if generationbestscore > currentbestscore:
                        currentbestscore = generationbestscore
            print('\t{}\t\t{}\t\t {}/{}'.format(count, bestdna, generationbestscore, maxscore))
            if currentbestscore < self.targetscore:
                self.populationlist = self.newgeneration(
                    self.target, length, self.mutationrate, self.population, self.populationlist
                    )
        print('')
        print('\tFound \'' + self.target + '\' after ' + str(count) + ' generations.')
        print(
            '\tMutation Rate: ' + str(self.mutationrate) + '% chance.\n' +
            '\tPopulation: ' + str(self.population) + ' individuals.'
            )
    @staticmethod
    def runcount(stopcount, populationobject):
        """Runs the simulation up to a given number of generations"""
        currentmaxscore = 0
        count = 0
        length = len(populationobject.target)
        while count < stopcount and currentmaxscore < populationobject.targetscore:
            count += 1
            generationbestscore = 0
            for element in populationobject.populationlist:
                if element.score > generationbestscore:
                    generationbestscore = element.score
                    if generationbestscore > currentmaxscore:
                        currentmaxscore = generationbestscore
            if currentmaxscore < populationobject.targetscore:
                populationobject.populationlist = populationobject.newgeneration(
                    populationobject.target, length, populationobject.mutationrate,
                    populationobject.population, populationobject.populationlist
                    )
        return count
    @staticmethod
    #With given maxgen
    def runcount_test(populationobject):
        """Runs the simulation up to a given number of generations"""
        currentmaxscore = 0
        count = 0
        stopcount = 200
        length = len(populationobject.target)
        while count < stopcount and currentmaxscore < populationobject.targetscore:
            count += 1
            generationbestscore = 0
            for element in populationobject.populationlist:
                if element.score > generationbestscore:
                    generationbestscore = element.score
                    if generationbestscore > currentmaxscore:
                        currentmaxscore = generationbestscore
            if currentmaxscore < populationobject.targetscore:
                populationobject.populationlist = populationobject.newgeneration(
                    populationobject.target, length, populationobject.mutationrate,
                    populationobject.population, populationobject.populationlist
                    )
        return count

class PopulationMap(object):
    """Runs all simulations within given ranges of population and mutation rates"""
    target = ''
    maxgen = 0
    minpopulation = 0
    maxpopulation = 0
    minmutationrate = 0
    maxmutationrate = 0

    #Constructor
    def __init__(self, target, maxgen,
                 minpopulation, maxpopulation, minmutationrate, maxmutationrate):
        self.target = target
        self.maxgen = maxgen
        self.minpopulation = minpopulation
        self.maxpopulation = maxpopulation
        self.minmutationrate = minmutationrate
        self.maxmutationrate = maxmutationrate

    #TODO: Matrix operations and exception handling

    #Matrix simulator
    def fillmap(self,
                target, maxgen, minpopulation, maxpopulation,
                minmutationrate, maxmutationrate, iterations):
        """Fills the matrix with the values of the simulation map"""

        fileobj = open('data.csv', 'w')        
        start_time = time.time()

        currentpopulation = minpopulation
        while currentpopulation <= maxpopulation:
            fileobj.write('{};'.format(currentpopulation))

            mutationrate = minmutationrate
            while mutationrate <= maxmutationrate:
                currentiteration = 0
                #sumgen = 0
                mypopulationlist = list()
                while currentiteration < iterations:
                    mypopulationlist.append(Population(target, mutationrate, currentpopulation))
                    currentiteration += 1
                #<THREADING>
                #pool = ThreadPool(4) sets the pool size to 4
                #pool = ThreadPool() defaults for the number of cores in the machine
                pool = ThreadPool()
                #Each Thread performs an interation
                results = pool.map(Population.runcount_test, mypopulationlist)
                sumgen = sum
                pool.close()
                pool.join()(results)
                #</THREADING>

                genaverage = sumgen / iterations
                fileobj.write('{};'.format(genaverage))
                mutationrate += 1


            fileobj.write('\n')
            print('After {} seconds'.format(start_time - time.time()))
            currentpopulation += 5

        fileobj.close()

    #Runs the script
    def run(self, iterations):
        """Runs the matrix simulator"""
        start_time = time.time()
        self.fillmap(
            self.target, self.maxgen, self.minpopulation, self.maxpopulation,
            self.minmutationrate, self.maxmutationrate, iterations
            )
        print(
            "Mapped {} from {} to {} individuals with {}% to {}% mutation chance on {} iterations".
            format(self.target, self.minpopulation, self.maxpopulation,
                   self.minmutationrate, self.maxmutationrate, iterations
                  )
            )
        print('After {} seconds'.format(start_time - time.time()))


#Launch the program
#Population('to be or not to be', 10, 100).run()
#target, maxgen, minpopulation, maxpopulation, minmutationrate, maxmutationrate
#popmap = PopulationMap('abcdefghij', 200, 30, 100, 1, 10)
#popmap.run(5)
popmap = PopulationMap('abcdefghij', 50, 50, 60, 5, 10)
popmap.run(2)