import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train():
    df = pd.read_csv("data/crop_dataset.csv")

    X = df[
        [
            "rainfall",
            "humidity",
            "sunshine",
            "nitrogen",
            "phosphorus",
            "potassium",
            "ph"
        ]
    ]
    y = df["yield"]

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, "models/yield_model.pkl")

    print("✅ AI model trained")

if __name__ == "__main__":
    train()