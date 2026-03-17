import torch
import numpy as np
import pandas as pd
import joblib
from model import Autoencoder

device = torch.device("cpu")

# Load once
scaler = joblib.load("models/scaler.pkl")
threshold = joblib.load("models/threshold.pkl")
reference_columns = joblib.load("models/reference_columns.pkl")

model = Autoencoder(len(reference_columns))
model.load_state_dict(torch.load("models/autoencoder.pth", map_location=device))
model.eval()

def detect(X):

    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)

    # One-hot encoding
    X = pd.get_dummies(X)

    # Align columns
    X = X.reindex(columns=reference_columns, fill_value=0)

    # Scale
    X_scaled = scaler.transform(X)

    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)

    with torch.no_grad():
        reconstruction = model(X_tensor)

    error = torch.mean((X_tensor - reconstruction)**2, dim=1).numpy()

    predictions = (error > threshold).astype(int)

    # Risk metrics
    severity = ["High Risk" if e > threshold else "Normal" for e in error]
    confidence = np.round(error * 100, 2)
    risk_percentage = np.clip(error * 100, 0, 100)

    return predictions, error, severity, confidence, risk_percentage