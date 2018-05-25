# Classes

This map contains the data structure of the case. The structure is split up in a environment and model.

Environment: Contains the data which is provided by the case. Several functions (e.g. distanceTable) are built in the Environment data structure. The functions can be calculated with just the data that the case provides.

Model: Contains the results which is calculated by the algorithms. The functions herein can only be calculated if the houses are assigned to the batteries, but it is not necessary to satisfy the constraints to make a model.