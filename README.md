# ludobots
This project showcases the simulated evolution of 3D rigid robots. 
<p align="center">
    <img src="./ludobots-final trailer - 4K.gif" width="50%" height="50%"/>
</p>

Video: https://youtu.be/uKB8FFeYaAg 

# robot generation
Robots are composed of 3D blocks called "links" connected by joints, and have sensors that define how the robot moves. This program generates 3D jointed, motorized, and sensorized robots with a random number of links (with random dimensions) and random sensor placement. Links with sensors are colored green, and links without sensors are colored blue.

First, a "spine" chain is grown in the y-direction. A random number 'num_links' is generated to determine the number of links in the chain. A "base" link is generated first, positioned at (0, 0) in 2D space. From there, the remaining links (given randomized dimensions) are added to the chain. 

Next, "branches" are added in the x and z directions. For each direction, the program loops through each of the existing links in the "spine." At each iteraction, a (randomly generated) number of links to add in the given direction is produced, and that number of joint-link pairs is added to the given spine link.

The diagram below provides a visual summary of the growth process.
<p align="center">
    <img src="./Computer Science 396_ Artificial Life-22.jpg" width="50%" height="50%"/>
</p>

In both of the phenotype diagrams above, the green arrows show the direction of growth of the branch links (colored blue) at each spine link (colored black).

Each time a new joint and link pair is generated, a random boolean value is also generated to decide whether or not that link will have a sensor. Sensor neurons are added only for the links for which this boolean is set to True. The link is colored green if the sensor boolean is True, and blue otherwise. Random values for the entire program were generated using the random module.

Random robot generation occurs in the solution.py file.

# robot evolution

Evolution was simulated by mutating the randomly generated robots at each generation. The type of mutation made was randomly determined. The possible types of mutations were:
- The probability of more links in the x, y, or z directions was increased 
- The probability of fewer links in the x, y, or z directions was increased
- The probability of larger links was increased
- The probability of smaller links was increased
To select a mutation, a random integer was generated between 1 and 10, each corresponding to a different mutation. This resulted in a 10% chance of each type of body mutation, and a 20% chance of a mutation that alters a synapse weight. Thiis process is depicted in the following diagram.
- The weights of the synapses were randomly altered
<p align="center">
    <img src="./Computer Science 396_ Artificial Life-23.jpg" width="70%" height="70%"/>
</p>

If a mutation in the parent led to an increase in fitness for the child, the child replaced the parent, thus keeping track of the maximum obtained fitness.

Evolution used parallel hill climber, which runs a given number of generations with a given number of randomly generated parents per generation. At each generation, a mutation is made to the parent to produce a child. The fitness of the child is calculated, and if it is more fit than the parent, the child replaces the parent in the following generation. At the end of all of the generations, the robot with the best fitness overall is selected.
<p align="center">
    <img src="./Computer Science 396_ Artificial Life-21.jpg" width="50%" height="50%"/>
</p>

The fitness curves are shown below.
<p align="center">
    <img src="./FFigureAGAIIN.png" width="50%" height="50%"/>
</p>

Robot mutation occurs in the solution.py file, and the PHC algorithm is run in the parallelHillClimber.py file.


# usage
Run search.py to generate a random kinematic chain.
>python3 search.py

Run analyze.py to generate a fitness plot.
>python3 analyze.py

Run pickled.py to see one of the saved robots.
>python3 pickled.py <robot_number>
e.g. If you would like to run robot0 in the saved robots, run
>python3 pickled.py 0
To see the saved robot data, see the best_robots folder, which contains the body.urdf and brain.nndf of several of the best evolved robots.

Python package requirements: random, numpy, pybullet

# sources
- Ludobots MOOC on Reddit (https://www.reddit.com/r/ludobots/)
- Evolving Virtual Creatures by Karl Sims (https://www.karlsims.com/papers/siggraph94.pdf)
- Project built on pyrosim (https://github.com/jbongard/pyrosim)
