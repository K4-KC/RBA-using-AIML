import pandas as pd

data = pd.read_csv('data/rba-dataset.csv')

print(data.head())

split = [None for i in range(24)]
j1, j2 = 0, int(len(data)/24)
print(len(data))
print(j1, j2)
input('press enter to continue')

for i in range(24):
    split[i] = data.iloc[j1:j1 + j2]
    j1 += j2

print('done splitting')

for i in range(24):
    split[i].to_csv(f'rba-split-{i}.csv', index=False)
    print(split[i].head())