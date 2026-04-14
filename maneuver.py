import numpy as np

def calculate_delta_v(obj1, obj2):
    relative_velocity = np.linalg.norm(obj1.velocity - obj2.velocity)
    return relative_velocity * 0.1

def fuel_required(delta_v, mass=500):
    return mass * delta_v * 0.05

def decide_action(risk, min_dist):
    if risk == "LOW":
        return "No Action"
    elif risk == "MEDIUM":
        return "Orbit Adjustment"
    else:
        return "Emergency Maneuver"
