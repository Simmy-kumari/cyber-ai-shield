import torch
import numpy as np
import joblib
from model import Autoencoder
from risk import risk_engine

def detect(X):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load scaler
    scaler = joblib.load("models/scaler.pkl")
    X = scaler.transform(X)

    # Convert to tensor
    X_tensor = torch.FloatTensor(X).to(device)

    # Load model
    model = Autoencoder(X.shape[1]).to(device)
    model.load_state_dict(torch.load("models/autoencoder.pth", map_location=device))
    model.eval()

    # Reconstruction
    with torch.no_grad():
        reconstruction = model(X_tensor)

    # Calculate reconstruction error
    error = torch.mean((X_tensor - reconstruction) ** 2, dim=1)
    error = error.cpu().numpy()

    # Load threshold
    threshold = joblib.load("models/threshold.pkl")

    # Prediction
    predictions = (error > threshold).astype(int)

    # Risk Analysis
    severity, confidence, risk_percentage = risk_engine(error, threshold)

    return predictions, error, severity, confidence, risk_percentage