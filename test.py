import pandas as pd

data = pd.read_csv('rba-dataset.csv')

print(data.head())

A = data.iloc[:int(len(data)/2)]
B = data.iloc[int(len(data)/2):]

# A.to_csv('A.csv', index=False)
# B.to_csv('B.csv', index=False)