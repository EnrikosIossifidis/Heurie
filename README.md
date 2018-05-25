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

(1) maximumGenerations, 

(2) populationSize, 

(3) mutationProbability, 

(4) crossoverProbability,


(1) maximumGenerations (Int)

The number of generations, stop criterium. 

(2) populationSize (Int)

The amount of individuals in the initial population. The size of the population is remains constant over time. 

(3) mutationProbability (Float)

The probability that a mutation occurs during recombination. 

(4) crossoverProbability (Float)

The probability that crossover occurs, i.e. a parent's genome is combined with its partner's to form a new child. If crossover does not occur, the genome of the parent is taken up in the next population unchanged. 


## Auteurs (Authors)

* Milou Nederstigt
* Enrikos Iossifidis
* Pelle Groot

## Dankwoord (Acknowledgments)

* Daan van den Berg
* Quinten van der Post
* StackOverflow
* minor programmeren van de UvA
