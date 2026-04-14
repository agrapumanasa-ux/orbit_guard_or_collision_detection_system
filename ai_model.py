import joblib

MODEL_PATH = "models/collision_model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def predict_collision_risk(model, features):
    prob = model.predict_proba([features])[0][1]

    if prob < 0.3:
        return prob, "LOW"
    elif prob < 0.7:
        return prob, "MEDIUM"
    else:
        return prob, "HIGH"
