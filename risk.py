import numpy as np

def risk_engine(error, threshold):

    severity = []
    confidence = []
    risk_percentage = []

    for e in error:
        if e > threshold:
            if e > threshold * 2:
                severity.append("High Risk")
            elif e > threshold * 1.5:
                severity.append("Medium Risk")
            else:
                severity.append("Low Risk")
        else:
            severity.append("Normal")

        confidence.append(round(e * 100, 2))
        risk_percentage.append(min(e * 100, 100))

    return severity, confidence, risk_percentage