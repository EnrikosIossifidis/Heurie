# Algorithms

The following algorithms are included in this folder (categorized):

Random function
Constructive: depthfirst branch-n-bound
Iterative: hillclimber for houses, hillclimber for battery location
Population Based: Evolutionary algorithm
Cluster: K-means

# Evolutionary algorithm 

The new population consists of children created during recombination. Depending on the input parameters more children than parents are created. Through fitness proportionate selection the children are selected to form the new population. If conflict resolvement is enabled it is possible that children die during the recombination process. This occurs when the effort put into making it meet the constraints does not yield any result within the set amount of attempts. In a situation where less children are generated than the initial population size individuals are taken up more than once in the new generation. 

## To run the evolutionary algorithm the following parameters are required: 

(1) environment

(2) maximumGenerations

(3) populationSize

(4) crossoversPerParent 

(5) matingPartners

(6) parentDominance 

(7) mutationProbability 

(8) crossoverProbability 

(9) conflictResolvement


## (1) environment (Environment)

An object of type "Environment", containing locations of houses and batteries as well as their capacity, as specified earlier. 

## (2) maximumGenerations (Int)

The number of generations, stop criterium. 

## (3) populationSize (Int)

The amount of individuals in the initial population. The size of the population is remains constant over time. 

## (4) crossoverPerParent (Int)

For every couple of parents two crossovers are performed, in which both parents are the most dominant genome once. Which part of the genome is passed on to the child is decided randomly.
The crossoverPerParent parameter indicates how many crossovers occur (children are created) for one parent in a pair of parents. 

## (5) matingPartners (Int)

The amount of mating partners that an individual makes children with. 

## (6) parentDominance (Float)

The share of the genome of the first parent that is copied to the child.

## (7) mutationProbability (Float)

The probability that a mutation occurs during recombination. 

## (8) crossoverProbability (Float)

The probability that crossover occurs, i.e. a parent's genome is combined with its partner's to form a new child. If crossover does not occur, the genome of the parent is taken up in the next population unchanged. 

## (9) conflictResolvement (Boolean)

If True, the child created during recombination is adapted to meet the constraints. During conflict resolvement houses from the batteries of which the capacity is exceeded are randomly assigned to a different battery. 

