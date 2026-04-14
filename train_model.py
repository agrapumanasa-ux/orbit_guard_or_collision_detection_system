import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("data/sample_data.csv")

X = df[['distance', 'relative_velocity']]
y = df['collision']

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "models/collision_model.pkl")
print("Model trained!")
