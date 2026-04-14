import numpy as np

def calculate_distance(obj1, obj2):
    return np.linalg.norm(obj1.position - obj2.position)

def predict_min_distance(obj1, obj2, steps=50):
    min_dist = float('inf')
    time_to_collision = -1

    for t in range(steps):
        p1 = obj1.predict_position(t)
        p2 = obj2.predict_position(t)

        dist = np.linalg.norm(p1 - p2)

        if dist < min_dist:
            min_dist = dist
            time_to_collision = t

    return min_dist, time_to_collision
