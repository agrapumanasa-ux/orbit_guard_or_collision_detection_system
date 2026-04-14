import streamlit as st
import numpy as np
import pandas as pd
from sgp4.api import Satrec, jday
from datetime import datetime

from core.objects import SpaceObject
from core.physics import predict_trajectory
from core.maneuver import calculate_delta_v, fuel_required, decide_action
from visualization.plot_3d import plot_objects

def tle_to_state(line1, line2):
    sat = Satrec.twoline2rv(line1, line2)
    now = datetime.utcnow()
    jd, fr = jday(now.year, now.month, now.day,
                  now.hour, now.minute, now.second)
    e, r, v = sat.sgp4(jd, fr)
    if e != 0:
        return None, None
    return np.array(r), np.array(v)

def predict_min_distance(obj1, obj2, time_steps=50):
    min_dist = float("inf")
    best_t = 0
    for t in range(time_steps):
        pos1 = np.array(obj1.position) + np.array(obj1.velocity) * t
        pos2 = np.array(obj2.position) + np.array(obj2.velocity) * t
        dist = np.linalg.norm(pos1 - pos2)
        if dist < min_dist:
            min_dist = dist
            best_t = t
    return round(min_dist, 2), best_t

def calculate_risk(min_dist, rel_vel):
    score = (1 / (min_dist + 1)) * rel_vel * 100
    if score > 5:
        return 0.9, "HIGH"
    elif score > 2:
        return 0.5, "MEDIUM"
    else:
        return 0.1, "LOW"

st.set_page_config(layout="wide")
st.title("🚀 AI Satellite Collision Avoidance System")
st.write("Real-time satellite & debris collision prediction using TLE data")

tle_data = [
    ("CALSPHERE 1",
     "1 00900U 64063C   26074.97769105  .00000630  00000+0  63342-3 0  9990",
     "2 00900  90.2164  69.5934 0024172 210.5039 203.4549 13.76506345 58601"),
    ("IRIDIUM 33",
     "1 24946U 97051C   26074.93146146  .00000272  00000+0  88422-4 0  9998",
     "2 24946  86.3894  29.0790 0005718 272.3789  87.6752 14.35105441491716"),
    ("IRIDIUM 33 DEB",
     "1 33773U 97051L   26074.88953291  .00001031  00000+0  29910-3 0  9997",
     "2 33773  86.4046  21.0964 0010030 194.6044 165.4868 14.43495291896910"),
]

objects = []
for name, l1, l2 in tle_data:
    pos, vel = tle_to_state(l1, l2)
    if pos is not None:
        obj = SpaceObject(name, pos, vel)
        obj.type = "DEBRIS" if "DEB" in name else "SATELLITE"
        objects.append(obj)

st.write("Objects Loaded:", len(objects))

sat_count = sum(1 for o in objects if o.type == "SATELLITE")
deb_count = sum(1 for o in objects if o.type == "DEBRIS")

col1, col2, col3 = st.columns(3)
col1.metric("Satellites", sat_count)
col2.metric("Debris", deb_count)
col3.metric("Total Objects", len(objects))

results = []
for i in range(len(objects)):
    for j in range(i + 1, len(objects)):
        min_dist, ttc = predict_min_distance(objects[i], objects[j])
        rel_vel = np.linalg.norm(
            np.array(objects[i].velocity) - np.array(objects[j].velocity)
        )
        prob, risk = calculate_risk(min_dist, rel_vel)
        delta_v = calculate_delta_v(objects[i], objects[j])
        fuel = fuel_required(delta_v)
        action = decide_action(risk, min_dist)

        results.append([
            objects[i].id,
            objects[j].id,
            min_dist,
            ttc,
            round(rel_vel, 2),
            prob,
            risk,
            action,
            round(fuel, 2)
        ])

st.subheader("📊 Collision Analysis Results")

if results:
    df = pd.DataFrame(results, columns=[
        "Object A","Object B","Min Distance (km)","Time to Closest",
        "Relative Velocity","Collision Probability","Risk Level",
        "Suggested Action","Fuel Required"
    ])

    def highlight_risk(val):
        if val == "HIGH":
            return "background-color: red; color: white"
        elif val == "MEDIUM":
            return "background-color: orange"
        else:
            return "background-color: green; color: white"

    st.dataframe(df.style.applymap(highlight_risk, subset=["Risk Level"]))

    high_risk = df[df["Risk Level"] == "HIGH"]
    if not high_risk.empty:
        st.error("⚠️ High Collision Risk Detected!")
    else:
        st.success("✅ All objects are safe")
else:
    st.warning("No data to display")

st.subheader("🛰️ 3D Trajectory Visualization")

if objects:
    trajectories = [predict_trajectory(obj) for obj in objects]
    fig = plot_objects(objects, trajectories)
    st.plotly_chart(fig)
else:
    st.warning("No objects to visualize")
