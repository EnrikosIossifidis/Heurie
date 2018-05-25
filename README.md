# Smart Grids

Smart grids is about optimizing the energy distribution between 150 houses and 5 batteries in a village. In this case we have to optimize three villages.

## Getting Started

### Prerequisites

The whole codebase is fully written in [Python3.6.3](https://www.python.org/downloads/). In the requirements.txt are all the neede packages to run the code succesfully. These are easy to install through pip following the next instruction:

```
pip install -r requirements.txt
```

### Structure

All python scripts are in the folder "code". Within this folder there are three folders (algorithms, classes and functions), a main.py and a README.
The folder algorithms contains all the written algorithms and variantions on these algorithms. In the folder classes are the two data classes we use (model & environment). And in the folder functions are the functions we use to make visualisation or to help running the algorithms. 

### Testing

To run the code use the next statement, where n is the number of the village you want to use (village 1, 2 or 3):

```
python main.py n
```

From this point on a menu in the terminal will guide you.
The menu will ask which algorithm you want to use.
    For getting the distribution of house to batteries:
        1: Random
        2: Depth first with branch & Bound 
        3: Hill climber
        4: Simulated Annealing
        5: Evolution
    For getting new locaties of the batteries 
        6: K-means 
        7: Hill climber on the batteries

After choosing an algorithm, the menu will guide you through filling in the parameters. The parameters should be filled in with a space in between. For example for the hill climber:
```
30 1 1 10
```
Not every algorithm needs parameter, the depth first algorithm starts when you choose it.
The other algorithms need parameters. The parameters for the simulated annealing is similar to the hill climber but the simulated annealing has an additional parameter.
The hillclimber for the battery is the same as the simulated annealing.

### Instructions to run the hill climbers and the simulated annealing

To run the hillclimber algorithms the following parameters are required as input:
(1) iteration
(2) choose constraints
(3) choose mutation
(4) amount of moves
(5) cooling scheme (only for simulated annealing and hill climber for moving batteries)

(1) iteration is the amount of iterations the algorithm goes through. 
(2) choose constraints is the choice of if you want to run the algorithm with the constraint check or not.
(3) choose mutation is the choice of how the algorithm behaves. Does it switch two houses between batteries or does it moves a house from one battery to another.
(4) amount of moves the algorithm makes before checking the validity of the model.
(5) cooling scheme is the choice of what cooling scheme the simulated annealing follows.


#### Instructions to run the evolutionary algorithm

To run the evolutionary algorithm the following parameters are required as input: 

(1) environment,
(2) maximumGenerations, 
(3) populationSize, 
(4) crossoversPerParent, 
(5) matingPartners, 
(6) parentDominance, 
(7) mutationProbability, 
(8) crossoverProbability,
(9) conflictResolvement

(1) environment (Environment)
An object of type "Environment", containing locations of houses and batteries as well as their capacity, as specified earlier. 

(2) maximumGenerations (Int)
The number of generations, stop criterium. 

(3) populationSize (Int)
The amount of individuals in the initial population. The size of the population is remains constant over time. 

(4) crossoverPerParent (Int)
For every couple of parents two crossovers are performed, in which both parents are the most dominant genome once. Which part of the genome is passed on to the child is decided randomly.
The crossoverPerParent parameter indicates how many crossovers occur (children are created) for one parent in a pair of parents. 

(5) matingPartners (Int)
The amount of mating partners that an individual makes children with. 

(6) parentDominance (Float)
The share of the genome of the first parent that is copied to the child.

(7) mutationProbability (Float)
The probability that a mutation occurs during recombination. 

(8) crossoverProbability (Float)
The probability that crossover occurs, i.e. a parent's genome is combined with its partner's to form a new child. If crossover does not occur, the genome of the parent is taken up in the next population unchanged. 

(9) conflictResolvement (Boolean)
If True, the child created during recombination is adapted to meet the constraints. During conflict resolvement houses from the batteries of which the capacity is exceeded are randomly assigned to a different battery. 

## Authors

* Milou Nederstigt
* Enrikos Iossifidis
* Pelle Groot

## Acknowledgments

* Daan van den Berg
* Quinten van der Post
* StackOverflow
* minor programmeren van de UvA
