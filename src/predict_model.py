import joblib
import numpy as np

model = joblib.load("models/yield_model.pkl")

def predict_crop_yield(
    rainfall,
    humidity,
    sunshine,
    nitrogen,
    phosphorus,
    potassium,
    ph
):
    X = np.array([[
        rainfall,
        humidity,
        sunshine,
        nitrogen,
        phosphorus,
        potassium,
        ph
    ]])

    return model.predict(X)[0]