# Smart Grids

Smart grids gaat over het optimaliseren van een energienetwerk in 3 verschillende wijken. Elk huis in deze wijken levert energie dat moet worden opgeslagen in batterijen.

## Aan de slag (Getting Started)

### Verseisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.6.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip door miidel van de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

Alle Python scripts staan in de folder Code. In de map Data zitten alle inputwaardes en in de map resultaten worden alle resultaten opgeslagen door de code.

### Test (Testing)

Om de code te draaien met de standaardconfiguratie (bv. brute-force en voorbeeld.csv) gebruik de instructie:

```
python main.py
```

-----------------------------
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

## Auteurs (Authors)

* Milou Nederstigt
* Enrikos Iossifidis
* Pelle Groot

## Dankwoord (Acknowledgments)

* Daan van den Berg
* Quinten van der Post
* StackOverflow
* minor programmeren van de UvA
