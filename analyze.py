import numpy as numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load('data/backLegSensorValues.npy')
print(backLegSensorValues)
matplotlib.pyplot.plot(backLegSensorValues, label='Back leg', linewidth=3)

frontLegSensorValues = numpy.load('data/frontLegSensorValues.npy')
matplotlib.pyplot.plot(frontLegSensorValues, label='Front leg')

matplotlib.pyplot.legend()
matplotlib.pyplot.show()