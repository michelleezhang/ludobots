# ludobots: random snake
This program generates a kinematic chain (a jointed, motorized, sensorized snake) with a random number of links (with random dimensions) and random sensor placement along the chain. Links with sensors are colored green, and links without sensors are colored blue.

A random number 'num_links' is generated first to determine the number of links in the chain. Then a vector of length 'num_links' is created, filled with random numbers -- these provide the z-directional lengths of the links. A "base" link is generated first, positioned at (0, 0) in 2D space, with a height that is half of its corresponding random z-directional length. From there, the remaining links (given randomized x and y dimensions) are added to the chain. Each time a new joint and link pair is generated, a random boolean value is also generated to decide whether or not that link will have a sensor. Sensor neurons are added only for the links for which this boolean is set to True. The link is colored green if the sensor boolean is True, and blue otherwise. Random values for the entire program were generated using the random module.

# usage
Run search.py to generate a random kinematic chain.
>python3 search.py
