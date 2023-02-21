# ludobots: morphospace
This program generates a 3D creature (jointed, motorized, sensorized) with a random number of links (with random dimensions) and random sensor placement along the chain. Links with sensors are colored green, and links without sensors are colored blue.


First, a chain is grown in the y-direction. A random number 'num_links' is generated first to determine the number of links in the chain. Then a vector of length 'num_links' is created, filled with random numbers -- these provide the z-directional lengths of the links. 
A "base" link is generated first, positioned at (0, 0) in 2D space, with a height that is half of its corresponding random z-directional length. From there, the remaining links (given randomized x and y dimensions) are added to the chain. 
Each time a new joint and link pair is generated, a random boolean value is also generated to decide whether or not that link will have a sensor. Sensor neurons are added only for the links for which this boolean is set to True. The link is colored green if the sensor boolean is True, and blue otherwise. Random values for the entire program were generated using the random module.

An analogous process is performed to add "branches" in the x and z directions. 
The diagram below provides a visual summary of the growth process.
<p align="center">
    <img src="./sims-diag.jpg" width="30%" height="30%"/>
</p>
For each direction, the program loops through each of the existing links in the y-directional chain. In this way, the y-directional chain can be treated as a "spine," off of which additional links can branch out. At each of these "spine" links, a random number of links to add in the given direction is generated. That number of joint-link pairs is added to the spine link. Using the same process as before, these "branch" links are given a sensor randomly. Those with sensors are green, and those without are blue.



The diagram below shows an example of branching in the x direction.
<p align="center">
    <img src="./x-graph.jpg" width="30%" height="30%"/>
</p>
The diagram below shows an example of branching in the z direction.
<p align="center">
    <img src="./x-graph.jpg" width="30%" height="30%"/>
</p>
In both of the diagrams above, the green arrows show the direction of growth of the branch links (colored blue) at each spine link (colored black).


# usage
Run search.py to generate a random kinematic chain.
>python3 search.py

Python package requirements: random, numpy, pybullet

# sources
- Computer Science 396 (Artificial Life) course at Northwestern University
- Ludobots MOOC on Reddit (https://www.reddit.com/r/ludobots/)
- Evolving Virtual Creatures by Karl Sims (https://www.karlsims.com/papers/siggraph94.pdf)
