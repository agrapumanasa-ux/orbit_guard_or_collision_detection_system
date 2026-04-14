import numpy as np

def predict_trajectory(obj, time_steps=50, dt=1):
    positions = []
    pos = obj.position.copy()

    for _ in range(time_steps):
        pos = pos + obj.velocity * dt
        positions.append(pos.copy())

    return np.array(positions)
