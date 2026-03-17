import pandas as pd

# Read TXT dataset
train = pd.read_csv("data/KDDTrain+.txt", header=None, delimiter=",")
test = pd.read_csv("data/KDDTest+.txt", header=None, delimiter=",")

# Save as CSV
train.to_csv("data/train.csv", index=False)
test.to_csv("data/test.csv", index=False)

print("Conversion completed!")