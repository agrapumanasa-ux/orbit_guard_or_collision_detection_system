import numpy as np

class SpaceObject:
    def __init__(self, obj_id, position, velocity, mass=500):
        self.id = obj_id
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.mass = mass

    def update_position(self, dt):
        self.position = self.position + self.velocity * dt

    def predict_position(self, t):
        return self.position + self.velocity * t
