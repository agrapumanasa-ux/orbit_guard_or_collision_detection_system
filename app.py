import streamlit as st
import numpy as np
from core.objects import SpaceObject
from core.physics import predict_trajectory
from core.collision import predict_min_distance
from core.ai_model import load_model, predict_collision_risk
from core.maneuver import calculate_delta_v, fuel_required, decide_action
from core.swarm import swarm_alert
from visualization.plot_3d import plot_objects

st.set_page_config(layout="wide")
st.title("🚀 AI Satellite Collision Avoidance System")

num_objects = st.slider("Number of Objects", 2, 5, 2)
objects = []

for i in range(num_objects):
    x = st.number_input(f"x{i}", value=100*i)
    y = st.number_input(f"y{i}", value=50*i)
    z = st.number_input(f"z{i}", value=30*i)

    vx = st.number_input(f"vx{i}", value=1+i)
    vy = st.number_input(f"vy{i}", value=2+i)
    vz = st.number_input(f"vz{i}", value=1+i)

    obj = SpaceObject(f"SAT-{i}", [x,y,z], [vx,vy,vz])
    objects.append(obj)

model = load_model()
results = []

for i in range(len(objects)):
    for j in range(i+1, len(objects)):
        min_dist, ttc = predict_min_distance(objects[i], objects[j])
        rel_vel = np.linalg.norm(objects[i].velocity - objects[j].velocity)
        prob, risk = predict_collision_risk(model, [min_dist, rel_vel])
        delta_v = calculate_delta_v(objects[i], objects[j])
        fuel = fuel_required(delta_v)
        action = decide_action(risk, min_dist)

        results.append((objects[i].id, objects[j].id, prob, risk, action, fuel))

for r in results:
    st.write(r)

trajectories = [predict_trajectory(obj) for obj in objects]
fig = plot_objects(objects, trajectories)
st.plotly_chart(fig)
