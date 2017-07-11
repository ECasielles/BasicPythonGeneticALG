"""Basic architecture for a simple Genetic Algorithm example."""
import random

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
    dna = ''
    score = 0

class Population(object):
    """Represents a population with parameters: target, mutation rate, population."""
    target = ''
    mutationrate = 0
    population = 0
    targetscore = 0
    totalScore = 0
    populationlist = list()

    #Constructor
    def __init__(self, target, mutationrate, population):
        self.target = target
        self.mutationrate = mutationrate
        self.population = population
        self.targetscore = 2**len(target)
        self.populationlist = Population.initpopulation(target, len(target), population)

    ##GENETIC RULES##

    #Initialization
    @staticmethod
    def initpopulation(target, length, population):
        """Initializes population with a random set of individuals"""
        currentpopulation = 0
        newpopulationlist = list()
        while currentpopulation < population:
            newdna = ''
            count = 0
            while count < length:
                newdna = newdna + Population.newchar()
                count += 1
            newchild = GeneticElement()
            newchild.dna = newdna
            newchild.score = Population.fitnessfunction(target, length, newdna)
            newpopulationlist.append(newchild)
            currentpopulation += 1
        return newpopulationlist

    #Selection
    @staticmethod
    def fitnessfunction(target, length, dna):
        """Evaluates a given individual's score"""
        score = 0
        position = 0
        while position < length:
            if target[position] == dna[position]:
                score += 1
            position += 1
        return 2**score

    #Heredity
    @staticmethod
    def crossover(length, parent_a, parent_b):
        """Performs parental gene crosover"""
        newdna = ''
        score_a = parent_a.score
        score_b = parent_b.score
        totalscore = score_a + score_b
        count = 0
        while count < length:
            #The fittest is more likely to pass its genes
            if random.randint(0, totalscore) < score_a:
                newdna = newdna + parent_a.dna[count]
            else:
                newdna = newdna + parent_b.dna[count]
            count += 1
        return newdna

    #Variation
    @staticmethod
    def newchar():
        """Generates a random new character"""
        char = random.randint(63, 122)
        if char == 63:
            char = 32
        if char == 64:
            char = 46
        return chr(char)

    @staticmethod
    def mutation(dna, mutationrate):
        """Performs mutation on a given Dna with current mutation rate"""
        newdna = ''
        for character in dna:
            if random.randint(0, 99) < mutationrate:
                newdna = newdna + Population.newchar()
            else:
                newdna = newdna + character
        return newdna

    @staticmethod
    def crossmutation(target, length, parent_a, parent_b, mutationrate):
        """Crossover + Mutation. Returns a brand new individual"""
        newchild = GeneticElement()
        dna = Population.crossover(length, parent_a, parent_b)
        newchild.dna = Population.mutation(dna, mutationrate)
        newchild.score = Population.fitnessfunction(target, length, newchild.dna)
        return newchild

    ##GENETIC ENGINE##

    #These methods manage the population list
    def gettotalscore(self):
        """Sums the score of all the population to do the probability calculations"""
        newscore = 0
        for element in self.populationlist:
            newscore += element.score
        return newscore
    def pickrandomparent(self, lastscore):
        """Returns a random parent Id with probability pi / (p1 + p2 + ... + pn)
        with p being its score. It is executed when there's 2 or more eligible parents."""
        comparablescore = random.randint(0, lastscore)
        currentscore = 0
        count = 0
        while currentscore < comparablescore:
            currentscore += self.populationlist[count].score
            if currentscore < comparablescore:
                count += 1
        return count
    def newgeneration(self, target, length, mutationrate, population, populationlist):
        """Creates one generation."""
        lastscore = self.gettotalscore()
        newgenerationlist = list()
        #lastscore = 0 implies there's no preferred parent
        if lastscore == 0:
            count = 0
            while count < population:
                #Randomly picks 2 parents
                parentcouple = random.sample(populationlist, 2)
                parent_a = parentcouple[0]
                parent_b = parentcouple[1]
                #Creates new child
                newchild = Population.crossmutation(
                    target, length, parent_a, parent_b, mutationrate
                    )
                newgenerationlist.append(newchild)
                count += 1
        else:
            currentmaxscore = 0
            maxscoreid = -1
            for i, element in enumerate(populationlist):
                if element.score > currentmaxscore:
                    currentmaxscore = element.score
                    maxscoreid = i
            #lastscore = currentmaxscore implies there's just 1 preferred parent since lastscore > 0
            if lastscore == currentmaxscore:
                count = 0
                while count < population:
                    parent_id_b = random.randint(1, population) - 1
                    #Forces both parents to be different
                    while parent_id_b == maxscoreid:
                        parent_id_b = random.randint(1, population) - 1
                    parent_a = populationlist[maxscoreid]
                    parent_b = populationlist[parent_id_b]
                    #Creates child
                    newchild = Population.crossmutation(
                        target, length, parent_a, parent_b, mutationrate
                        )
                    newgenerationlist.append(newchild)
                    count += 1
            #lastscore != myMaxScore is the regular case where there's 2 or more eligible parents
            else:
                count = 0
                while count < self.population:
                    parent_id_a = self.pickrandomparent(lastscore)
                    parent_id_b = self.pickrandomparent(lastscore)
                    #Forces all parents to be different
                    while parent_id_a == parent_id_b:
                        parent_id_b = self.pickrandomparent(lastscore)
                    #Creates parents
                    parent_a = populationlist[parent_id_a]
                    parent_b = populationlist[parent_id_b]
                    #Creates child
                    newchild = Population.crossmutation(
                        target, length, parent_a, parent_b, mutationrate
                        )
                    newgenerationlist.append(newchild)
                    count += 1
        return newgenerationlist

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
    def runcount(self, stopcount):
        """Runs the simulation up to a given number of generations"""
        currentmaxscore = 0
        count = 0
        length = len(self.target)
        #maxscore = self.targetscore
        while count < stopcount and currentmaxscore < self.targetscore:
            count += 1
            #bestdna = ''
            generationbestscore = 0
            for element in self.populationlist:
                if element.score > generationbestscore:
                    generationbestscore = element.score
                    #bestdna = element.dna
                    if generationbestscore > currentmaxscore:
                        currentmaxscore = generationbestscore
            if currentmaxscore < self.targetscore:
                self.populationlist = self.newgeneration(
                    self.target, length, self.mutationrate, self.population, self.populationlist
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

        currentpopulation = minpopulation
        while currentpopulation <= maxpopulation:
            fileobj.write('{};'.format(currentpopulation))

            mutationrate = minmutationrate
            while mutationrate <= maxmutationrate:

                currentiteration = 0
                sumgen = 0
                while currentiteration < iterations:
                    mypopulation = Population(target, mutationrate, currentpopulation)
                    sumgen += mypopulation.runcount(maxgen)
                    currentiteration += 1

                genaverage = sumgen / iterations
                fileobj.write('{};'.format(genaverage))
                mutationrate += 1

            fileobj.write('\n')
            currentpopulation += 5

        fileobj.close()

    #Runs the script
    def run(self, iterations):
        """Runs the matrix simulator"""
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


#Launch the program
#Population('to be or not to be', 10, 100).run()
#Population('unicorn', 5, 100).run()
#PopulationMap('abcdefghij', 200, 30, 100, 1, 10).run(5)
PopulationMap('abcdefghij', 200, 30, 100, 1, 10).run(5)
