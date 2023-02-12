# ludobots: random snake
This program generates a kinematic chain (a jointed, motorized, sensorized snake) with a random number of links (with random dimensions) and random sensor placement along the chain. Links with sensors are colored green, and links without sensors are colored blue.

A "base" link is generated first, positioned at (0, 0) in 2D space. From there, a random number of additional links of randomized dimensions are added to the chain. Each time a joint and link pair is generated, a random boolean value is also generated to decide whether or not that link will have a sensor. Sensor neurons are added only for the links for which this boolean is set to True. The pyrosim module was modified to generate a green link if the sensor boolean is True, and a blue link otherwise. Random values for the entire program were generated using the random module.

# usage
Run search.py to generate a random kinematic chain.
>python3 search.py
