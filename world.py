import pybullet as p
import pybullet_data

class WORLD:
    def __init__(self):
        # add a floor
        self.planeId = p.loadURDF("plane.urdf")

        # tells pybullet to read in the world described in box.sdf
        p.loadSDF("world.sdf")