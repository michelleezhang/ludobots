import numpy as numpy
import matplotlib.pyplot

# backLegSensorValues = numpy.load('data/backLegSensorValues.npy')
# print(backLegSensorValues)
# matplotlib.pyplot.plot(backLegSensorValues, label='Back leg', linewidth=3)

# frontLegSensorValues = numpy.load('data/frontLegSensorValues.npy')
# matplotlib.pyplot.plot(frontLegSensorValues, label='Front leg')

targetAngles_back = numpy.load('data/targetAngles_back.npy')
matplotlib.pyplot.plot(targetAngles_back, label="Back leg target angles")
targetAngles_front = numpy.load('data/targetAngles_front.npy')
matplotlib.pyplot.plot(targetAngles_front, label="Front leg target angles")

matplotlib.pyplot.xlabel('Steps')
matplotlib.pyplot.ylabel('Value in Radians')
matplotlib.pyplot.axis('tight')

matplotlib.pyplot.legend(loc='upper right')
matplotlib.pyplot.show()