"""Module docstring"""
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

    dna = ''
    score = 0
        
class Population(object):

    target = ''
    mutationRate = 0
    population = 0

    targetScore = 0
    totalScore = 0
    populationList = list()
            
    #Constructor
    def __init__(self, target, mutationRate, population):
        self.target = target
        self.mutationRate = mutationRate
        self.population = population
        self.targetScore = 2**len(target)
        self.populationList = self.initPopulation(target, len(target), population)

    ##GENETIC RULES##
    #Initialization
    def initPopulation(self, target, length, population):
        currentPopulation = 0
        newPopulationList = list()
        while currentPopulation < population:
            newDna = ''
            count = 0
            while count < length:
                newDna = newDna + self.newChar()
                count += 1
            newChild = GeneticElement()
            newChild.dna = newDna
            newChild.score = self.fitnessFunction(target, length, newDna)
            newPopulationList.append(newChild)
            currentPopulation += 1
        return newPopulationList
    #Selection
    def fitnessFunction(self, target, length, dna):
        score = 0
        position = 0
        while position < length:
            if target[position] == dna[position]:
                score += 1
            position += 1
        return 2**score
    #Heredity
    def crossover(self, length, parentA, parentB):
        newDna = ''
        scoreA = parentA.score
        scoreB = parentB.score
        totalScore = scoreA + scoreB
        count = 0
        while count < length:
            #The fittest is more likely to pass its genes
            if random.randint(0, totalScore) < scoreA:
                newDna = newDna + parentA.dna[count]
            else:
                newDna = newDna + parentB.dna[count]
            count += 1
        return newDna
    #Variation
    def newChar(self):
        c = random.randint(63, 122)
        if c == 63:
            c = 32
        if c == 64:
            c = 46
        return chr(c)
    def mutation(self, dna, mutationRate):
        newDna = ''
        for i, character in enumerate(dna):
            if random.randint(0, 99) < mutationRate:
                newDna = newDna + self.newChar()
            else:
                newDna = newDna + character
        return newDna
    def crossMutation(self, target, length, parentA, parentB, mutationRate):
        """Crossover + Mutation"""
        newChild = GeneticElement()
        dna = self.crossover(length, parentA, parentB)
        newChild.dna = self.mutation(dna, mutationRate)
        newChild.score = self.fitnessFunction(target, length, newChild.dna)
        return newChild

    ##GENETIC ENGINE##
    def getTotalScore(self):
        """Sums the score of all the population to do the probability calculations"""
        newScore = 0;
        for i, element in enumerate(self.populationList):
            newScore += element.score
        return newScore
    def pickRandomParent(self, lastScore):
        """Returns a random parent Id with probability pi / (p1 + p2 + ... + pn) with p being its score.
        It is executed when there's 2 or more eligible parents."""
        comparableScore = random.randint(0, lastScore)
        currentScore = 0
        count = 0
        while currentScore < comparableScore:
            currentScore += self.populationList[count].score
            if currentScore < comparableScore:
                count += 1
        return count    
    def newGeneration(self, target, length, mutationRate, population, populationList):
        """Creates one generation."""
        lastScore = self.getTotalScore()
        newGenerationList = list()
        #lastScore = 0 implies there's no preferred parent
        if lastScore == 0:
            count = 0
            while count < population:
                #Randomly picks 2 parents
                parentCouple = random.sample(populationList, 2)
                parentA = parentCouple[0]
                parentB = parentCouple[1]
                #Creates new child
                newChild = self.crossMutation(target, length, parentA, parentB, mutationRate)
                newGenerationList.append(newChild)
                count += 1
        else:
            myMaxScore = 0
            maxScoreId = -1
            for i, element in enumerate(populationList):
                if(element.score > myMaxScore):
                    myMaxScore = element.score
                    maxScoreId = i;            
            #lastScore = myMaxScore implies there's just 1 preferred parent since lastScore > 0
            if lastScore == myMaxScore:
                count = 0
                while count < population:
                    parentIdB = random.randint(1, population) - 1
                    #Forces both parents to be different
                    while parentIdB == maxScoreId:
                        parentIdB = random.randint(1, population) - 1
                    parentA = populationList[maxScoreId]
                    parentB = populationList[parentId2]
                    #Creates child
                    newChild = self.crossMutation(target, length, parentA, parentB, mutationRate)
                    newGenerationList.append(newChild)
                    count += 1
            #lastScore != myMaxScore is the regular case where there's 2 or more eligible parents
            else: 
                count = 0
                while count < self.population:
                    parentIdA = self.pickRandomParent(lastScore)
                    parentIdB = self.pickRandomParent(lastScore)
                    #Forces all parents to be different
                    while parentIdA == parentIdB:
                        parentIdB = self.pickRandomParent(lastScore)
                    #Creates parents
                    parentA = populationList[parentIdA]
                    parentB = populationList[parentIdB]
                    #Creates child
                    newChild = self.crossMutation(target, length, parentA, parentB, mutationRate)
                    newGenerationList.append(newChild)
                    count += 1
        return newGenerationList
    
    ##THE MAIN SCRIPT##
    def run(self):
        """Runs the simulation"""
        myMaxScore = 0
        count = 0
        print('')
        print('\t{}\t{}\t\t {}'.format('Generation', 'Best', 'Score'))
        print('\t---------------------------------------------------')
        length = len(self.target)
        maxScore = self.targetScore
        while myMaxScore < self.targetScore:
            count += 1
            bestId = -1
            bestDna = ''
            actualMaxScore = 0
            for i, element in enumerate(self.populationList):
                if element.score > actualMaxScore:
                    actualMaxScore = element.score
                    bestDna = element.dna
                    if actualMaxScore > myMaxScore:
                        myMaxScore = actualMaxScore
            print('\t{}\t\t{}\t\t {}/{}'.format(count, bestDna, actualMaxScore, maxScore))
            if myMaxScore < self.targetScore:
                self.populationList = self.newGeneration(self.target, length, self.mutationRate, self.population, self.populationList)
        print()
        print('\tEncontrado: \'' + self.target + '\' tras ' + str(count) + ' generaciones')
        print('\tMutation Rate: ' + str(self.mutationRate) + '% chance\tPopulation: ' + str(self.population) + ' individuals')
        print()
    def runCount(self, stopCount):
        myMaxScore = 0
        count = 0
        length = len(self.target)
        maxScore = self.targetScore
        while count < stopCount and myMaxScore < self.targetScore:
            count += 1
            bestId = -1
            bestDna = ''
            actualMaxScore = 0
            for i, element in enumerate(self.populationList):
                if element.score > actualMaxScore:
                    actualMaxScore = element.score
                    bestDna = element.dna
                    if actualMaxScore > myMaxScore:
                        myMaxScore = actualMaxScore
            if myMaxScore < self.targetScore:
                self.populationList = self.newGeneration(self.target, length, self.mutationRate, self.population, self.populationList)
        return count

class PopulationMap(object):

    target = ''
    stopCount = 0
    minPopulation = 0
    maxPopulation = 0
    minMutationRate = 0
    maxMutationRate = 0

    #Constructor
    def __init__(self, target, stopCount, minPopulation, maxPopulation, minMutationRate, maxMutationRate):
        self.target = target
        self.stopCount = stopCount
        self.minPopulation = minPopulation
        self.maxPopulation = maxPopulation
        self.minMutationRate = minMutationRate
        self.maxMutationRate = maxMutationRate
    #Matrix simulator
    def fillMap(self, target, stopCount, minPopulation, maxPopulation, minMutationRate, maxMutationRate):
        nextRow = False
        population = minPopulation
        print()
        print('\t{}\t{}\t{}'.format('Population', 'Rate', 'Count'))
        print('\t------------------------------------')
        print()
        while population < maxPopulation:
            mutationRate = minMutationRate
            while nextRow == False:
                myPopulation = Population(target, mutationRate, population)
                count = myPopulation.runCount(stopCount)
                if count == stopCount or mutationRate == maxMutationRate:
                    nextRow = True
                else:
                    print('\t{}\t\t{}\t{}'.format(population, mutationRate, count))
                    mutationRate += 1
            nextRow = False
            population += 5
    #Runs the script
    def run(self):
        self.fillMap(self.target, self.stopCount, self.minPopulation, self.maxPopulation, self.minMutationRate, self.maxMutationRate)
        
#Runs the script
#Population('to be or not to be', 10, 100).run()
Population('unicorn', 5, 100).run()
#PopulationMap('abcdefghij', 200, 30, 100, 1, 10).run()


#TODO: Missing phenotype at GeneticElement

