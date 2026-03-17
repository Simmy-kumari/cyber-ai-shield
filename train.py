import torch
import numpy as np
import joblib
from model import Autoencoder
from preprocess import preprocess

X_train,y_train,X_test,y_test = preprocess(
    "data/KDDTrain+.txt",
    "data/KDDTest+.txt"
)

# Train ONLY on normal data
X_train = X_train[y_train==0]

X_tensor = torch.tensor(X_train,dtype=torch.float32)

model = Autoencoder(X_tensor.shape[1])

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=0.001)

for epoch in range(20):

    optimizer.zero_grad()

    output = model(X_tensor)

    loss = criterion(output,X_tensor)

    loss.backward()

    optimizer.step()

    print("Epoch:",epoch+1,"Loss:",loss.item())

torch.save(model.state_dict(),"models/autoencoder.pth")

# Threshold calculation
with torch.no_grad():
    reconstruction = model(X_tensor)
    error = torch.mean((X_tensor-reconstruction)**2,dim=1).numpy()

threshold = np.percentile(error,95)

joblib.dump(threshold,"models/threshold.pkl")

print("Model Training Complete")